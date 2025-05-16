from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv1D, MaxPooling1D, LSTM, Dense, Dropout
from tensorflow.keras.losses import BinaryFocalCrossentropy
from tensorflow.keras.metrics import MeanAbsoluteError


def build_cnn_lstm_model(seq_length, feature_dim, lstm_units=64, dropout_rate=0.3):
    """
    Builds a hybrid CNN + LSTM model for seismic event prediction.

    Parameters:
        seq_length (int): Number of timesteps in each input sequence.
        feature_dim (int): Number of features per timestep.
        lstm_units (int): Number of units in the LSTM layer.
        dropout_rate (float): Dropout rate after LSTM.

    Returns:
        tf.keras.Model: Compiled multi-output model.
    """
    inputs = Input(shape=(seq_length, feature_dim), name='input_sequence')

    # CNN for local spatial patterns
    x = Conv1D(filters=64, kernel_size=3, activation='relu', padding='same')(inputs)
    x = MaxPooling1D(pool_size=2)(x)

    # LSTM for temporal sequence modeling
    x = LSTM(lstm_units, return_sequences=False)(x)
    x = Dropout(dropout_rate)(x)

    # Shared dense representation
    shared = Dense(64, activation='relu')(x)

    # Output 1: Classification (event occurrence)
    out_class = Dense(1, activation='sigmoid', name='event_occurred')(shared)

    # Output 2: Regression (magnitude)
    out_magnitude = Dense(1, activation='linear', name='magnitude')(shared)

    # Output 3 & 4: Regression (latitude and longitude)
    out_lat = Dense(1, activation='linear', name='location_lat')(shared)
    out_lon = Dense(1, activation='linear', name='location_lon')(shared)

    # Output 5: Regression (time until event in days)
    out_time = Dense(1, activation='linear', name='time_delta')(shared)

    # Define model
    model = Model(
        inputs=inputs,
        outputs=[out_class, out_magnitude, out_lat, out_lon, out_time],
        name="Hybrid_CNN_LSTM_Seismic_Model"
    )

    # Compile model
    model.compile(
        optimizer='adam',
        loss={
            'event_occurred': BinaryFocalCrossentropy(gamma=2.0),
            'magnitude': 'mae',
            'location_lat': 'mse',
            'location_lon': 'mse',
            'time_delta': 'mae'
        },
        metrics={
            'event_occurred': ['accuracy'],
            'magnitude': [MeanAbsoluteError(name='mae')],
            'location_lat': [MeanAbsoluteError(name='mae')],
            'location_lon': [MeanAbsoluteError(name='mae')],
            'time_delta': [MeanAbsoluteError(name='mae')]
        }
    )

    return model


if __name__ == "__main__":
    # Example summary for debug purposes
    model = build_cnn_lstm_model(seq_length=30, feature_dim=4)
    model.summary()
