from pymongo import MongoClient, UpdateOne
from tqdm import tqdm

# MongoDB Atlas URI
MONGO_URI = "mongodb+srv://soumyabhakuni456:soumya@cluster-georhytm.vv79ifq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-GeoRhytm"

# Source DBs and collections
SOURCE_DB_COLLECTIONS = [
    ("earthquake_db", "events"),
    ("earthquakes_db", "all_quakes"),
]

# Final merged database and collection
TARGET_DB_NAME = "earthquake_db"
TARGET_COLLECTION_NAME = "merged_events"

# Connect to client
client = MongoClient(MONGO_URI)

# Create target collection
target_db = client[TARGET_DB_NAME]
target_collection = target_db[TARGET_COLLECTION_NAME]

# Create unique compound index for deduplication
target_collection.create_index(
    [("time", 1), ("latitude", 1), ("longitude", 1), ("depth", 1)],
    unique=True
)

merged_count = 0
total_duplicates = 0
batch_size = 1000

for db_name, collection_name in SOURCE_DB_COLLECTIONS:
    source = client[db_name][collection_name]
    total_docs = source.count_documents({})
    print(f"📦 Merging from `{db_name}.{collection_name}` ({total_docs} docs)...")

    cursor = source.find({}, no_cursor_timeout=True).batch_size(batch_size)
    batch = []

    for doc in tqdm(cursor, total=total_docs):
        doc.pop("_id", None)

        # Extract unique fields
        time = doc.get("time")
        latitude = doc.get("latitude")
        longitude = doc.get("longitude")
        depth = doc.get("depth")

        if not all([time, latitude, longitude, depth]):
            continue  # Skip incomplete records

        query = {
            "time": time,
            "latitude": latitude,
            "longitude": longitude,
            "depth": depth
        }

        batch.append(UpdateOne(query, {"$setOnInsert": doc}, upsert=True))

        if len(batch) >= batch_size:
            result = target_collection.bulk_write(batch, ordered=False)
            merged_count += result.upserted_count
            total_duplicates += len(batch) - result.upserted_count
            batch = []

    if batch:
        result = target_collection.bulk_write(batch, ordered=False)
        merged_count += result.upserted_count
        total_duplicates += len(batch) - result.upserted_count

    cursor.close()

print(f"\n✅ Merge complete: {merged_count} new docs inserted.")
print(f"⚠️ Duplicates skipped: {total_duplicates}")
print(f"🎉 All records now reside in `{TARGET_DB_NAME}.{TARGET_COLLECTION_NAME}`")

client.close()
