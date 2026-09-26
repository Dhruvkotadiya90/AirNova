import pandas as pd
import numpy as np


def load_locations():

    locations = pd.read_csv(
        "data/locations.csv"
    )

    return locations


def generate_location_aqi(locations):

    np.random.seed(42)

    locations = locations.copy()

    locations["AQI"] = np.random.randint(
        50,
        350,
        len(locations)
    )

    return locations


def get_aqi_category(aqi):

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