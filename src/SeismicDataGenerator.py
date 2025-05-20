import numpy as np
import os
from tensorflow.keras.utils import Sequence
import joblib

class SeismicDataGenerator(Sequence):
    def __init__(self, chunk_files, batch_size=32, sequence_length=100, shuffle=True, scalers=None):
        """
        Args:
            chunk_files (list): List of paths to .npz chunk files.
            batch_size (int): Number of sequences per batch.
            sequence_length (int): Length of each input sequence.
            shuffle (bool): Whether to shuffle batches each epoch.
            scalers (dict): Dictionary of fitted scalers for each regression output.
        """
        self.chunk_files = chunk_files
        self.batch_size = batch_size
        self.sequence_length = sequence_length
        self.shuffle = shuffle
        self.scalers = scalers or {}

        # Load metadata: number of sequences per chunk for indexing
        self.chunk_data = []
        self.sequence_counts = []
        for path in self.chunk_files:
            with np.load(path) as data:
                self.chunk_data.append(path)
                self.sequence_counts.append(data['X'].shape[0])

        # Create global index mapping: (chunk_idx, seq_idx_in_chunk)
        self.indices = []
        for chunk_idx, count in enumerate(self.sequence_counts):
            for seq_idx in range(count):
                self.indices.append((chunk_idx, seq_idx))

        self.on_epoch_end()

    def __len__(self):
        return int(np.floor(len(self.indices) / self.batch_size))

    def __getitem__(self, index):
        batch_indices = self.indices[index * self.batch_size : (index + 1) * self.batch_size]

        X_batch, y_class_batch, y_mag_batch, y_lat_batch, y_lon_batch, y_time_batch = [], [], [], [], [], []

        # Group indices by chunk for efficient loading
        chunk_to_indices = {}
        for chunk_idx, seq_idx in batch_indices:
            chunk_to_indices.setdefault(chunk_idx, []).append(seq_idx)

        for chunk_idx, seq_indices in chunk_to_indices.items():
            chunk_path = self.chunk_data[chunk_idx]
            with np.load(chunk_path) as data:
                X = data['X']
                y_class = data['y_class']
                y_mag = data['y_mag']
                y_lat = data['y_lat']
                y_lon = data['y_lon']
                y_time = data['y_time']

                for seq_idx in seq_indices:
                    X_batch.append(X[seq_idx])
                    y_class_batch.append(y_class[seq_idx])
                    y_mag_batch.append(y_mag[seq_idx])
                    y_lat_batch.append(y_lat[seq_idx])
                    y_lon_batch.append(y_lon[seq_idx])
                    y_time_batch.append(y_time[seq_idx])

        # Convert to arrays
        X_batch = np.array(X_batch)
        y_class_batch = np.array(y_class_batch)
        y_mag_batch = np.array(y_mag_batch).reshape(-1, 1)
        y_lat_batch = np.array(y_lat_batch).reshape(-1, 1)
        y_lon_batch = np.array(y_lon_batch).reshape(-1, 1)
        y_time_batch = np.array(y_time_batch).reshape(-1, 1)

        # Scale regression targets
        if self.scalers:
            if 'magnitude' in self.scalers:
                y_mag_batch = self.scalers['magnitude'].transform(y_mag_batch)
            if 'latitude' in self.scalers:
                y_lat_batch = self.scalers['latitude'].transform(y_lat_batch)
            if 'longitude' in self.scalers:
                y_lon_batch = self.scalers['longitude'].transform(y_lon_batch)
            if 'time_delta' in self.scalers:
                y_time_batch = self.scalers['time_delta'].transform(y_time_batch)

        return (
            X_batch,
            {
                'event_occurred': y_class_batch,
                'magnitude': y_mag_batch,
                'location_lat': y_lat_batch,
                'location_lon': y_lon_batch,
                'time_delta': y_time_batch,
            }
        )

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indices)
