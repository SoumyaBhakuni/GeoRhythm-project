# 🌍 GeoRhythm: A Hybrid AI Model for Seismic Event Detection and Prediction

## 📌 Overview

**GeoRhythm** is an AI-powered seismic event prediction system that uses a hybrid **CNN + LSTM** deep learning architecture to predict:

- 🟢 **Occurrence** (Will an earthquake happen?)
- 📈 **Magnitude** (How strong will it be?)
- 📍 **Location** (Where will it strike?)
- ⏰ **Time** (When might it occur?)

Designed for both real-time alerts and historical analysis, GeoRhythm combines scalable backend logic, intuitive UI, and a powerful prediction engine.



## 🎯 Objectives

GeoRhythm is built to:

- Predict seismic event **occurrence**
- Estimate earthquake **magnitude**
- Forecast **location** (latitude and longitude)
- Approximate **timing** of the event

> **Example Output:**  
> “An earthquake of ~6.2 magnitude is likely to occur near 38.7°N, 122.3°W around June 20, 2025 ± 3 days.”



## 📊 Data Sources

- 🌐 **Real-Time:** [USGS Earthquake API](https://earthquake.usgs.gov)
- 🗃️ **Historical:** Dataset with 94,000+ events (1900–present, magnitude > 0)
- 🧠 **Storage:** MongoDB Atlas (normalized and indexed)

**Attributes:** timestamp, magnitude, depth, latitude, longitude, place



## 🧠 Model Architecture

| Layer        | Function                          |
|--------------|-----------------------------------|
| CNN          | Extracts spatial features         |
| LSTM         | Captures temporal dependencies    |
| Dense Layers | Outputs for multiple predictions  |

**Outputs:**
- Event occurrence (binary)
- Magnitude (regression)
- Latitude & Longitude (regression)
- Time estimate (delta-based)

**Training Details:**
- Sequence length: `SEQ_LENGTH=30`
- Loss Function: Multi-output (classification + regression)


## 🚀 Prediction Modes

| Mode            | Description                           | Use Case             |
|------------------|----------------------------------------|----------------------|
| **Real-Time**     | Pulls latest data from MongoDB        | Live alerting        |
| **Manual Input**  | Custom sequence input via UI          | Research & testing   |
| **Random Sample** | Random historic data from DB          | Demo & debug mode    |


📚 References

1.Bhakuni, S. et al. LSTM-Based Temporal Modeling for Accurate Seismic Event Detection, GEHU AI Conference, 2024.

2.Author, F. CNN-LSTM Hybrids for Spatiotemporal Forecasting, Journal of AI Research, 2023.

3.USGS API Documentation

4.OpenAI Seismic Modeling Research, 2023

5.Author, T. AI Applications in Natural Disaster Prediction, Springer, 2022

