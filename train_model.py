import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Load dataset
data = pd.read_csv("data/airnova_data.csv")

features = [
    "temperature",
    "humidity",
    "wind_speed",
    "pbl_height",
    "pm25",
    "pm10",
    "o3",
    "no2",
    "stubble_activity"
]

X = data[features]
y = data["aqi"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Test
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("Model Training Complete")
print("-----------------------")
print("MAE:", round(mae, 2))
print("R² Score:", round(r2, 2))

# Save model
joblib.dump(model, "models/aq_model.pkl")

print("Model saved successfully!")