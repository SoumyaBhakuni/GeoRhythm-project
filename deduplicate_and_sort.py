from pymongo import MongoClient
from collections import defaultdict
from tqdm import tqdm

# MongoDB connection details
MONGO_URI = "mongodb+srv://soumyabhakuni2005:UhEfvYDzIkmvhnSm@georhythm.q3cv8p0.mongodb.net/?retryWrites=true&w=majority&appName=GeoRhythm"
DB_NAME = "earthquakes"
COLLECTION_NAME = "events"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

print("📊 Checking for duplicate documents by 'id'...")

# Step 1: Detect and remove duplicates (based on 'id')
id_map = defaultdict(list)
for doc in tqdm(collection.find({}, {"_id": 1, "id": 1}), total=collection.count_documents({})):
    if "id" in doc:
        id_map[doc["id"]].append(doc["_id"])

duplicates_removed = 0
for ids in id_map.values():
    if len(ids) > 1:
        # Keep the first, remove the rest
        collection.delete_many({"_id": {"$in": ids[1:]}})
        duplicates_removed += len(ids) - 1

print(f"✅ Removed {duplicates_removed} duplicate documents.")

# Step 2: Read and sort documents by 'timestamp'
print("📥 Sorting remaining documents by 'timestamp'...")

docs_sorted = collection.find().sort("timestamp", 1)

# Step 3: Backup + overwrite original collection
print("⚠️ Overwriting the original 'events' collection...")

# Backup the original collection just in case
collection.rename("events_backup", dropTarget=True)

# Create a new clean 'events' collection
cleaned_collection = db[COLLECTION_NAME]
batch = []
for doc in tqdm(docs_sorted, total=db["events_backup"].count_documents({})):
    doc.pop("_id", None)  # Let MongoDB assign a new unique _id
    batch.append(doc)
    if len(batch) >= 1000:
        cleaned_collection.insert_many(batch)
        batch = []
if batch:
    cleaned_collection.insert_many(batch)

print("🎉 Success: 'events' collection is now deduplicated and time-sorted!")

client.close()
