import requests


def get_live_data(latitude, longitude):

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "wind_direction_10m"
        ),
        "hourly": "boundary_layer_height",
        "forecast_hours": 72,
        "timezone": "auto"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params,
        timeout=15
    )

    weather_response.raise_for_status()

    weather = weather_response.json()

    air_url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    air_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "pm10,"
            "pm2_5,"
            "ozone,"
            "nitrogen_dioxide"
        ),
        "hourly": (
            "pm10,"
            "pm2_5,"
            "ozone,"
            "nitrogen_dioxide"
        ),
        "forecast_hours": 72,
        "timezone": "auto"
    }

    air_response = requests.get(
        air_url,
        params=air_params,
        timeout=15
    )

    air_response.raise_for_status()

    air = air_response.json()

    current = {
        "temperature": weather["current"]["temperature_2m"],
        "humidity": weather["current"]["relative_humidity_2m"],
        "wind_speed": weather["current"]["wind_speed_10m"],
        "wind_direction": weather["current"]["wind_direction_10m"],

        "pm25": air["current"]["pm2_5"],
        "pm10": air["current"]["pm10"],
        "o3": air["current"]["ozone"],
        "no2": air["current"]["nitrogen_dioxide"],

        "pbl_height": weather["hourly"]["boundary_layer_height"][0]
    }

    return current