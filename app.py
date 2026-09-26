import streamlit as st

from live_data import get_live_data

import folium

from streamlit_folium import st_folium

import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

from map_data import (
    load_locations,
    generate_location_aqi,
    get_aqi_category
)

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="AirNova",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# LOAD MODEL
# -----------------------------

model = joblib.load("models/aq_model.pkl")

# -----------------------------
# TITLE
# -----------------------------

st.title("🌍 AirNova")
st.subheader("72-Hour Air Quality Forecasting System")

st.write(
    "AI-powered weather and pollution coupled forecasting "
    "prototype for Delhi NCR."
)

st.divider()

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.header("🌍 AirNova Controls")

# Load available locations
locations = load_locations()

location = st.sidebar.selectbox(
    "📍 Select Location",
    locations["location"].tolist()
)

selected_location = locations[
    locations["location"] == location
].iloc[0]

latitude = selected_location["latitude"]
longitude = selected_location["longitude"]

live_data = get_live_data(
    latitude,
    longitude
)

st.sidebar.write("Forecast Horizon")

hours = st.sidebar.slider(
    "Hours",
    min_value=24,
    max_value=72,
    value=72
)
# -----------------------------
# CURRENT CONDITIONS
# -----------------------------

st.header("Current Conditions")

col1, col2, col3, col4 = st.columns(4)

temperature = live_data["temperature"]
humidity = live_data["humidity"]
wind_speed = live_data["wind_speed"]
pm25 = live_data["pm25"]

pm10 = live_data["pm10"]
o3 = live_data["o3"]
no2 = live_data["no2"]
pbl_height = live_data["pbl_height"]
wind_direction = live_data["wind_direction"]

st.header(f"📍 {location} — Live Conditions")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🌡️ Temperature",
    f"{temperature:.1f} °C"
)

col2.metric(
    "💧 Humidity",
    f"{humidity:.0f}%"
)

col3.metric(
    "💨 Wind Speed",
    f"{wind_speed:.1f} km/h"
)

col4.metric(
    "🌫️ PM2.5",
    f"{pm25:.1f} µg/m³"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🌫️ PM10",
    f"{pm10:.1f} µg/m³"
)

col2.metric(
    "🧪 O₃",
    f"{o3:.1f} µg/m³"
)

col3.metric(
    "🧪 NO₂",
    f"{no2:.1f} µg/m³"
)

col4.metric(
    "🌬️ PBL Height",
    f"{pbl_height:.0f} m"
)

st.divider()

# -----------------------------
# INPUT DATA
# -----------------------------

input_data = pd.DataFrame({
    "temperature": [temperature],
    "humidity": [humidity],
    "wind_speed": [wind_speed],
    "pbl_height": [pbl_height],
    "pm25": [pm25],
    "pm10": [pm10],
    "o3": [o3],
    "no2": [no2],
    "stubble_activity": [0.0]
})

# -----------------------------
# CURRENT AQI
# -----------------------------

current_aqi = model.predict(input_data)[0]

st.header("Current AQI")

st.metric(
    "Predicted AQI",
    f"{current_aqi:.0f}"
)

# -----------------------------
# AQI CATEGORY
# -----------------------------

def get_color(aqi):

    if aqi <= 50:
        return "green"

    elif aqi <= 100:
        return "lightgreen"

    elif aqi <= 200:
        return "orange"

    elif aqi <= 300:
        return "red"

    else:
        return "darkred"

def aqi_category(aqi):

    if aqi <= 50:
        return "Good"

    elif aqi <= 100:
        return "Satisfactory"

    elif aqi <= 200:
        return "Moderate"

    elif aqi <= 300:
        return "Poor"

    elif aqi <= 400:
        return "Very Poor"

    else:
        return "Severe"


category = aqi_category(current_aqi)

st.info(f"Air Quality Category: **{category}**")

# -----------------------------
# 72-HOUR FORECAST
# -----------------------------

st.header("📈 72-Hour AQI Forecast")

forecast_hours = np.arange(1, hours + 1)

forecast_values = []

for h in forecast_hours:

    future_input = input_data.copy()

    # Simulate changing weather conditions
    future_input["temperature"] += np.sin(h / 12)
    future_input["humidity"] += np.sin(h / 8) * 2

    future_input["wind_speed"] += (
        np.sin(h / 10) * 0.5
    )

    future_input["pbl_height"] += (
        np.sin(h / 15) * 50
    )

    prediction = model.predict(
        future_input
    )[0]

    forecast_values.append(prediction)

# -----------------------------
# GRAPH
# -----------------------------

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=forecast_hours,
        y=forecast_values,
        mode="lines+markers",
        name="AQI"
    )
)

fig.update_layout(
    xaxis_title="Forecast Hour",
    yaxis_title="AQI",
    title="AirNova 72-Hour AQI Forecast"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# -----------------------------
# POLLUTANTS
# -----------------------------

st.header("Pollutant Levels")

pollutants = pd.DataFrame({
    "Pollutant": [
        "PM2.5",
        "PM10",
        "O₃",
        "NO₂"
    ],

    "Value": [
        pm25,
        250,
        45,
        85
    ]
})

st.bar_chart(
    pollutants.set_index("Pollutant")
)

# -----------------------------
# ATMOSPHERIC CONDITIONS
# -----------------------------

st.header("🌬️ Atmospheric Conditions")

col1, col2, col3 = st.columns(3)

col1.metric(
    "PBL Height",
    "350 m"
)

col2.metric(
    "Wind",
    "2.5 m/s"
)

col3.metric(
    "Stubble Activity",
    "High"
)

st.warning(
    "⚠️ Low wind speed + low PBL height + "
    "high regional emission activity may increase "
    "pollutant accumulation."
)

st.divider()

st.caption(
    "AirNova Prototype | Weather–Pollution Coupled Forecasting"
)

# -----------------------------
# FOOTER
# -----------------------------

st.header("🗺️ AirNova Multi-Location AQI Map")

locations = load_locations()

locations = generate_location_aqi(
    locations
)

m = folium.Map(
    location=[23.5, 78.9],
    zoom_start=5,
    tiles="OpenStreetMap"
)

for _, row in locations.iterrows():

    aqi = row["AQI"]

    category = get_aqi_category(aqi)

    popup_text = f"""
    <b>{row['location']}</b><br>
    AQI: {aqi}<br>
    Category: {category}
    """

    folium.CircleMarker(
    location=[
        row["latitude"],
        row["longitude"]
    ],
    radius=12,
    color=get_color(aqi),
    fill=True,
    fill_color=get_color(aqi),
    fill_opacity=0.8,

    popup=popup_text,

    tooltip=(
        f"{row['location']} | "
        f"AQI: {aqi}"
    )
).add_to(m)

st_folium(
    m,
    width=1200,
    height=600
)