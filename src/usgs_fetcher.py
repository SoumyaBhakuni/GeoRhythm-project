import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_usgs_last_month():
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    url = (
        f"https://earthquake.usgs.gov/fdsnws/event/1/query"
        f"?format=geojson&starttime={start_date.date()}&endtime={end_date.date()}&minmagnitude=1"
    )

    response = requests.get(url)
    data = response.json()

    records = []
    for feature in data["features"]:
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]
        records.append({
            "time": datetime.utcfromtimestamp(props["time"] / 1000),
            "latitude": coords[1],
            "longitude": coords[0],
            "depth": coords[2],
            "mag": props.get("mag", 0),
            "place": props.get("place", "")
        })

    df = pd.DataFrame(records)
    df = df.sort_values("time").reset_index(drop=True)
    return df.to_dict(orient="records")
