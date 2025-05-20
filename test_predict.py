import requests
import json
from datetime import datetime, timezone, timedelta

# Your raw data pasted here (only a few entries shown for example)
raw_data = [
{
    "timestamp": -2017675022960,
    "latitude": 50.088,
    "longitude": -125.314,
    "depth_km": 15.0,
    "magnitude": 6.45,
    "magnitude_type": "mw",
    "net": "iscgem",
    "id": "iscgem610548623",
    "last_updated": 1650919194095,
    "location": "9 km NNW of Campbell River, Canada",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2017908626430,
    "latitude": 34.175,
    "longitude": 138.025,
    "depth_km": 300.0,
    "magnitude": 7.4,
    "magnitude_type": "mw",
    "net": "iscgem",
    "id": "iscgem16957883",
    "last_updated": 1650918275887,
    "location": "50 km SSW of ?yama, Japan",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2018912114430,
    "latitude": 49.256,
    "longitude": 18.421,
    "depth_km": 15.0,
    "magnitude": 5.63,
    "magnitude_type": "mw",
    "net": "iscgem",
    "id": "iscgem610326302",
    "last_updated": 1650918999809,
    "location": "10 km WNW of Byt?a, Slovakia",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2019176906780,
    "latitude": 53.418,
    "longitude": 170.1,
    "depth_km": 35.0,
    "magnitude": 6.58,
    "magnitude_type": "mw",
    "net": "iscgem",
    "id": "iscgem610548622",
    "last_updated": 1650919187898,
    "location": "216 km WNW of Attu Station, Alaska",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2019584012750,
    "latitude": 45.386,
    "longitude": 16.521,
    "depth_km": 15.0,
    "magnitude": 5.79,
    "magnitude_type": "mw",
    "net": "iscgem",
    "id": "iscgem610326299",
    "last_updated": 1650918994425,
    "location": "4 km WNW of Sunja, Croatia",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2020383420000,
    "latitude": 35.3,
    "longitude": -118.8,
    "depth_km": 0.0,
    "magnitude": 5.8,
    "magnitude_type": "ml",
    "net": "ushis",
    "id": "ushis445",
    "last_updated": 1721781674881,
    "location": "Near Bakersfield, California",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2020962567790,
    "latitude": 18.32,
    "longitude": -108.557,
    "depth_km": 10.0,
    "magnitude": 6.96,
    "magnitude_type": "mw",
    "net": "iscgemsup",
    "id": "iscgemsup16957881",
    "last_updated": 1652109038461,
    "location": "Revilla Gigedo Islands region",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2021521801110,
    "latitude": 13.445,
    "longitude": 125.858,
    "depth_km": 15.0,
    "magnitude": 6.8,
    "magnitude_type": "mw",
    "net": "iscgem",
    "id": "iscgem610548621",
    "last_updated": 1650919186303,
    "location": "123 km NE of Cabatuan, Philippines",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2021541896370,
    "latitude": 51.247,
    "longitude": -176.193,
    "depth_km": 35.0,
    "magnitude": 6.71,
    "magnitude_type": "mw",
    "net": "iscgem",
    "id": "iscgem16957880",
    "last_updated": 1721778870117,
    "location": "76 km SSE of Adak, Alaska",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2022061192040,
    "latitude": 37.216,
    "longitude": 38.83,
    "depth_km": 15.0,
    "magnitude": 5.56,
    "magnitude_type": "mw",
    "net": "iscgem",
    "id": "iscgem16957879",
    "last_updated": 1650918272586,
    "location": "6 km NNE of ?anl?urfa, Turkey",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2022080069450,
    "latitude": 38.153,
    "longitude": 38.645,
    "depth_km": 10.0,
    "magnitude": 6.8,
    "magnitude_type": "mw",
    "net": "iscgemsup",
    "id": "iscgemsup603952288",
    "last_updated": 1652109544842,
    "location": "13 km NNE of Sincik, Turkey",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2022772079610,
    "latitude": 41.159,
    "longitude": 14.847,
    "depth_km": 15.0,
    "magnitude": 5.2,
    "magnitude_type": "mw",
    "net": "iscgemsup",
    "id": "iscgemsup610548620",
    "last_updated": 1740792415506,
    "location": "3 km WSW of Paduli, Italy",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2023486800000,
    "latitude": 40.932,
    "longitude": 22.241,
    "depth_km": 15.0,
    "magnitude": 5.45,
    "magnitude_type": "mw",
    "net": "iscgemsup",
    "id": "iscgemsup610548618",
    "last_updated": 1652109812678,
    "location": "8 km NNE of M\u00e1ndalo, Greece",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2024015640000,
    "latitude": 42.9,
    "longitude": -114.5,
    "depth_km": 0.0,
    "magnitude": 5.5,
    "magnitude_type": "mfa",
    "net": "uu",
    "id": "uu19051111212600000",
    "last_updated": 1721603454522,
    "location": "Near Shoshone, Idaho",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2024196831290,
    "latitude": 40.037,
    "longitude": 24.078,
    "depth_km": 15.0,
    "magnitude": 5.28,
    "magnitude_type": "mw",
    "net": "iscgemsup",
    "id": "iscgemsup610548617",
    "last_updated": 1652109811167,
    "location": "10 km SE of S\u00e1rti, Greece",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2024272428160,
    "latitude": 40.092,
    "longitude": 24.627,
    "depth_km": 15.0,
    "magnitude": 7.24,
    "magnitude_type": "mw",
    "net": "iscgem",
    "id": "iscgem16957878",
    "last_updated": 1650918270989,
    "location": "Aegean Sea",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2025634415370,
    "latitude": 34.339,
    "longitude": 138.846,
    "depth_km": 15.0,
    "magnitude": 7.2,
    "magnitude_type": "ms",
    "net": "iscgemsup",
    "id": "iscgemsup16957876",
    "last_updated": 1740791400043,
    "location": "38 km SSW of Shimoda, Japan",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2025806728290,
    "latitude": 40.761,
    "longitude": 28.183,
    "depth_km": 15.0,
    "magnitude": 5.78,
    "magnitude_type": "mw",
    "net": "iscgemsup",
    "id": "iscgemsup610548615",
    "last_updated": 1652109809292,
    "location": "30 km SE of Marmara Ere?lisi, Turkey",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2025867512770,
    "latitude": 43.096,
    "longitude": 41.664,
    "depth_km": 15.0,
    "magnitude": 6.37,
    "magnitude_type": "mw",
    "net": "iscgemsup",
    "id": "iscgemsup16957875",
    "last_updated": 1652109035433,
    "location": "28 km N of Tqvarch'eli, Georgia",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2026347467330,
    "latitude": 18.989,
    "longitude": -77.755,
    "depth_km": 15.0,
    "magnitude": 6.33,
    "magnitude_type": "mw",
    "net": "iscgem",
    "id": "iscgem610548613",
    "last_updated": 1650919185301,
    "location": "55 km N of Falmouth, Jamaica",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2027003542770,
    "latitude": 42.461,
    "longitude": 23.143,
    "depth_km": 15.0,
    "magnitude": 6.12,
    "magnitude_type": "mw",
    "net": "iscgem",
    "id": "iscgem610326295",
    "last_updated": 1650918991775,
    "location": "15 km NE of Bobov Dol, Bulgaria",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2027765271110,
    "latitude": -8.277,
    "longitude": 127.465,
    "depth_km": 35.0,
    "magnitude": 7.16,
    "magnitude_type": "mw",
    "net": "iscgem",
    "id": "iscgem16957874",
    "last_updated": 1650918265349,
    "location": "58 km ENE of Lospalos, Timor Leste",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2028062040430,
    "latitude": 28.784,
    "longitude": 75.157,
    "depth_km": 20.0,
    "magnitude": 6.9,
    "magnitude_type": "ms",
    "net": "iscgemsup",
    "id": "iscgemsup16957873",
    "last_updated": 1740791476095,
    "location": "17 km NE of Taranagar, India",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2028995859040,
    "latitude": 55.751,
    "longitude": 163.952,
    "depth_km": 15.0,
    "magnitude": 7.84,
    "magnitude_type": "mw",
    "net": "iscgem",
    "id": "iscgem16957872",
    "last_updated": 1721594139201,
    "location": "off the east coast of the Kamchatka Peninsula, Russia",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2029033099360,
    "latitude": 50.462,
    "longitude": -179.492,
    "depth_km": 15.0,
    "magnitude": 6.71,
    "magnitude_type": "mw",
    "net": "iscgem",
    "id": "iscgem610548612",
    "last_updated": 1732670292315,
    "location": "254 km SW of Adak, Alaska",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2029616217590,
    "latitude": 38.636,
    "longitude": 15.784,
    "depth_km": 15.0,
    "magnitude": 7.19,
    "magnitude_type": "mw",
    "net": "iscgem",
    "id": "iscgem16957871",
    "last_updated": 1650918258050,
    "location": "5 km W of San Nicol\u00f2, Italy",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2030217257920,
    "latitude": 45.309,
    "longitude": 142.089,
    "depth_km": 255.0,
    "magnitude": 7.3,
    "magnitude_type": "mB",
    "net": "iscgemsup",
    "id": "iscgemsup16957870",
    "last_updated": 1741132211552,
    "location": "22 km ESE of Makubetsu, Japan",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2030757547000,
    "latitude": 41.981,
    "longitude": 13.776,
    "depth_km": 15.0,
    "magnitude": 5.21,
    "magnitude_type": "mw",
    "net": "iscgemsup",
    "id": "iscgemsup610326411",
    "last_updated": 1652109592589,
    "location": "southern Italy",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2030796797120,
    "latitude": 42.921,
    "longitude": 129.907,
    "depth_km": 470.0,
    "magnitude": 6.6,
    "magnitude_type": "mB",
    "net": "iscgemsup",
    "id": "iscgemsup914296",
    "last_updated": 1740618421083,
    "location": "5 km SE of Namyang, North Korea",
    "event_type": "earthquake"
  },
  {
    "timestamp": -2031072720000,
    "latitude": 37.56,
    "longitude": -89.62,
    "depth_km": 0.0,
    "magnitude": 4.6,
    "magnitude_type": "mfa",
    "net": "official",
    "id": "official19050822050800000",
    "last_updated": 1723676256000,
    "location": "Ste. Genevieve Fault Zone, Missouri",
    "event_type": "earthquake"
  }
]

def convert_timestamp(ts_ms):
    # Convert milliseconds since epoch (can be negative) to ISO 8601 string
    # Negative means before 1970, so datetime can handle it by timedelta from epoch
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    dt = epoch + timedelta(milliseconds=ts_ms)
    return dt.isoformat()

# Prepare sequence data for the model
sequence = []
for entry in raw_data:
    # If depth_km is None, replace with 0.0 or a default value
    depth = entry.get("depth_km") if entry.get("depth_km") is not None else 0.0
    event = {
        "time": convert_timestamp(entry["timestamp"]),
        "latitude": entry["latitude"],
        "longitude": entry["longitude"],
        "depth": depth,
        "mag": entry["magnitude"],
    }
    sequence.append(event)

# Now send to your API
url = "http://127.0.0.1:5000/predict"
headers = {"Content-Type": "application/json"}
response = requests.post(url, json=sequence, headers=headers)

print("Status code:", response.status_code)
print("Response JSON:", response.json())
