import os
import numpy as np
from tensorflow.keras.utils import Sequence

class SeismicDataGenerator(Sequence):
    def __init__(
        self,
        X=None, y_class=None, y_mag=None, y_lat=None, y_lon=None, y_time=None,
        chunk_dir=None, batch_size=64, shuffle=True
    ):
        self.in_memory_mode = X is not None
        self.batch_size = batch_size
        self.shuffle = shuffle

        if self.in_memory_mode:
            self.X = X
            self.y_class = y_class
            self.y_mag = y_mag
            self.y_lat = y_lat
            self.y_lon = y_lon
            self.y_time = y_time
            self.indices = np.arange(len(self.X))

        elif chunk_dir:
            self.chunk_dir = chunk_dir
            self.chunk_files = sorted([
                os.path.join(chunk_dir, f)
                for f in os.listdir(chunk_dir)
                if f.endswith(".npz")
            ])
            self._prepare_chunk_index()

        else:
            raise ValueError("Either in-memory arrays or chunk_dir must be provided.")

        self.on_epoch_end()

    def _prepare_chunk_index(self):
        """Prepare global index mapping from (chunk_idx, local_idx)."""
        self.global_index = []
        self.chunk_data_lengths = []

        for chunk_idx, file_path in enumerate(self.chunk_files):
            with np.load(file_path) as data:
                length = data['X'].shape[0]
                self.chunk_data_lengths.append(length)
                for local_idx in range(length):
                    self.global_index.append((chunk_idx, local_idx))

        self.indices = np.arange(len(self.global_index))

    def __len__(self):
        return int(np.ceil(len(self.indices) / self.batch_size))

    def __getitem__(self, index):
        if self.in_memory_mode:
            idxs = self.indices[index * self.batch_size:(index + 1) * self.batch_size]
            X_batch = self.X[idxs]
            y_batch = {
                'event_occurred': self.y_class[idxs],
                'magnitude': self.y_mag[idxs],
                'location_lat': self.y_lat[idxs],
                'location_lon': self.y_lon[idxs],
                'time_delta': self.y_time[idxs],
            }
            return X_batch, y_batch

        else:
            idxs = self.indices[index * self.batch_size:(index + 1) * self.batch_size]
            # Group by chunk index
            chunk_map = {}
            for global_idx in idxs:
                chunk_idx, local_idx = self.global_index[global_idx]
                if chunk_idx not in chunk_map:
                    chunk_map[chunk_idx] = []
                chunk_map[chunk_idx].append(local_idx)

            X_list, y_dict = [], {
                'event_occurred': [],
                'magnitude': [],
                'location_lat': [],
                'location_lon': [],
                'time_delta': [],
            }

            for chunk_idx, local_indices in chunk_map.items():
                with np.load(self.chunk_files[chunk_idx]) as data:
                    X_chunk = data['X'][local_indices]
                    X_list.append(X_chunk)
                    for key in y_dict:
                        y_dict[key].append(data[key.replace('event_occurred', 'y_class')
                                               .replace('magnitude', 'y_mag')
                                               .replace('location_lat', 'y_lat')
                                               .replace('location_lon', 'y_lon')
                                               .replace('time_delta', 'y_time')][local_indices])

            X_batch = np.concatenate(X_list)
            y_batch = {key: np.concatenate(y_dict[key]) for key in y_dict}

            return X_batch, y_batch

    def on_epoch_end(self):
        if self.shuffle:
            if self.in_memory_mode:
                np.random.shuffle(self.indices)
            else:
                np.random.shuffle(self.indices)
