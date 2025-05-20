import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, mean_absolute_error
import seaborn as sns
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split

from src.SeismicDataGenerator import SeismicDataGenerator
from src.config import MODEL_PATH, CHUNK_OUTPUT_DIR, SEQ_LENGTH

def get_chunk_filepaths(output_dir=CHUNK_OUTPUT_DIR):
    files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.npz')]
    return sorted(files)

def evaluate_from_chunks():
    print("📁 Loading .npz chunk files...")
    chunk_files = get_chunk_filepaths()
    if not chunk_files:
        print("❌ No chunk files found.")
        return

    _, val_files = train_test_split(chunk_files, test_size=0.2, random_state=42)
    print(f"✅ Using {len(val_files)} chunk files for evaluation.")

    print("🧠 Loading trained model...")
    try:
        model = load_model(MODEL_PATH, compile=False)
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return

    print("📦 Collecting validation data into memory...")
    X_val, y_class_val, y_mag_val, y_lat_val, y_lon_val, y_time_val = [], [], [], [], [], []
    for file in val_files:
        with np.load(file) as data:
            X_val.append(data['X'])
            y_class_val.append(data['y_class'])
            y_mag_val.append(data['y_mag'])
            y_lat_val.append(data['y_lat'])
            y_lon_val.append(data['y_lon'])
            y_time_val.append(data['y_time'])

    X_val = np.concatenate(X_val, axis=0)
    y_class_val = np.concatenate(y_class_val, axis=0).flatten()
    y_mag_val = np.concatenate(y_mag_val, axis=0).flatten()
    y_lat_val = np.concatenate(y_lat_val, axis=0).flatten()
    y_lon_val = np.concatenate(y_lon_val, axis=0).flatten()
    y_time_val = np.concatenate(y_time_val, axis=0).flatten()

    print("🤖 Running inference...")
    predictions = model.predict(X_val, batch_size=32)
    y_class_pred_prob = predictions[0].flatten()
    y_mag_pred = predictions[1].flatten()
    y_lat_pred = predictions[2].flatten()
    y_lon_pred = predictions[3].flatten()
    y_time_pred = predictions[4].flatten()

    y_class_pred = (y_class_pred_prob > 0.5).astype(int)

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
    cm_path = os.path.join(output_dir, "confusion_matrix_chunks.png")
    plt.savefig(cm_path)
    print(f"📉 Confusion matrix saved to: {cm_path}")

    def plot_regression_metric(name, y_true, y_pred):
        mae = mean_absolute_error(y_true, y_pred)
        print(f"🔢 Mean Absolute Error ({name}): {mae:.4f}")

        plt.figure(figsize=(12, 4))
        plt.plot(y_true[:200], label=f"True {name}")
        plt.plot(y_pred[:200], label=f"Predicted {name}", linestyle='--')
        plt.title(f"{name} Prediction vs Ground Truth")
        plt.xlabel("Sample Index")
        plt.ylabel(name)
        plt.legend()
        plt.tight_layout()
        plot_path = os.path.join(output_dir, f"{name.lower().replace(' ', '_')}_chunks.png")
        plt.savefig(plot_path)
        print(f"📈 {name} plot saved to: {plot_path}")

    plot_regression_metric("Magnitude", y_mag_val, y_mag_pred)
    plot_regression_metric("Latitude", y_lat_val, y_lat_pred)
    plot_regression_metric("Longitude", y_lon_val, y_lon_pred)
    plot_regression_metric("Time Delta", y_time_val, y_time_pred)

    print("\n🔍 Sample Predictions (first 5):")
    for i in range(5):
        print(f"[{i}] Event: {y_class_val[i]} → {y_class_pred[i]}, "
              f"Magnitude: {y_mag_val[i]:.2f} → {y_mag_pred[i]:.2f}, "
              f"Lat: {y_lat_val[i]:.2f} → {y_lat_pred[i]:.2f}, "
              f"Lon: {y_lon_val[i]:.2f} → {y_lon_pred[i]:.2f}, "
              f"Time Δ: {y_time_val[i]:.2f} → {y_time_pred[i]:.2f}")


if __name__ == "__main__":
    evaluate_from_chunks()
