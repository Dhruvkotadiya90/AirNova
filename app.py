import streamlit as st
from live_data import get_live_data

import folium
from streamlit_folium import st_folium

import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

from map_data import load_locations


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
    "prototype for Delhi NCR and selected Indian cities."
)

st.divider()


# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.header("🌍 AirNova Controls")

locations = load_locations()

location = st.sidebar.selectbox(
    "📍 Select Location",
    locations["location"].tolist()
)

hours = st.sidebar.slider(
    "Forecast Horizon",
    min_value=24,
    max_value=72,
    value=72
)


# -----------------------------
# SELECT LOCATION
# -----------------------------

selected_location = locations[
    locations["location"] == location
].iloc[0]

latitude = selected_location["latitude"]
longitude = selected_location["longitude"]


# -----------------------------
# GET LIVE DATA
# -----------------------------

try:

    current_data, forecast_data = get_live_data(
        latitude,
        longitude
    )

except Exception as e:

    st.error(
        "Unable to retrieve live environmental data."
    )

    st.stop()


# -----------------------------
# CURRENT VALUES
# -----------------------------

temperature = current_data["temperature"]
humidity = current_data["humidity"]
wind_speed = current_data["wind_speed"]
wind_direction = current_data["wind_direction"]

pm25 = current_data["pm25"]
pm10 = current_data["pm10"]
o3 = current_data["o3"]
no2 = current_data["no2"]

pbl_height = current_data["pbl_height"]


# -----------------------------
# CURRENT CONDITIONS
# -----------------------------

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
# MODEL INPUT
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

    # Future upgrade:
    # NASA FIRMS / regional fire activity
    "stubble_activity": [0.0]

})


# -----------------------------
# CURRENT AQI
# -----------------------------

current_aqi = model.predict(
    input_data
)[0]


st.header("🌫️ Current AQI")

st.metric(
    "Predicted AQI",
    f"{current_aqi:.0f}"
)


# -----------------------------
# AQI CATEGORY
# -----------------------------

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


category = aqi_category(
    current_aqi
)

st.info(
    f"Air Quality Category: **{category}**"
)


# -----------------------------
# 72-HOUR PROTOTYPE FORECAST
# -----------------------------

st.header("📈 72-Hour AQI Forecast")

forecast_hours = np.arange(
    1,
    hours + 1
)

forecast_values = []


for h in forecast_hours:

    future_input = input_data.copy()

    # Prototype simulation
    future_input["temperature"] += (
        np.sin(h / 12)
    )

    future_input["humidity"] += (
        np.sin(h / 8) * 2
    )

    future_input["wind_speed"] += (
        np.sin(h / 10) * 0.5
    )

    future_input["pbl_height"] += (
        np.sin(h / 15) * 50
    )

    prediction = model.predict(
        future_input
    )[0]

    forecast_values.append(
        prediction
    )


# -----------------------------
# AQI GRAPH
# -----------------------------

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=forecast_hours,
        y=forecast_values,
        mode="lines+markers",
        name="Predicted AQI"
    )
)

fig.update_layout(

    xaxis_title="Forecast Hour",

    yaxis_title="AQI",

    title=(
        f"AirNova {hours}-Hour AQI Forecast"
    ),

    hovermode="x unified"

)


st.plotly_chart(
    fig,
    width="stretch"
)


# -----------------------------
# POLLUTANT LEVELS
# -----------------------------

st.header("🧪 Current Pollutant Levels")

pollutants = pd.DataFrame({

    "Pollutant": [
        "PM2.5",
        "PM10",
        "O₃",
        "NO₂"
    ],

    "Value": [
        pm25,
        pm10,
        o3,
        no2
    ]

})


st.bar_chart(
    pollutants.set_index(
        "Pollutant"
    )
)


# -----------------------------
# ATMOSPHERIC CONDITIONS
# -----------------------------

st.header("🌬️ Atmospheric Conditions")

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "PBL Height",
    f"{pbl_height:.0f} m"
)


col2.metric(
    "Wind",
    f"{wind_speed:.1f} km/h"
)


col3.metric(
    "Wind Direction",
    f"{wind_direction:.0f}°"
)


col4.metric(
    "Humidity",
    f"{humidity:.0f}%"
)


st.info(
    "AirNova considers meteorological conditions such as "
    "wind speed, humidity and planetary boundary layer height "
    "when estimating air-quality conditions."
)


st.divider()


# -----------------------------
# MULTI-LOCATION MAP
# -----------------------------

st.header("🗺️ AirNova Multi-Location Map")

st.write(
    "Selected monitoring locations are displayed below. "
    "The current prototype focuses on the selected location's "
    "live environmental conditions."
)


m = folium.Map(

    location=[
        23.5,
        78.9
    ],

    zoom_start=5,

    tiles="OpenStreetMap"

)


# Add locations to map

for _, row in locations.iterrows():

    is_selected = (
        row["location"] == location
    )

    popup_text = f"""
    <b>{row['location']}</b><br>
    Latitude: {row['latitude']}<br>
    Longitude: {row['longitude']}
    """

    folium.CircleMarker(

        location=[
            row["latitude"],
            row["longitude"]
        ],

        radius=12 if is_selected else 8,

        color="red" if is_selected else "blue",

        fill=True,

        fill_color=(
            "red"
            if is_selected
            else "blue"
        ),

        fill_opacity=0.8,

        popup=popup_text,

        tooltip=row["location"]

    ).add_to(m)


st_folium(

    m,

    width=1200,

    height=600

)


# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.caption(
    "AirNova Prototype | Weather–Pollution Coupled Forecasting"
)

st.caption(
    "Environmental data: Open-Meteo API | "
    "AQI estimation: AirNova Machine Learning Model"
)