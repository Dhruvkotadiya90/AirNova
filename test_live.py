from live_data import get_live_data


data, forecast = get_live_data(
    28.6139,
    77.2090
)

print("\nAIRNOVA LIVE DATA")
print("------------------")

for key, value in data.items():
    print(f"{key}: {value}")

print("\nAIRNOVA 72-HOUR FORECAST")
print("------------------------")

for i in range(5):
    print(
        forecast["time"][i],
        "| PM2.5:",
        forecast["pm25"][i],
        "| PM10:",
        forecast["pm10"][i],
        "| Temp:",
        forecast["temperature"][i]
    )

print("\nTotal forecast hours:", len(forecast["time"]))