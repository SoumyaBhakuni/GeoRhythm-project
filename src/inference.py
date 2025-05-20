# src/inference.py

import os
import json
import numpy as np
import pandas as pd
import datetime
import joblib
from tensorflow.keras.models import load_model

from src.config import MODEL_PATH, SCALER_PATH, SEQ_LENGTH
from src.utils import sequence_splitter, latlon_to_location
from src.fetch_from_mongo import fetch_earthquake_data


def load_artifacts():
    print("📦 Loading model and scaler...")
    model = load_model(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler


def prepare_input(df_raw, scaler, sequence_length=SEQ_LENGTH):
    print("🧼 Preprocessing input for inference...")
    df = df_raw.copy()
    df.sort_values("time", inplace=True)
    df.reset_index(drop=True, inplace=True)

    numeric_cols = ["latitude", "longitude", "depth", "mag"]
    df[numeric_cols] = scaler.transform(df[numeric_cols])

    X = sequence_splitter(df, sequence_length=sequence_length)

    if len(X) == 0:
        raise ValueError("❌ Not enough data to form a sequence.")

    return X, df.tail(1)


def generate_prediction(model, X, context_df):
    print("🔮 Generating predictions...")
    predictions = model.predict(X)

    y_cls_prob = predictions[0][:, 0]
    y_mag = predictions[1][:, 0]
    y_lat = predictions[2][:, 0]
    y_lon = predictions[3][:, 0]
    y_time_delta = predictions[4][:, 0]

    y_cls = int(y_cls_prob[-1] > 0.5)

    return {
        "event_occurred": y_cls,
        "confidence": float(y_cls_prob[-1]),
        "magnitude": float(y_mag[-1]),
        "latitude": float(y_lat[-1]),
        "longitude": float(y_lon[-1]),
        "time_delta_days": float(y_time_delta[-1]),
        "context_time": context_df.iloc[-1]["time"]
    }


def format_natural_language_prediction(pred):
    if pred["event_occurred"] == 0:
        return "✅ No significant earthquake predicted in the immediate future."

    base_time = pd.to_datetime(pred["context_time"])
    predicted_time = base_time + datetime.timedelta(days=pred["time_delta_days"])
    location_str = latlon_to_location(pred["latitude"], pred["longitude"])

    return (
        f"🌍 Prediction:\n"
        f"An earthquake of ~{pred['magnitude']:.1f} magnitude is likely to occur "
        f"near {location_str} ({pred['latitude']:.2f}°N, {pred['longitude']:.2f}°E) "
        f"around {predicted_time.strftime('%B %d, %Y')} ± 2 days."
    )


def run_inference(model, scaler, data):
    try:
        if isinstance(data, list):
            input_df = pd.DataFrame(data)
        else:
            input_df = data

        X, context_row = prepare_input(input_df, scaler)
        pred = generate_prediction(model, X, context_row)
        message = format_natural_language_prediction(pred)

        print("✅ Prediction complete.")
        print(message)
        # Return prediction dict directly, not wrapped in {"prediction": ...}
        return pred, []  # plot paths list

    except Exception as e:
        print(f"❌ Inference failed: {e}")
        return {"error": str(e)}, []


if __name__ == "__main__":
    df_full = fetch_earthquake_data()
    df_recent = df_full.sort_values("time").tail(SEQ_LENGTH)

    response = run_inference(df_recent)

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/inference_result.json", "w") as f:
        json.dump(response, f, indent=4, default=str)
    print("📝 Inference result saved to outputs/inference_result.json")
    print("✅ Inference process completed.")
