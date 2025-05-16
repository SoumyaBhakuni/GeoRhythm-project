# src/fetch_from_mongo.py

import random
from pymongo import MongoClient
import pandas as pd
from src.config import MONGO_URI, DB_NAME, COLLECTION_NAME, SEQ_LENGTH

# 🔗 Initialize MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def fetch_in_chunks(batch_size=10000):
    """
    Generator that yields data in chunks from MongoDB.
    Useful for processing large datasets without loading all data into memory.
    """
    skip = 0
    while True:
        cursor = collection.find().skip(skip).limit(batch_size)
        data = list(cursor)
        if not data:
            break
        df = pd.DataFrame(data)
        if "_id" in df.columns:
            df.drop(columns=["_id"], inplace=True)
        yield df
        skip += batch_size

def fetch_earthquake_data(limit=None):
    """
    Fetch all or limited earthquake data from MongoDB as a DataFrame.
    """
    try:
        print("🔗 Connecting to MongoDB...")
        print("📦 Fetching data from MongoDB collection...")

        projection = {
            '_id': 0,
            'timestamp': 1,
            'latitude': 1,
            'longitude': 1,
            'depth_km': 1,
            'magnitude': 1
        }

        cursor = collection.find({}, projection)
        if limit:
            cursor = cursor.limit(limit)

        data = list(cursor)
        if not data:
            print("⚠️ No data found in the MongoDB collection.")
            return pd.DataFrame()

        df = pd.DataFrame(data)
        print(f"✅ Retrieved {len(df)} earthquake records.")
        return df

    except Exception as e:
        print(f"❌ Error fetching data from MongoDB: {e}")
        return pd.DataFrame()

def fetch_latest_sequence(n=SEQ_LENGTH):
    """
    Fetch the latest N records sorted by timestamp (descending),
    then return them in chronological order for prediction.
    """
    projection = {
        '_id': 0,
        'timestamp': 1,
        'latitude': 1,
        'longitude': 1,
        'depth_km': 1,
        'magnitude': 1
    }

    cursor = collection.find({}, projection).sort("timestamp", -1).limit(n)
    data = list(cursor)
    if not data or len(data) < n:
        raise ValueError(f"⚠️ Not enough recent data available. Required: {n}, Found: {len(data)}")
    
    df = pd.DataFrame(data)
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df.to_dict(orient="records")

def fetch_random_sequence(n=SEQ_LENGTH):
    """
    Fetch a random sequence of N records from the collection,
    sorted chronologically.
    """
    total_docs = collection.count_documents({})
    if total_docs < n:
        raise ValueError(f"⚠️ Not enough data to fetch random sequence of {n}. Available: {total_docs}")
    
    start_index = random.randint(0, total_docs - n)
    projection = {
        '_id': 0,
        'timestamp': 1,
        'latitude': 1,
        'longitude': 1,
        'depth_km': 1,
        'magnitude': 1
    }

    cursor = collection.find({}, projection).skip(start_index).limit(n)
    data = list(cursor)
    df = pd.DataFrame(data)
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df.to_dict(orient="records")

if __name__ == "__main__":
    df = fetch_earthquake_data(limit=5)
    print(df)
