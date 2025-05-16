# src/evaluate.py

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, mean_absolute_error
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model

from src.config import MODEL_PATH, SEQUENCE_LENGTH
from src.preprocess import preprocess_data


def evaluate():
    print("📊 Evaluating final CNN-LSTM hybrid model...")

    # Load and preprocess data
    X, y_class, y_mag, y_lat, y_lon, y_time = preprocess_data(sequence_length=SEQUENCE_LENGTH)

    # Validation split
    _, X_val, _, y_class_val, _, y_mag_val, _, y_lat_val, _, y_lon_val, _, y_time_val = train_test_split(
        X, y_class, y_mag, y_lat, y_lon, y_time, test_size=0.2, random_state=42
    )

    # Load model
    model = load_model(MODEL_PATH, compile=False)

    # Predict
    predictions = model.predict(X_val, batch_size=32)
    (
        y_class_pred_prob,
        y_mag_pred,
        y_lat_pred,
        y_lon_pred,
        y_time_pred
    ) = predictions

    y_class_pred = (y_class_pred_prob > 0.5).astype(int)

    # 📋 Classification metrics
    print("\n✅ Classification Report:")
    print(classification_report(y_class_val, y_class_pred))

    print("📉 Confusion Matrix:")
    print(confusion_matrix(y_class_val, y_class_pred))

    # 📊 Regression metrics
    def print_regression_metrics(name, y_true, y_pred):
        mae = mean_absolute_error(y_true, y_pred)
        print(f"🔢 Mean Absolute Error ({name}): {mae:.4f}")
        return mae

    print_regression_metrics("Magnitude", y_mag_val, y_mag_pred)
    print_regression_metrics("Latitude", y_lat_val, y_lat_pred)
    print_regression_metrics("Longitude", y_lon_val, y_lon_pred)
    print_regression_metrics("Time Delta", y_time_val, y_time_pred)

    # 📈 Plot predictions vs true values for magnitude
    plt.figure(figsize=(12, 6))
    plt.plot(y_mag_val[:200], label="True Magnitude")
    plt.plot(y_mag_pred[:200], label="Predicted Magnitude", linestyle="--")
    plt.title("Magnitude Prediction vs. Ground Truth")
    plt.xlabel("Sample Index")
    plt.ylabel("Magnitude")
    plt.legend()
    plt.tight_layout()

    # Save plot
    output_dir = "outputs/plots"
    os.makedirs(output_dir, exist_ok=True)
    plot_path = os.path.join(output_dir, "magnitude_prediction_vs_true.png")
    plt.savefig(plot_path)
    print(f"📈 Plot saved to: {plot_path}")


if __name__ == "__main__":
    evaluate()
