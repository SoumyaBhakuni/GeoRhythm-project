import os
import requests
from datetime import datetime, timedelta
from time import sleep
from pymongo import MongoClient
from tqdm import tqdm

# --- MongoDB Connection ---
MONGO_URI = "mongodb+srv://soumyabhakuni456:soumya@cluster-georhytm.vv79ifq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-GeoRhytm"
DB_NAME = "earthquakes_db"
COLLECTION_NAME = "all_quakes"

# --- USGS API ---
USGS_ENDPOINT = "https://earthquake.usgs.gov/fdsnws/event/1/query"
LIMIT = 20000

# --- Mongo Setup ---
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
collection.create_index("id", unique=True)


def fetch_usgs_data(starttime, endtime, offset):
    params = {
        "format": "geojson",
        "starttime": starttime,
        "endtime": endtime,
        "orderby": "time-asc",
        "limit": LIMIT,
        "offset": offset,
        "minmagnitude": 0.1
    }

    try:
        response = requests.get(USGS_ENDPOINT, params=params, timeout=30)
        if response.status_code == 200:
            return response.json().get("features", [])
        else:
            print(f"⚠️ API error: {response.status_code}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    return []


def format_event(event):
    props = event["properties"]
    geo = event["geometry"]["coordinates"]
    return {
        "timestamp": props["time"],
        "latitude": geo[1],
        "longitude": geo[0],
        "depth_km": geo[2],
        "magnitude": props.get("mag", 0.0),
        "magnitude_type": props.get("magType", "unknown"),
        "net": props.get("net", "unknown"),
        "id": event.get("id", ""),
        "last_updated": props.get("updated", 0),
        "location": props.get("place", "unknown"),
        "event_type": props.get("type", "earthquake")
    }


def daterange(start_year, end_year):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    while start_date <= end_date:
        next_month = start_date + timedelta(days=32)
        next_month = datetime(next_month.year, next_month.month, 1)
        yield start_date, min(next_month - timedelta(days=1), end_date)
        start_date = next_month


def main():
    current_year = datetime.utcnow().year
    print(f"📅 Fetching all events from 1900 to {current_year}...\n")

    for start, end in tqdm(list(daterange(1900, current_year))):
        start_str = start.strftime("%Y-%m-%d")
        end_str = end.strftime("%Y-%m-%d")

        print(f"📆 Fetching from {start_str} to {end_str}")
        offset = 1
        total_inserted = 0

        while True:
            events = fetch_usgs_data(start_str, end_str, offset)
            if not events:
                break

            formatted_batch = [format_event(e) for e in events]
            try:
                result = collection.insert_many(formatted_batch, ordered=False)
                total_inserted += len(result.inserted_ids)
            except Exception as e:
                print(f"⚠️ Insert error (likely due to duplicates): {e}")

            print(f"  ➕ Inserted {len(formatted_batch)} records (offset={offset})")
            offset += LIMIT
            sleep(0.3)  # Be polite to USGS

        print(f"✅ Month complete. Inserted total: {total_inserted}\n")

    print("🎉 All data fetched and stored in MongoDB.")


if __name__ == "__main__":
    main()
