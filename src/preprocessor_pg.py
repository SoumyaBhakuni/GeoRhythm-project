import os
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
from src.fetch_from_postgress import fetch_in_chunks  # Import your PG fetch function

OUTPUT_DIR = './outputs/processed/'
SCALER_DIR = './scalers/'

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SCALER_DIR, exist_ok=True)

SEQ_LENGTH = 30  # Same as before
CHUNK_SIZE = 50000  # Chunk size for saving processed data

def preprocess_row(row):
    # row is a dict with keys: timestamp, latitude, longitude, depth_km, magnitude
    features = [
        row.get('magnitude', 0.0),
        row.get('latitude', 0.0),
        row.get('longitude', 0.0),
        row.get('depth_km', 0.0)
    ]
    # For targets, define event_occurred as magnitude > 0 (or customize)
    y_class = 1 if row.get('magnitude', 0.0) > 0 else 0
    y_mag = row.get('magnitude', 0.0)
    y_lat = row.get('latitude', 0.0)
    y_lon = row.get('longitude', 0.0)
    # For time_delta, you can define as difference between current and previous timestamp
    # But here just use 0 for simplicity or extend with real calculation later
    y_time = 0.0
    return features, y_class, y_mag, y_lat, y_lon, y_time

def chunk_data(features_list, y_class_list, y_mag_list, y_lat_list, y_lon_list, y_time_list):
    n_samples = len(features_list)
    n_chunks = int(np.ceil(n_samples / CHUNK_SIZE))
    print(f"💾 Splitting data into {n_chunks} chunks of size up to {CHUNK_SIZE}.")

    for i in range(n_chunks):
        start = i * CHUNK_SIZE
        end = min(start + CHUNK_SIZE, n_samples)

        X_chunk = np.array(features_list[start:end])
        y_class_chunk = np.array(y_class_list[start:end])
        y_mag_chunk = np.array(y_mag_list[start:end])
        y_lat_chunk = np.array(y_lat_list[start:end])
        y_lon_chunk = np.array(y_lon_list[start:end])
        y_time_chunk = np.array(y_time_list[start:end])

        # Reshape to (samples, seq_length, features)
        # Assumes your data is sequential and can be reshaped this way
        X_chunk = X_chunk.reshape((-1, SEQ_LENGTH, 4))

        chunk_path = os.path.join(OUTPUT_DIR, f'data_chunk_{i:04d}.npz')
        np.savez_compressed(chunk_path,
                            X=X_chunk,
                            y_class=y_class_chunk,
                            y_mag=y_mag_chunk,
                            y_lat=y_lat_chunk,
                            y_lon=y_lon_chunk,
                            y_time=y_time_chunk)
        print(f"Saved chunk {i+1}/{n_chunks} at {chunk_path}")

def main():
    features_list, y_class_list, y_mag_list, y_lat_list, y_lon_list, y_time_list = [], [], [], [], [], []

    print("📥 Fetching earthquake data from PostgreSQL in chunks...")
    for chunk_df in fetch_in_chunks(batch_size=100000):  # large batch size for efficiency
        for _, row in chunk_df.iterrows():
            features, y_class, y_mag, y_lat, y_lon, y_time = preprocess_row(row)
            features_list.append(features)
            y_class_list.append(y_class)
            y_mag_list.append(y_mag)
            y_lat_list.append(y_lat)
            y_lon_list.append(y_lon)
            y_time_list.append(y_time)

    print(f"📊 Total entries fetched and preprocessed: {len(features_list)}")

    # Fit scalers on targets
    print("⚙️ Fitting scalers on targets...")
    scaler_mag = MinMaxScaler().fit(np.array(y_mag_list).reshape(-1,1))
    scaler_lat = MinMaxScaler().fit(np.array(y_lat_list).reshape(-1,1))
    scaler_lon = MinMaxScaler().fit(np.array(y_lon_list).reshape(-1,1))
    scaler_time = MinMaxScaler().fit(np.array(y_time_list).reshape(-1,1))

    # Save scalers
    joblib.dump(scaler_mag, os.path.join(SCALER_DIR, 'magnitude.pkl'))
    joblib.dump(scaler_lat, os.path.join(SCALER_DIR, 'latitude.pkl'))
    joblib.dump(scaler_lon, os.path.join(SCALER_DIR, 'longitude.pkl'))
    joblib.dump(scaler_time, os.path.join(SCALER_DIR, 'time_delta.pkl'))
    print(f"✅ Scalers saved in {SCALER_DIR}")

    # Scale targets before saving
    y_mag_scaled = scaler_mag.transform(np.array(y_mag_list).reshape(-1,1)).flatten()
    y_lat_scaled = scaler_lat.transform(np.array(y_lat_list).reshape(-1,1)).flatten()
    y_lon_scaled = scaler_lon.transform(np.array(y_lon_list).reshape(-1,1)).flatten()
    y_time_scaled = scaler_time.transform(np.array(y_time_list).reshape(-1,1)).flatten()

    chunk_data(features_list, y_class_list, y_mag_scaled, y_lat_scaled, y_lon_scaled, y_time_scaled)

if __name__ == "__main__":
    main()
