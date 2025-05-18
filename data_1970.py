import os
import requests
from datetime import datetime, timedelta
from time import sleep
from tqdm import tqdm
import psycopg2
from psycopg2.extras import execute_batch

# --- PostgreSQL Connection (NeonDB URI) ---
PG_CONN_STR = "postgresql://neondb_owner:npg_PWdAUj7thi4w@ep-long-wildflower-a4nkjfc2-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"
conn = psycopg2.connect(PG_CONN_STR)
conn.autocommit = True
cur = conn.cursor()

TABLE_NAME = "all_quakes"

# --- USGS API ---
USGS_ENDPOINT = "https://earthquake.usgs.gov/fdsnws/event/1/query"
LIMIT = 20000

# --- PostgreSQL Setup ---
cur.execute(f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id TEXT PRIMARY KEY,
    timestamp BIGINT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    depth_km DOUBLE PRECISION,
    magnitude DOUBLE PRECISION,
    magnitude_type TEXT,
    net TEXT,
    last_updated BIGINT,
    location TEXT,
    event_type TEXT
);
""")


def fetch_usgs_data(starttime, endtime, offset):
    params = {
        "format": "geojson",
        "starttime": starttime,
        "endtime": endtime,
        "orderby": "time-asc",
        "limit": LIMIT,
        "offset": offset,
        "minmagnitude": -2.0  # Fetching all possible magnitudes
    }

    try:
        response = requests.get(USGS_ENDPOINT, params=params, timeout=30)
        if response.status_code == 200:
            return response.json().get("features", [])
        elif response.status_code == 429:
            print("⏳ Rate limited. Sleeping for 60 seconds...")
            sleep(60)
            return fetch_usgs_data(starttime, endtime, offset)
        else:
            print(f"⚠ API error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    return []


def format_event(event):
    props = event["properties"]
    geo = event["geometry"]["coordinates"]
    return (
        event.get("id", ""),
        props["time"],
        geo[1],
        geo[0],
        geo[2],
        props.get("mag", 0.0),
        props.get("magType", "unknown"),
        props.get("net", "unknown"),
        props.get("updated", 0),
        props.get("place", "unknown"),
        props.get("type", "earthquake")
    )


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
                execute_batch(cur,
                    f"""
                    INSERT INTO {TABLE_NAME} 
                    (id, timestamp, latitude, longitude, depth_km, magnitude, magnitude_type, net, last_updated, location, event_type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                    """,
                    formatted_batch
                )
                total_inserted += len(formatted_batch)
            except Exception as e:
                print(f"⚠ Insert error: {e}")

            print(f"  ➕ Inserted {len(formatted_batch)} records (offset={offset})")
            offset += LIMIT
            sleep(0.3)  # Be polite to USGS

        print(f"✅ Month complete. Inserted total: {total_inserted}\n")

    print("🎉 All data fetched and stored in neon.")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()