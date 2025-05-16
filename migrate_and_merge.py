from pymongo import MongoClient, UpdateOne
from tqdm import tqdm
import hashlib

# MongoDB URIs
OLD_URI = "mongodb+srv://soumyabhakuni456:soumya@cluster-georhytm.vv79ifq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-GeoRhytm"
NEW_URI = "mongodb+srv://soumyabhakuni2005:UhEfvYDzIkmvhnSm@georhythm.q3cv8p0.mongodb.net/?retryWrites=true&w=majority&appName=GeoRhythm"

# Source details
SOURCE_DBS = [("earthquake_db", "events"), ("earthquakes_db", "all_quakes")]

# Target details
TARGET_DB = "earthquakes"
TARGET_COLLECTION = "events"

# Connect clients
old_client = MongoClient(OLD_URI)
new_client = MongoClient(NEW_URI)

target_col = new_client[TARGET_DB][TARGET_COLLECTION]
target_col.create_index("hash", unique=True)  # For deduplication

def generate_hash(doc):
    """
    Generate a unique hash from key earthquake properties.
    """
    fields = [str(doc.get("time")), str(doc.get("latitude")), str(doc.get("longitude")), str(doc.get("depth"))]
    return hashlib.md5("|".join(fields).encode()).hexdigest()

merged_count = 0
duplicates_skipped = 0
batch_size = 1000
seen_hashes = set()

for db_name, col_name in SOURCE_DBS:
    source_col = old_client[db_name][col_name]
    total_docs = source_col.count_documents({})
    print(f"📦 Reading from {db_name}.{col_name} ({total_docs} docs)...")

    cursor = source_col.find({}).batch_size(batch_size)
    batch = []

    for doc in tqdm(cursor, total=total_docs):
        doc.pop("_id", None)  # Remove MongoDB-specific ID
        doc_hash = generate_hash(doc)

        if doc_hash in seen_hashes:
            duplicates_skipped += 1
            continue

        doc["hash"] = doc_hash
        seen_hashes.add(doc_hash)

        batch.append(UpdateOne({"hash": doc_hash}, {"$setOnInsert": doc}, upsert=True))

        if len(batch) >= batch_size:
            result = target_col.bulk_write(batch, ordered=False)
            merged_count += result.upserted_count
            batch = []

    if batch:
        result = target_col.bulk_write(batch, ordered=False)
        merged_count += result.upserted_count

    cursor.close()

print(f"\n✅ Migration complete: {merged_count} new docs inserted into {TARGET_DB}.{TARGET_COLLECTION}.")
print(f"⚠️ Duplicates skipped: {duplicates_skipped}")

old_client.close()
new_client.close()
