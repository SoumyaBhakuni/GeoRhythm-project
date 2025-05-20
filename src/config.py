# src/config.py

# === MongoDB Configuration ===
MONGO_URI = "mongodb+srv://soumyabhakuni2005:UhEfvYDzIkmvhnSm@georhythm.q3cv8p0.mongodb.net/?retryWrites=true&w=majority&appName=GeoRhythm"
DB_NAME = "earthquakes"
COLLECTION_NAME = "events"

# === Model Training Configuration ===
SEQ_LENGTH = 30              # Number of past records to form one sequence
TRAIN_TEST_SPLIT = 0.8            # 80% training, 20% testing
PREDICTION_WINDOW_HOURS = 24      # For binary occurrence classification
MAGNITUDE_THRESHOLDS = [4.0, 6.0] # For classifying magnitude into low, moderate, high

# === Paths ===
DATA_PATH = "data/earthquakes_master.json"

# Preprocessed sequences will be stored here
CHUNK_OUTPUT_DIR = "outputs/processed/"

# Model and logs
MODEL_DIR = "outputs/models/"
LOG_DIR = "outputs/logs/"
PLOT_DIR = "outputs/plots/"

# Model + Scaler
MODEL_PATH = f"{MODEL_DIR}seismic_hybrid_model.h5"
SCALER_PATH = f"{MODEL_DIR}hybrid_scaler.pkl"

# PostgreSQL credentials
PG_CONN_STR = "postgresql://neondb_owner:npg_PWdAUj7thi4w@ep-long-wildflower-a4nkjfc2-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

CHUNK_SIZE = 10000