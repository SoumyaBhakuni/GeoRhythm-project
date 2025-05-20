from flask import Flask, request, jsonify, send_file
import pandas as pd
import datetime
import joblib
import os

from tensorflow.keras.models import load_model
from flask_cors import CORS

# Internal modules
from src.config import SEQ_LENGTH, MODEL_PATH, SCALER_PATH
from src.utils import (
    sequence_splitter, latlon_to_location
)
from src.inference import run_inference
from src.fetch_from_mongo import fetch_random_sequence
from src.usgs_fetcher import fetch_usgs_last_month

# Flask setup
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
    return X, df.iloc[-1]

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
        context_time = result.get("context_time")
        if context_time is None:
            return jsonify({"error": "'context_time' missing from prediction result"}), 500

        message = format_prediction(result, {"time": context_time})

        plot_urls = [
            f"/plot/{os.path.basename(path)}"
            for path in plot_paths or []
            if os.path.exists(path)
        ]

        return jsonify({
            "prediction": result,
            "natural_language_summary": message,
            "plot_urls": plot_urls
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def clean_usgs_data(raw_data):
    cleaned = []
    for d in raw_data:
        try:
            # Extract and convert to correct types; skip if missing or invalid
            lat = float(d.get("latitude"))
            lon = float(d.get("longitude"))
            depth = float(d.get("depth"))
            mag = float(d.get("mag"))
            time = d.get("time")  # assume string ISO format or timestamp
            
            # If any field is None or invalid, skip this entry
            if None in [lat, lon, depth, mag, time]:
                continue
            
            cleaned.append({
                "latitude": lat,
                "longitude": lon,
                "depth": depth,
                "mag": mag,
                "time": time
            })
        except Exception:
            # skip entries that fail conversion
            continue
    return cleaned

@app.route("/predict-latest-usgs", methods=["GET"])
def predict_latest_usgs():
    try:
        raw_data = fetch_usgs_last_month()[-SEQ_LENGTH:]
        data = clean_usgs_data(raw_data)

        if len(data) < SEQ_LENGTH:
            return jsonify({"error": f"Not enough valid data after cleaning (need {SEQ_LENGTH})."}), 400
        
        result, plot_paths = run_inference(model, scaler, data)

        message = format_prediction(result, {"time": result["context_time"]})
        plot_urls = [
            f"/plot/{os.path.basename(path)}"
            for path in plot_paths or []
            if os.path.exists(path)
        ]

        return jsonify({
            "prediction": result,
            "natural_language_summary": message,
            "plot_urls": plot_urls
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/fetch-random-sequence", methods=["GET"])
def fetch_random():
    try:
        sequence = fetch_random_sequence()
        return jsonify(sequence)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/plot/<filename>")
def serve_plot(filename):
    path = os.path.join(PLOTS_DIR, filename)
    if os.path.exists(path):
        return send_file(path, mimetype="image/png")
    return jsonify({"error": f"Plot {filename} not found."}), 404

# ---------------- RUN APP -------------------

if __name__ == "__main__":
    app.run(debug=True)
