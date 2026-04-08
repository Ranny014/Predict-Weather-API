# 🌤 Weather Prediction with Linear Regression

[![Python Version](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is a **mini ETL + Machine Learning pipeline** to predict tomorrow's temperature at 8 AM for multiple cities using historical weather data from OpenWeatherMap API. It demonstrates **data extraction, transformation, loading, feature engineering, linear regression modeling, and prediction** in Python.

---

## Features

- **ETL Pipeline**: Fetch weather data from API and save to CSV.
- **Feature Engineering**: Convert timestamp to `hour` and `day`, use `humidity` as model feature.
- **Linear Regression Model**: Train a separate model per city.
- **Prediction**: Forecast tomorrow's temperature at 8 AM.
- **Evaluation**: Measure accuracy using Mean Squared Error (MSE).

---

## Dataset

- File: `data/weather_data.csv`  
- Columns:

| Column       | Description                             |
|--------------|-----------------------------------------|
| city         | City name (e.g., Jakarta, Bandung)      |
| temperature  | Temperature in °C                        |
| humidity     | Humidity percentage                      |
| weather      | Weather condition (Clear, Rain, etc.)   |
| timestamp    | Date and time of observation             |

> The script automatically appends daily weather data to this CSV.

---

## Requirements

- Python 3.10+
- pandas
- scikit-learn
- requests
- python-dotenv

Install dependencies:

```bash
pip install pandas scikit-learn requests python-dotenv
```

---

## Usage
- Place ```weather_data.csv``` in ```data/``` folder (will be auto-created if not exists).
- Edit API_KEY in your OpenWeatherMap API key.
- Run the script:
```bash
python predict_weather_api.py
```

---

## Example Output
```
Jakarta - MSE Model: 0.45
Jakarta - Prediksi suhu besok jam 8 pagi: 32.05°C
Bandung - MSE Model: 0.62
Bandung - Prediksi suhu besok jam 8 pagi: 28.10°C
...
```

---

## How It Works
- Extract → Fetch current weather data for multiple cities from OpenWeatherMap API.
- Transform → Extract temperature, humidity, weather, and timestamp.
- Load → Save data to `weather_data.csv` (append mode).
Feature Engineering → Generate hour and day features from timestamp.
- Modeling → Train Linear Regression model per city using features: humidity, hour, day.
- Prediction → Forecast tomorrow's temperature at 8 AM using average humidity and tomorrow’s day.
- Evaluation → Compute Mean Squared Error (MSE) to check model performance.

---

## Notes
- Script works best if CSV contains **10–15 days of historical data per city.**
- Using **DataFrame** ensures column names match when predicting → avoids scikit-learn warnings.
- CSV will grow daily → model accuracy improves over time.
- Suitable as a **learning project** for ETL + Machine Learning workflow.
