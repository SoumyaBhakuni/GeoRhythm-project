from flask import Flask, request, jsonify, send_file
import pandas as pd
import datetime
import joblib
import os

from tensorflow.keras.models import load_model
from flask_cors import CORS

# Import internal modules
from src.config import SEQ_LENGTH, MODEL_PATH, SCALER_PATH
from src.utils import (
    load_scaler, load_keras_model, sequence_splitter,
    latlon_to_location
)
from src.inference import run_inference
from src.fetch_from_mongo import fetch_latest_sequence, fetch_random_sequence
from src.usgs_fetcher import fetch_usgs_last_month

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})

# Load model and scaler
model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

PLOTS_DIR = "outputs/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

# ---------------- UTILS -------------------

def prepare_input(data: list, scaler, sequence_length=SEQ_LENGTH):
    df = pd.DataFrame(data)
    df.sort_values("time", inplace=True)
    df.reset_index(drop=True, inplace=True)
    numeric_cols = ["latitude", "longitude", "depth", "mag"]
    df[numeric_cols] = scaler.transform(df[numeric_cols])
    X = sequence_splitter(df, sequence_length)
    return X, df.iloc[-1]  # last context row

def format_prediction(pred, context_row):
    if pred["event_occurred"] == 0:
        return "✅ No significant earthquake predicted in the immediate future."

    base_time = pd.to_datetime(context_row["time"])
    predicted_time = base_time + datetime.timedelta(days=pred["time_delta_days"])
    location_str = latlon_to_location(pred["latitude"], pred["longitude"])

    return (
        f"Prediction:\n"
        f"An earthquake of ~{pred['magnitude']:.1f} magnitude is likely to occur "
        f"near {location_str} ({pred['latitude']:.2f}°N, {pred['longitude']:.2f}°E) "
        f"around {predicted_time.strftime('%B %d, %Y')} ± 2 days."
    )

# ---------------- ROUTES -------------------

@app.route("/")
def index():
    return jsonify({"message": "🌍 Seismic Hybrid Model API is running."})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not isinstance(data, list) or len(data) < SEQ_LENGTH:
            return jsonify({"error": f"Input must be a list of at least {SEQ_LENGTH} records."}), 400

        result, plot_paths = run_inference(model, scaler, data)

        # Defensive get for context_time:
        context_time = result.get("context_time", None)
        if context_time is None:
            return jsonify({"error": "'context_time' missing from prediction result"}), 500

        message = format_prediction(result, {"time": context_time})

        # Defensive handling for plot_paths:
        if plot_paths is None:
            plot_paths = []

        plot_urls = [
            f"/plot/{os.path.basename(path)}"
            for path in plot_paths
            if os.path.exists(path)
        ]

        return jsonify({
            "prediction": result,
            "natural_language_summary": message,
            "plot_urls": plot_urls
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/predict-latest", methods=["GET"])
def predict_latest():
    try:
        data = fetch_latest_sequence()
        X_input, context_row = prepare_input(data, scaler)
        preds = model.predict(X_input)

        result = {
            "event_occurred": int(preds[0][-1][0] > 0.5),
            "confidence": float(preds[0][-1][0]),
            "magnitude": float(preds[1][-1][0]),
            "latitude": float(preds[2][-1][0]),
            "longitude": float(preds[3][-1][0]),
            "time_delta_days": float(preds[4][-1][0]),
            "context_time": context_row["time"]
        }

        return jsonify({
            "prediction": result,
            "natural_language_summary": format_prediction(result, context_row)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/generate-sample-sequence", methods=["GET"])
def generate_sample_sequence():
    sequence = []
    for i in range(30):
        sequence.append({
            "time": f"2023-01-01T00:{i:02d}:00Z",
            "latitude": 35.5 + i * 0.01,
            "longitude": -117.5 + i * 0.01,
            "depth": 10 + i * 0.1,
            "mag": 4.5 + (i % 3) * 0.1
        })
    return jsonify(sequence)


@app.route("/fetch-usgs-latest-month", methods=["GET"])
def fetch_usgs_latest():
    try:
        sequence = fetch_usgs_last_month()
        return jsonify({"sequence": sequence[-SEQ_LENGTH:]})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ---------------- UNIVERSAL PLOT ROUTE -------------------

@app.route("/plot/<filename>")
def serve_plot(filename):
    path = os.path.join(PLOTS_DIR, filename)
    if os.path.exists(path):
        return send_file(path, mimetype="image/png")
    return jsonify({"error": f"Plot {filename} not found."}), 404

# ---------------- RUN APP -------------------

if __name__ == "__main__":
    app.run(debug=True)
