from .preprocessor_pg import preprocess_large_dataset_postgres
from .train_hybrid_pg import train_on_chunks

def main():
    print("🔹 Step 1: Running preprocessing (PostgreSQL chunked)...")
    # Run preprocessing that saves .npz chunk files in outputs/processed/
    preprocess_large_dataset_postgres()

    print("🔹 Step 2: Training model on preprocessed chunked data...")
    train_on_chunks(batch_size=64, validation_split=0.2, epochs=50)

if __name__ == "__main__":
    main()
