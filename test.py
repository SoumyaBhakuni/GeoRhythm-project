from src.utils import load_scaler, load_keras_model
from src.inference import load_new_data, prepare_sequence
from src.config import SEQ_LENGTH
import numpy as np

MODEL_PATH = "outputs/models/seismic_hybrid_model.h5"
SCALER_PATH = "outputs/models/hybrid_scaler.pkl"
SAMPLE_FILE = "data/sample_input.json"

def test_model():
    print("🧪 Running test...")

    # Load model and scaler
    model = load_keras_model(MODEL_PATH)
    scaler = load_scaler(SCALER_PATH)

    # Load and prepare data
    raw_data = load_new_data(SAMPLE_FILE)
    X = prepare_sequence(raw_data, scaler, SEQ_LENGTH)

    # Predict
    print("🔮 Predicting...")
    y_class_prob, y_mag = model.predict(X)

    # Interpret results
    occurred = y_class_prob[0][0] > 0.5
    magnitude = y_mag[0][0]

    print("\n✅ Prediction Output:")
    print(f"  Will event occur? {'YES ✅' if occurred else 'NO ❌'}")
    print(f"  Predicted Magnitude: {magnitude:.2f}")

    # Simple assertions
    assert 0.0 <= y_class_prob[0][0] <= 1.0, "❌ Classification probability out of bounds"
    assert 0.0 <= magnitude <= 10.0, "❌ Magnitude looks unreasonable"

    print("🧪 Test passed successfully!")

if __name__ == "__main__":
    test_model()
