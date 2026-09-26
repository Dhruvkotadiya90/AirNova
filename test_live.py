from live_data import get_live_data

data = get_live_data(
    28.6139,
    77.2090
)

print("\nAIRNOVA LIVE DATA")
print("------------------")

for key, value in data.items():
    print(f"{key}: {value}")