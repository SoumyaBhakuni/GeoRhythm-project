import os
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model, save_model
from src.config import SEQ_LENGTH, SCALER_PATH

# -----------------------
# 🔧 Directory Utilities
# -----------------------

def ensure_dir(path):
    """Ensure a directory exists (file or directory path-safe)."""
    dir_path = path if os.path.isdir(path) else os.path.dirname(path)
    os.makedirs(dir_path, exist_ok=True)

# -----------------------
# ⚙️ Preprocessing
# -----------------------

def preprocess_chunk(df, sequence_length=SEQ_LENGTH, scaler=None, verbose=False):

    if 'timestamp' in df.columns:
        df['time'] = pd.to_datetime(df['timestamp'], unit='ms', errors='coerce')
    else:
        df['time'] = pd.to_datetime(df['time'], errors='coerce')

    df = df.sort_values('time').reset_index(drop=True)
    df = df[['time', 'latitude', 'longitude', 'depth_km', 'magnitude']].dropna()
    df.rename(columns={'depth_km': 'depth', 'magnitude': 'mag'}, inplace=True)

    df['event_occurred'] = df['mag'].apply(lambda m: 1 if m > 0 else 0)

    input_features = ['latitude', 'longitude', 'depth', 'mag']

    if len(df) < sequence_length + 2:
        if verbose:
            print(f"⚠️ Skipping chunk: only {len(df)} valid rows after cleaning (need ≥ {sequence_length + 2})")
        return np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([])

    # Apply or create scaler
    if scaler is None:
        if not os.path.exists(SCALER_PATH):
            raise FileNotFoundError(f"Scaler not found at {SCALER_PATH}. Please run full preprocessing first.")
        scaler = joblib.load(SCALER_PATH)

    df[input_features] = scaler.transform(df[input_features])

    X, y_class, y_mag, y_lat, y_lon, y_time = [], [], [], [], [], []

    for i in range(len(df) - sequence_length - 1):
        seq = df.iloc[i:i + sequence_length][input_features].values
        target = df.iloc[i + sequence_length]
        next_event = df.iloc[i + sequence_length + 1]

        # Check for any NaNs or invalid timestamps
        if (
            np.isnan(seq).any() or
            pd.isnull(target['time']) or
            pd.isnull(next_event['time'])
        ):
            if verbose:
                print(f"⚠️ Skipping sequence at index {i}: contains NaNs or invalid timestamps.")
            continue

        delta_days = max((next_event['time'] - target['time']).total_seconds() / (3600 * 24), 0)

        X.append(seq)
        y_class.append(target['event_occurred'])
        y_mag.append(target['mag'])
        y_lat.append(target['latitude'])
        y_lon.append(target['longitude'])
        y_time.append(delta_days)

    if verbose:
        print(f"✅ Processed {len(X)} valid sequences from chunk.")

    return (
        np.array(X),
        np.array(y_class),
        np.array(y_mag),
        np.array(y_lat),
        np.array(y_lon),
        np.array(y_time)
    )

# -----------------------
# 💾 Scaler Utilities
# -----------------------

def save_scaler(scaler, path):
    ensure_dir(path)
    joblib.dump(scaler, path)
    print(f"✅ Scaler saved to: {path}")

def load_scaler(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Scaler not found at: {path}")
    return joblib.load(path)

# -----------------------
# 💾 Model Utilities
# -----------------------

def save_keras_model(model, path):
    ensure_dir(path)
    save_model(model, path)
    print(f"✅ Model saved to: {path}")

def load_keras_model(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Model not found at: {path}")
    return load_model(path)

# -----------------------
# 📈 Plotting Utilities
# -----------------------

def plot_prediction_vs_truth(true_vals, pred_vals, save_path=None):
    true_vals = np.array(true_vals)
    pred_vals = np.array(pred_vals)

    plt.figure(figsize=(8, 4))
    plt.plot(true_vals, label="Actual", marker="o", linestyle="--", color="green")
    plt.plot(pred_vals, label="Predicted", marker="x", linestyle="-", color="blue")
    plt.xlabel("Time Step")
    plt.ylabel("Magnitude")
    plt.title("Predicted vs Actual Earthquake Magnitudes")
    plt.legend()
    plt.grid(True)

    if save_path:
        ensure_dir(save_path)
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
    else:
        plt.show()
