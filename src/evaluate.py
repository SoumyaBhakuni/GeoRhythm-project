import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, mean_absolute_error
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model
import seaborn as sns

from src.config import MODEL_PATH, SEQ_LENGTH
from src.preprocess import preprocess_data  # Ensure this does NOT call fetch_from_mongo

def evaluate():
    print("📊 Evaluating final CNN-LSTM hybrid model...")

    try:
        print("📁 Loading local dataset from data/dummy_earthquakes.json...")
        df = pd.read_json("data/dummy_earthquakes.json")
        print(f"✅ Loaded {len(df)} records.")
    except Exception as e:
        print(f"❌ Failed to load local dataset: {e}")
        return

    print("🔧 Preprocessing data...")
    try:
        X, y_class, y_mag, y_lat, y_lon, y_time = preprocess_data(df, sequence_length=SEQ_LENGTH)
    except Exception as e:
        print(f"❌ Preprocessing failed: {e}")
        return

    print("🔄 Splitting validation data...")
    _, X_val, _, y_class_val, _, y_mag_val, _, y_lat_val, _, y_lon_val, _, y_time_val = train_test_split(
        X, y_class, y_mag, y_lat, y_lon, y_time, test_size=0.2, random_state=42
    )

    print("🧠 Loading trained model from:", MODEL_PATH)
    try:
        model = load_model(MODEL_PATH, compile=False)
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return

    print("🤖 Making predictions...")
    try:
        predictions = model.predict(X_val, batch_size=32)
        (
            y_class_pred_prob,
            y_mag_pred,
            y_lat_pred,
            y_lon_pred,
            y_time_pred
        ) = predictions
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return

    # Flatten all arrays
    y_class_pred = (y_class_pred_prob > 0.5).astype(int).flatten()
    y_mag_pred = y_mag_pred.flatten()
    y_lat_pred = y_lat_pred.flatten()
    y_lon_pred = y_lon_pred.flatten()
    y_time_pred = y_time_pred.flatten()

    y_class_val = y_class_val.flatten()
    y_mag_val = y_mag_val.flatten()
    y_lat_val = y_lat_val.flatten()
    y_lon_val = y_lon_val.flatten()
    y_time_val = y_time_val.flatten()

    # 📊 Classification metrics
    print("\n✅ Classification Report:")
    print(classification_report(y_class_val, y_class_pred))

    cm = confusion_matrix(y_class_val, y_class_pred)
    print("📉 Confusion Matrix:")
    print(cm)

    output_dir = "outputs/plots"
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    cm_path = os.path.join(output_dir, "confusion_matrix.png")
    plt.savefig(cm_path)
    print(f"📉 Confusion matrix saved to: {cm_path}")

    # 📈 Regression metrics and plots
    def print_and_plot_regression(name, y_true, y_pred):
        mae = mean_absolute_error(y_true, y_pred)
        print(f"🔢 Mean Absolute Error ({name}): {mae:.4f}")

        plt.figure(figsize=(12, 4))
        plt.plot(y_true[:200], label=f"True {name}")
        plt.plot(y_pred[:200], label=f"Predicted {name}", linestyle="--")
        plt.title(f"{name} Prediction vs. Ground Truth")
        plt.xlabel("Sample Index")
        plt.ylabel(name)
        plt.legend()
        plt.tight_layout()

        plot_path = os.path.join(output_dir, f"{name.lower().replace(' ', '_')}_vs_true.png")
        plt.savefig(plot_path)
        print(f"📈 {name} plot saved to: {plot_path}")
        return mae

    print_and_plot_regression("Magnitude", y_mag_val, y_mag_pred)
    print_and_plot_regression("Latitude", y_lat_val, y_lat_pred)
    print_and_plot_regression("Longitude", y_lon_val, y_lon_pred)
    print_and_plot_regression("Time Delta", y_time_val, y_time_pred)

    print("\n🧪 Sample Predictions (first 5):")
    for i in range(5):
        print(f"[{i}] Event: {y_class_val[i]} → {y_class_pred[i]}, "
              f"Magnitude: {y_mag_val[i]:.2f} → {y_mag_pred[i]:.2f}, "
              f"Lat: {y_lat_val[i]:.2f} → {y_lat_pred[i]:.2f}, "
              f"Lon: {y_lon_val[i]:.2f} → {y_lon_pred[i]:.2f}, "
              f"Time Δ: {y_time_val[i]:.2f} → {y_time_pred[i]:.2f}")


if __name__ == "__main__":
    evaluate()
