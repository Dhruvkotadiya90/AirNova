import pandas as pd
import numpy as np

np.random.seed(42)

n = 3000

data = pd.DataFrame({
    "temperature": np.random.uniform(8, 35, n),
    "humidity": np.random.uniform(30, 95, n),
    "wind_speed": np.random.uniform(0.5, 15, n),
    "pbl_height": np.random.uniform(100, 1500, n),
    "pm25": np.random.uniform(20, 350, n),
    "pm10": np.random.uniform(40, 500, n),
    "o3": np.random.uniform(10, 150, n),
    "no2": np.random.uniform(10, 200, n),
    "stubble_activity": np.random.uniform(0, 1, n)
})

# Synthetic AQI relationship for prototype demonstration
data["aqi"] = (
    data["pm25"] * 0.9 +
    data["pm10"] * 0.25 +
    data["no2"] * 0.15 +
    data["o3"] * 0.10 +
    data["humidity"] * 0.15 +
    data["stubble_activity"] * 100 -
    data["wind_speed"] * 5 -
    data["pbl_height"] * 0.03 +
    np.random.normal(0, 15, n)
)

data["aqi"] = data["aqi"].clip(lower=0)

data.to_csv("data/airnova_data.csv", index=False)

print("AirNova dataset created successfully!")