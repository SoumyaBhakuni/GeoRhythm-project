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
    latlon_to_location, plot_prediction_vs_truth
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

        X_input, context_row = prepare_input(data, scaler)
        preds = model.predict(X_input)

        y_cls_prob = preds[0][:, 0]
        y_mag = preds[1][:, 0]
        y_lat = preds[2][:, 0]
        y_lon = preds[3][:, 0]
        y_time = preds[4][:, 0]

        result = {
            "event_occurred": int(y_cls_prob[-1] > 0.5),
            "confidence": float(y_cls_prob[-1]),
            "magnitude": float(y_mag[-1]),
            "latitude": float(y_lat[-1]),
            "longitude": float(y_lon[-1]),
            "time_delta_days": float(y_time[-1]),
            "context_time": context_row["time"]
        }

        message = format_prediction(result, context_row)

        # Plot actual (from last sequence) vs predicted magnitude
        true_vals = [entry["mag"] for entry in data[-SEQ_LENGTH:]]
        pred_vals = true_vals[:-1] + [result["magnitude"]]  # Dummy: predict only last step
        plot_path = "outputs/plots/predict_manual.png"
        plot_prediction_vs_truth(true_vals, pred_vals, plot_path)

        return jsonify({
            "prediction": result,
            "natural_language_summary": message,
            "plot_url": "/plot/predict-manual"
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

        plot_path = os.path.join(PLOTS_DIR, "predict_latest.png")
        plot_prediction_vs_truth(
            true_vals=[context_row["mag"]],
            pred_vals=[result["magnitude"]],
            save_path=plot_path
        )

        return jsonify({
            "prediction": result,
            "natural_language_summary": format_prediction(result, context_row)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/generate-sample-sequence", methods=["GET"])
def generate_sample_sequence():
    try:
        sequence = fetch_random_sequence()
        plot_path = os.path.join(PLOTS_DIR, "sample_sequence_plot.png")
        plot_prediction_vs_truth(
            true_vals=[item["mag"] for item in sequence],
            pred_vals=[item["mag"] * 0.95 for item in sequence],  # Dummy
            save_path=plot_path
        )
        return jsonify({
            "sequence": sequence,
            "plot_url": "/plot/sample-sequence"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/fetch-usgs-latest-month", methods=["GET"])
def fetch_usgs_latest():
    try:
        sequence = fetch_usgs_last_month()
        return jsonify({"sequence": sequence[-SEQ_LENGTH:]})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ---------------- PLOT SERVING ROUTES -------------------

@app.route("/plot/predict-manual")
def plot_manual():
    path = os.path.join(PLOTS_DIR, "predict_manual.png")
    if os.path.exists(path):
        return send_file(path, mimetype="image/png")
    return jsonify({"error": "Manual prediction plot not found."}), 404

@app.route("/plot/predict-latest")
def plot_latest():
    path = os.path.join(PLOTS_DIR, "predict_latest.png")
    if os.path.exists(path):
        return send_file(path, mimetype="image/png")
    return jsonify({"error": "Latest prediction plot not found."}), 404

@app.route("/plot/predict-manual")
def serve_predict_manual_plot():
    return send_file("outputs/plots/predict_manual.png", mimetype="image/png")

@app.route("/plot/predict-latest")
def serve_predict_latest_plot():
    return send_file("outputs/plots/predict_latest.png", mimetype="image/png")

@app.route("/plot/sample-sequence")
def plot_sample():
    path = os.path.join(PLOTS_DIR, "sample_sequence_plot.png")
    if os.path.exists(path):
        return send_file(path, mimetype="image/png")
    return jsonify({"error": "Sample plot not found."}), 404

# ---------------- RUN APP -------------------

if __name__ == "__main__":
    app.run(debug=True)
