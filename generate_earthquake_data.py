# generate_dummy_earthquakes.py

import json
import random
from datetime import datetime, timedelta
from tqdm import tqdm

def generate_dummy_earthquake():
    """Generate one dummy earthquake record."""
    return {
        "timestamp": (datetime(2000, 1, 1) + timedelta(seconds=random.randint(0, 25 * 365 * 24 * 3600))).isoformat(),
        "latitude": round(random.uniform(-90.0, 90.0), 4),
        "longitude": round(random.uniform(-180.0, 180.0), 4),
        "depth_km": round(random.uniform(0.0, 700.0), 1),
        "magnitude": round(random.uniform(1.0, 9.5), 2)
    }

def generate_dataset(n=10000, output_path="data/dummy_earthquakes.json"):
    data = [generate_dummy_earthquake() for _ in tqdm(range(n), desc="🔧 Generating dummy data")]
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n✅ Generated {n} dummy earthquake records and saved to '{output_path}'")

if __name__ == "__main__":
    generate_dataset()
