import os
import numpy as np
import pandas as pd
import joblib
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import resample

from src.fetch_from_mongo import fetch_in_chunks, fetch_earthquake_data
from src.utils import preprocess_chunk
from src.config import SCALER_PATH, SEQ_LENGTH

OUTPUT_DIR = "outputs/processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def preprocess_data(df, sequence_length=SEQ_LENGTH, balance=True):
    """
    Preprocess earthquake data into sequences for CNN-LSTM hybrid model (non-chunked version).
    """
    print("🔧 Preprocessing full dataset...")

    # Clean and sort
    df['time'] = pd.to_datetime(df['timestamp'], unit='ms', errors='coerce')
    df.dropna(subset=['time'], inplace=True)
    df = df[['time', 'latitude', 'longitude', 'depth_km', 'magnitude']].dropna()
    df.rename(columns={'depth_km': 'depth', 'magnitude': 'mag'}, inplace=True)
    df.sort_values('time', inplace=True)
    df.reset_index(drop=True, inplace=True)

    df['event_occurred'] = df['mag'].apply(lambda m: 1 if m > 0 else 0)

    input_features = ['latitude', 'longitude', 'depth', 'mag']
    os.makedirs(os.path.dirname(SCALER_PATH), exist_ok=True)

    if os.path.exists(SCALER_PATH):
        print(f"📦 Loading existing scaler from {SCALER_PATH}")
        scaler = joblib.load(SCALER_PATH)
    else:
        print("🧪 Fitting new scaler and saving...")
        scaler = MinMaxScaler()
        scaler.fit(df[input_features])
        joblib.dump(scaler, SCALER_PATH)
        print(f"💾 Scaler saved to {SCALER_PATH}")

    df[input_features] = scaler.transform(df[input_features])

    print(f"💾 Scaler saved to {SCALER_PATH}")

    X, y_class, y_mag, y_lat, y_lon, y_time = [], [], [], [], [], []

    for i in range(len(df) - sequence_length - 1):
        seq = df.iloc[i:i + sequence_length][input_features].values
        target = df.iloc[i + sequence_length]
        next_event = df.iloc[i + sequence_length + 1]

        delta_days = max((next_event['time'] - target['time']).total_seconds() / (3600 * 24), 0)

        X.append(seq)
        y_class.append(target['event_occurred'])
        y_mag.append(target['mag'])
        y_lat.append(target['latitude'])
        y_lon.append(target['longitude'])
        y_time.append(delta_days)

    X = np.array(X)
    y_class = np.array(y_class)
    y_mag = np.array(y_mag)
    y_lat = np.array(y_lat)
    y_lon = np.array(y_lon)
    y_time = np.array(y_time)

    if balance:
        print("⚖️ Balancing dataset...")
        class_0_idx = np.where(y_class == 0)[0]
        class_1_idx = np.where(y_class == 1)[0]

        if class_0_idx.size > 0 and class_1_idx.size > 0:
            class_0_upsampled = resample(class_0_idx, replace=True, n_samples=len(class_1_idx), random_state=42)
            all_idx = np.concatenate([class_0_upsampled, class_1_idx])
            np.random.shuffle(all_idx)

            X = X[all_idx]
            y_class = y_class[all_idx]
            y_mag = y_mag[all_idx]
            y_lat = y_lat[all_idx]
            y_lon = y_lon[all_idx]
            y_time = y_time[all_idx]
            print(f"✅ Balanced: {len(y_class)} samples")
        else:
            print("⚠️ Skipping balancing: one of the classes is missing.")

    return X, y_class, y_mag, y_lat, y_lon, y_time


def preprocess_large_dataset(sequence_length=SEQ_LENGTH, save_chunks=True, max_chunks=None):
    """
    Chunked preprocessing for large MongoDB datasets. Saves .npz files if requested.
    """
    print("🔧 Starting chunked preprocessing...")

    X_all, y_class_all, y_mag_all, y_lat_all, y_lon_all, y_time_all = [], [], [], [], [], []

    for chunk_idx, df_chunk in enumerate(tqdm(fetch_in_chunks(batch_size=10000), desc="📦 Processing chunks")):
        if max_chunks is not None and chunk_idx >= max_chunks:
            print(f"🛑 Stopping after {max_chunks} chunks.")
            break

        if df_chunk.empty or len(df_chunk) < sequence_length + 2:
            print(f"⚠️ Skipping chunk {chunk_idx}: too few records ({len(df_chunk)} rows)")
            continue

        try:
            X, y_class, y_mag, y_lat, y_lon, y_time = preprocess_chunk(df_chunk, sequence_length, verbose=True)

            if X.size == 0:
                print(f"⚠️ Chunk {chunk_idx} returned empty arrays.")
                continue

            if save_chunks:
                chunk_path = os.path.join(OUTPUT_DIR, f"chunk_{chunk_idx:03}.npz")
                np.savez_compressed(
                    chunk_path,
                    X=X,
                    y_class=y_class,
                    y_mag=y_mag,
                    y_lat=y_lat,
                    y_lon=y_lon,
                    y_time=y_time
                )
                print(f"✅ Saved: {chunk_path}")

            X_all.append(X)
            y_class_all.append(y_class)
            y_mag_all.append(y_mag)
            y_lat_all.append(y_lat)
            y_lon_all.append(y_lon)
            y_time_all.append(y_time)

        except Exception as e:
            print(f"❌ Error processing chunk {chunk_idx}: {e}")
            continue

    if not X_all:
        raise RuntimeError("❌ No valid data processed. Please check your dataset and filters.")

    print("📊 Concatenating all processed data...")
    return (
        np.concatenate(X_all),
        np.concatenate(y_class_all),
        np.concatenate(y_mag_all),
        np.concatenate(y_lat_all),
        np.concatenate(y_lon_all),
        np.concatenate(y_time_all)
    )


if __name__ == "__main__":
    # Toggle between full vs chunked mode
    USE_CHUNKED = True

    if USE_CHUNKED:
        X, y_class, y_mag, y_lat, y_lon, y_time = preprocess_large_dataset()
    else:
        df = fetch_earthquake_data()
        X, y_class, y_mag, y_lat, y_lon, y_time = preprocess_data(df)

    print("✅ Final shapes:")
    print(f"X: {X.shape}, y_class: {y_class.shape}, y_mag: {y_mag.shape}")
    print("✅ Preprocessing complete.")
