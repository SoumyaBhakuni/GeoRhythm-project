import random
import psycopg2
import pandas as pd
from src.config import PG_CONN_STR, SEQ_LENGTH

TABLE_NAME = "all_quakes"

def get_connection():
    return psycopg2.connect(PG_CONN_STR)

def fetch_in_chunks(batch_size=10000):
    """
    Generator that yields data in chunks from PostgreSQL using
    a timestamp cursor for better performance (avoids OFFSET).
    """
    last_timestamp = None
    while True:
        with get_connection() as conn:
            query = f"""
                SELECT timestamp, latitude, longitude, depth_km, magnitude
                FROM {TABLE_NAME}
                WHERE (%s IS NULL OR timestamp > %s)
                ORDER BY timestamp ASC
                LIMIT %s;
            """
            df = pd.read_sql(query, conn, params=(last_timestamp, last_timestamp, batch_size))
            if df.empty:
                break
            yield df
            last_timestamp = df["timestamp"].iloc[-1]

def fetch_earthquake_data(limit=None):
    """
    Fetch all or a limited number of earthquake records from PostgreSQL.
    """
    try:
        print("🔗 Connecting to PostgreSQL...")
        print("📦 Fetching data from table...")

        with get_connection() as conn:
            query = f"""
                SELECT timestamp, latitude, longitude, depth_km, magnitude
                FROM {TABLE_NAME}
                ORDER BY timestamp ASC
            """
            if limit:
                query += f" LIMIT {limit}"
            df = pd.read_sql(query, conn)

        if df.empty:
            print("⚠️ No data found.")
        else:
            print(f"✅ Retrieved {len(df)} records.")
        return df

    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return pd.DataFrame()

def fetch_latest_sequence(n=SEQ_LENGTH):
    """
    Fetch the latest N records and return in chronological order.
    """
    try:
        with get_connection() as conn:
            query = f"""
                SELECT timestamp, latitude, longitude, depth_km, magnitude
                FROM {TABLE_NAME}
                ORDER BY timestamp DESC
                LIMIT %s;
            """
            df = pd.read_sql(query, conn, params=(n,))

        if df.empty or len(df) < n:
            raise ValueError(f"⚠️ Not enough data. Required: {n}, Found: {len(df)}")

        return df.sort_values("timestamp").reset_index(drop=True).to_dict(orient="records")

    except Exception as e:
        print(f"❌ Error fetching latest sequence: {e}")
        return []

def fetch_random_sequence(n=SEQ_LENGTH):
    """
    Fetch a random sequence of N records (chronologically ordered).
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT COUNT(*) FROM {TABLE_NAME};")
                total_rows = cur.fetchone()[0]

        if total_rows < n:
            raise ValueError(f"⚠️ Not enough data for a random sequence of {n}. Available: {total_rows}")

        start_offset = random.randint(0, total_rows - n)

        with get_connection() as conn:
            query = f"""
                SELECT timestamp, latitude, longitude, depth_km, magnitude
                FROM {TABLE_NAME}
                ORDER BY timestamp ASC
                OFFSET %s LIMIT %s;
            """
            df = pd.read_sql(query, conn, params=(start_offset, n))

        return df.sort_values("timestamp").reset_index(drop=True).to_dict(orient="records")

    except Exception as e:
        print(f"❌ Error fetching random sequence: {e}")
        return []

if __name__ == "__main__":
    df = fetch_earthquake_data(limit=5)
    print(df)
