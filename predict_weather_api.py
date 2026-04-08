import requests
import os
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from dotenv import load_dotenv

# ==========================
# 1️⃣ Konfigurasi
# ==========================
# Load file .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY") 
cities = ["Jakarta", "Bandung", "Tegal", "Surabaya", "Yogyakarta"]
csv_file = "data/weather_data.csv"
if not os.path.exists("data"):
    os.makedirs("data")

# ==========================
# 2️⃣ Ambil Data dari API (Extract)
# ==========================
for city in cities:
    # Ekstrak
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Transform
        transformed = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["main"],
            "timestamp": datetime.fromtimestamp(data["dt"])
        }

        # Load ke CSV
        # Jika file belum ada, buat header. Jika sudah ada, append data
        if not os.path.isfile(csv_file):
            pd.DataFrame([transformed]).to_csv(csv_file, mode="w", index=False)
        else:
            pd.DataFrame([transformed]).to_csv(csv_file, mode="a", header=False, index=False)

        print(f"{city}: Data berhasil disimpan ✅")
    else:
        print(f"{city}: Gagal ambil data ❌", response.status_code)

# ==========================
# 3️⃣ Load Data CSV & Feature Engineering
# ==========================
df = pd.read_csv(csv_file)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["hour"] = df["timestamp"].dt.hour
df["day"] = df["timestamp"].dt.day

# ==========================
# 4️⃣ Train Model & Prediksi per Kota
# ==========================
tomorrow = datetime.now() + timedelta(days=1)

for city in cities:
    df_city = df[df["city"] == city]
    
    # Pastikan ada cukup data
    if len(df_city) < 2:
        print(f"{city} - Data tidak cukup untuk prediksi")
        continue
    
    # Fitur dan target
    X = df_city[["humidity", "hour", "day"]]
    y = df_city["temperature"]

    # Linear Regression
    model = LinearRegression()
    model.fit(X, y)

    # Prediksi suhu besok jam 8 pagi
    X_pred = pd.DataFrame([[df_city["humidity"].mean(), 8, tomorrow.day]],
                          columns=["humidity", "hour", "day"])
    pred_temp = model.predict(X_pred)

    # Evaluasi model
    pred_train = model.predict(X)
    mse = mean_squared_error(y, pred_train)

    print(f"{city} - MSE Model: {mse:.2f}")
    print(f"{city} - Prediksi suhu besok jam 8 pagi: {pred_temp[0]:.2f}°C\n")