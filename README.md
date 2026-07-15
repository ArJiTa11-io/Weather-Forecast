# 🌤️ Weather Forecast App

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FF4B4B.svg?style=for-the-badge&logo=Streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![OpenWeatherMap](https://img.shields.io/badge/API-OpenWeatherMap-orange?style=for-the-badge)

A weather forecasting web app built as part of my BCA (AI/ML) coursework. It fetches live weather data using the OpenWeatherMap API and uses a Random Forest model to predict short-term trends for temperature and other weather metrics, all displayed through an interactive Streamlit dashboard.

---

## 📌 About This Project

The project where I combined a live weather API with a basic machine learning model to explore how current conditions can be used to estimate near-future trends. 

---

## 🏗️ Project Structure

| File | What it does |
| :--- | :--- |
| `weather.csv` | Historical weather data used to train/support the prediction model |
| `.streamlit/secrets.toml` | Stores my OpenWeatherMap API key locally (not pushed to GitHub) |
| `.gitignore` | Keeps secrets and cache files out of version control |
| `app.py` | Main Streamlit app — handles the UI, API calls, and predictions |

---

## ⚙️ How It Works

### Fetching Live Weather Data
- The app calls the OpenWeatherMap API to get current weather details for a city — temperature, humidity, cloud cover, and wind speed.
- If the historical dataset (`weather.csv`) is missing or can't be read for some reason, the app falls back to a simpler prediction method instead of crashing.

### Predicting Trends
- I used a **Random Forest Regressor** to predict how temperature (and a few other metrics) might change over the next few hours, based on current readings.
- Used `st.cache_data` to cache the dataset loading step so the app doesn't reload data on every interaction — helped speed things up during testing.

---

## 📸 Screenshots

<p align="center">
  <img src="dashboard-main.png" alt="Main App Interface" width="100%">
  <br><br>
  <img src="dashboard-main(1).png" alt="Prediction Trend View" width="100%">
  <br><br>
  <img src="dashboard-main (2).png" alt="Data View" width="100%">
</p>

---

## 🛠️ Tech Stack

- **Python 3.13**
- **Streamlit** — for the web interface
- **Scikit-learn** — Random Forest model for predictions
- **OpenWeatherMap API** — live weather data
- **Pandas** — data handling

---

## 🚀 Running It Locally

```bash
# Clone the repo
git clone <your-repo-link>
cd weather-forecast-app

# Install dependencies
pip install -r requirements.txt

# Add your OpenWeatherMap API key
# Create .streamlit/secrets.toml and add:
# OPENWEATHER_API_KEY = "your_key_here"

# Run the app
streamlit run app.py
```

---

## 📚 What I Learned

- Working with REST APIs and handling live data in Python
- Training and using a basic Random Forest model for regression
- Building an interactive frontend with Streamlit
- Debugging across two different environments (Colab for the ML part, VS Code for the app) and getting them to work together
- Managing API keys securely instead of hardcoding them

---

## 🔮 Possible Improvements

- Add support for multiple cities at once
- Improve prediction accuracy with more historical data
- Add more weather metrics (rainfall probability, AQI, etc.)

---

*This is a student project built for learning purposes as part of my BCA coursework.*

