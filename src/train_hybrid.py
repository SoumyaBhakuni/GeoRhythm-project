import os
import numpy as np
import joblib
from keras.callbacks import EarlyStopping, ModelCheckpoint

from src.data_generator import SeismicDataGenerator
from src.model_cnn_lstm import build_cnn_lstm_model as build_hybrid_model
from src.preprocess import preprocess_large_dataset, preprocess_data
from src.fetch_from_mongo import fetch_earthquake_data
from src.config import MODEL_PATH, SCALER_PATH, SEQ_LENGTH, CHUNK_OUTPUT_DIR

def train_model_with_generator(X, y_class, y_mag, y_lat, y_lon, y_time):
    from sklearn.model_selection import train_test_split
    print("📚 Splitting data into train/val...")

    (X_train, X_val,
     y_class_train, y_class_val,
     y_mag_train, y_mag_val,
     y_lat_train, y_lat_val,
     y_lon_train, y_lon_val,
     y_time_train, y_time_val) = train_test_split(
        X, y_class, y_mag, y_lat, y_lon, y_time,
        test_size=0.2, random_state=42
    )

    print(f"✅ Training shape: {X_train.shape}, Validation shape: {X_val.shape}")
    seq_length, feature_dim = X.shape[1], X.shape[2]
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

    print("🔁 Using SeismicDataGenerator (in-memory)...")
    train_gen = SeismicDataGenerator(
        X=X_train,
        y_class=y_class_train,
        y_mag=y_mag_train,
        y_lat=y_lat_train,
        y_lon=y_lon_train,
        y_time=y_time_train,
        batch_size=64,
        shuffle=True
    )

    val_gen = SeismicDataGenerator(
        X=X_val,
        y_class=y_class_val,
        y_mag=y_mag_val,
        y_lat=y_lat_val,
        y_lon=y_lon_val,
        y_time=y_time_val,
        batch_size=64,
        shuffle=False
    )

    print("🚀 Starting training (in-memory)...")
    model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=50,
        callbacks=[early_stop, checkpoint],
        verbose=1
    )

    model.save(MODEL_PATH)
    print(f"✅ Training complete. Best model saved to {MODEL_PATH}")


if __name__ == "__main__":
    USE_CHUNKED = True

    if USE_CHUNKED:
        print("📥 Preprocessing from MongoDB in chunks...")
        preprocess_large_dataset()

        print("🔁 Initializing chunk-based SeismicDataGenerator...")
        train_gen = SeismicDataGenerator(chunk_dir=CHUNK_OUTPUT_DIR, batch_size=64, shuffle=True)
        val_gen = SeismicDataGenerator(chunk_dir=CHUNK_OUTPUT_DIR, batch_size=64, shuffle=False)

        sample_file = sorted([
            os.path.join(CHUNK_OUTPUT_DIR, f) for f in os.listdir(CHUNK_OUTPUT_DIR) if f.endswith(".npz")
        ])[0]
        sample = np.load(sample_file)
        seq_length, feature_dim = sample['X'].shape[1], sample['X'].shape[2]

        print(f"🧠 Building model with input shape: ({seq_length}, {feature_dim})...")
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

        print("🚀 Starting training (chunked)...")
        model.fit(
            train_gen,
            validation_data=val_gen,
            epochs=50,
            callbacks=[early_stop, checkpoint],
            verbose=1
        )

        model.save(MODEL_PATH)
        print(f"✅ Training complete. Best model saved to {MODEL_PATH}")

    else:
        print("📥 Fetching full dataset for in-memory preprocessing...")
        df = fetch_earthquake_data()
        X, y_class, y_mag, y_lat, y_lon, y_time = preprocess_data(df)

        print("🧠 Starting model training with generator...")
        train_model_with_generator(X, y_class, y_mag, y_lat, y_lon, y_time)
        print("✅ Model training complete.")
