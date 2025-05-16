# upload_local_json_to_mongo.py

import json
import pymongo

MONGO_URI = "mongodb+srv://soumyabhakuni456:soumya@cluster-georhytm.vv79ifq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-GeoRhytm"
FILE_PATH = "data/earthquakes_master.json"

def main():
    client = pymongo.MongoClient(MONGO_URI)
    db = client["earthquake_db"]
    collection = db["events"]

    with open(FILE_PATH, 'r') as f:
        data = json.load(f)

    result = collection.insert_many(data)
    print(f"✅ Inserted {len(result.inserted_ids)} records into MongoDB.")

if __name__ == "__main__":
    main()
