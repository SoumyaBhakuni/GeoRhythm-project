import os
import numpy as np
import argparse
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

from src.SeismicDataGenerator import SeismicDataGenerator
from src.model_cnn_lstm import build_cnn_lstm_model as build_hybrid_model
from src.config import MODEL_PATH, SEQ_LENGTH, CHUNK_OUTPUT_DIR

OUTPUT_DIR = CHUNK_OUTPUT_DIR


def get_chunk_filepaths(output_dir=OUTPUT_DIR):
    files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.npz')]
    return sorted(files)


def compute_scalers(chunk_files):
    mag_vals, lat_vals, lon_vals, time_vals = [], [], [], []

    for file in chunk_files:
        with np.load(file) as data:
            mag_vals.append(data['y_mag'])
            lat_vals.append(data['y_lat'])
            lon_vals.append(data['y_lon'])
            time_vals.append(data['y_time'])

    mag_all = np.concatenate(mag_vals).reshape(-1, 1)
    lat_all = np.concatenate(lat_vals).reshape(-1, 1)
    lon_all = np.concatenate(lon_vals).reshape(-1, 1)
    time_all = np.concatenate(time_vals).reshape(-1, 1)

    scalers = {
        'magnitude': StandardScaler().fit(mag_all),
        'lat': StandardScaler().fit(lat_all),
        'lon': StandardScaler().fit(lon_all),
        'time': StandardScaler().fit(time_all),
    }

    joblib.dump(scalers, "outputs/models/output_scalers.pkl")
    return scalers


def train_on_chunks(batch_size=64, validation_split=0.2, epochs=50):
    print("📥 Preparing chunk filepaths...")
    chunk_files = get_chunk_filepaths()
    if not chunk_files:
        raise RuntimeError(f"No chunk files found in {OUTPUT_DIR}")

    print(f"🟢 Found {len(chunk_files)} chunk files.")

    train_files, val_files = train_test_split(chunk_files, test_size=validation_split, random_state=42)

    print(f"🟢 Training on {len(train_files)} chunks, validating on {len(val_files)} chunks.")

    scalers = compute_scalers(train_files)

    train_generator = SeismicDataGenerator(train_files, batch_size=batch_size,
                                           sequence_length=SEQ_LENGTH, shuffle=True,
                                           scalers=scalers)

    val_generator = SeismicDataGenerator(val_files, batch_size=batch_size,
                                         sequence_length=SEQ_LENGTH, shuffle=False,
                                         scalers=scalers)

    example_chunk = np.load(train_files[0])
    X_example = example_chunk['X']
    seq_length, feature_dim = X_example.shape[1], X_example.shape[2]

    print(f"⚙️ Building model for input shape: (seq_length={seq_length}, feature_dim={feature_dim})")
    model = build_hybrid_model(seq_length, feature_dim)

    model.compile(
        optimizer='adam',
        loss={
            'event_occurred': 'binary_crossentropy',
            'magnitude': 'mse',
            'location_lat': 'mse',
            'location_lon': 'mse',
            'time_delta': 'mse'
        },
        loss_weights={
            'event_occurred': 1.0,
            'magnitude': 0.5,
            'location_lat': 0.5,
            'location_lon': 0.5,
            'time_delta': 0.5
        },
        metrics={
            'event_occurred': 'accuracy',
            'magnitude': 'mae',
            'location_lat': 'mae',
            'location_lon': 'mae',
            'time_delta': 'mae'
        }
    )

    early_stop = EarlyStopping(
        monitor='val_event_occurred_accuracy',
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
    checkpoint = ModelCheckpoint(
        MODEL_PATH,
        monitor='val_event_occurred_accuracy',
        save_best_only=True,
        verbose=1
    )

    print("🚀 Starting training on chunked data...")
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=epochs,
        callbacks=[early_stop, checkpoint],
        verbose=1,
        use_multiprocessing=False,
        workers=1,
        max_queue_size=10,
    )

    print(f"✅ Training complete. Saving final model to {MODEL_PATH} ...")
    model.save(MODEL_PATH)
    print("✅ Model saved successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train seismic CNN-LSTM model on .npz chunked data")
    parser.add_argument('--batch_size', type=int, default=64, help='Batch size for training')
    parser.add_argument('--validation_split', type=float, default=0.2, help='Validation split fraction')
    parser.add_argument('--epochs', type=int, default=50, help='Number of epochs to train')
    args = parser.parse_args()

    train_on_chunks(batch_size=args.batch_size, validation_split=args.validation_split, epochs=args.epochs)
