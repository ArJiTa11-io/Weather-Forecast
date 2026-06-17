import streamlit as st
import requests
import pandas as pd
import numpy as np
import pytz
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

bg_image = 'https://images.unsplash.com/photo-1504701954957-2010ec3bcec1?w=800'

st.set_page_config(page_title="Weather Forecast", page_icon="🌤️", layout="wide")

st.markdown("""
<style>
    body {background-color: #1a1a2e;}
    .stApp {background-color: #1a1a2e;}
    section[data-testid="stSidebar"] {display: none;}
    [data-testid="stToolbar"] {display: none;}
    .block-container {padding: 2rem !important; max-width: 100% !important;}
    
    /* Input field glassmorphism styling */
    .stTextInput input { 
        background: rgba(255,255,255,0.1) !important; 
        color: white !important; 
        border: none !important; 
        border-bottom: 1px solid rgba(255,255,255,0.5) !important; 
        padding: 10px !important; 
        border-radius: 5px !important;
    }
    .stTextInput input::placeholder {
        color: rgba(255,255,255,0.7) !important;
    }
</style>
""", unsafe_allow_html=True)

API_KEY = st.secrets["api_key"]
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather_image(description):
    description = description.lower()
    if 'thunder' in description or 'storm' in description:
        return 'https://images.unsplash.com/photo-1605727216801-e27ce1d0cc28?w=800'
    elif 'rain' in description or 'drizzle' in description:
        return 'https://images.unsplash.com/photo-1519692933481-e162a57d6721?w=800'
    elif 'snow' in description:
        return 'https://images.unsplash.com/photo-1491002052546-bf38f186af56?w=800'
    elif 'haze' in description or 'fog' in description or 'mist' in description:
        return 'https://images.unsplash.com/photo-1487621167305-5d248087c724?w=800'
    elif 'cloud' in description or 'overcast' in description:
        return 'https://images.unsplash.com/photo-1501630834273-4b5604d2ee31?w=800'
    elif 'clear' in description or 'sun' in description:
        return 'https://images.unsplash.com/photo-1601297183305-6df142704ea2?w=800'
    else:
        return 'https://images.unsplash.com/photo-1501630834273-4b5604d2ee31?w=1600'

def get_current_weather(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data.get('cod') != 200:
        return None

    return {
        'city': data['name'],
        'current_temp': round(data['main']['temp']),
        'feels_like': round(data['main']['feels_like']),
        'temp_min': round(data['main']['temp_min']),
        'temp_max': round(data['main']['temp_max']),
        'humidity': round(data['main']['humidity']),
        'pressure': data['main']['pressure'],
        'description': data['weather'][0]['description'],
        'country': data['sys']['country'],
        'wind_speed': data['wind']['speed'],
        'clouds': data.get('clouds', {}).get('all', 0)
    }

@st.cache_data
def prepare_models():
    try:
        df = pd.read_excel('weather.csv').dropna().drop_duplicates()
        le = LabelEncoder()
        df['WindGustDir'] = le.fit_transform(df['WindGustDir'])
        df['RainTomorrow'] = le.fit_transform(df['RainTomorrow'])
        x_temp = np.array(df['Temp'][:-1]).reshape(-1,1)
        y_temp = np.array(df['Temp'][1:])
        x_hum = np.array(df['Humidity'][:-1]).reshape(-1,1)
        y_hum = np.array(df['Humidity'][1:])
        temp_model = RandomForestRegressor(n_estimators=100, random_state=42)
        temp_model.fit(x_temp, y_temp)
        hum_model = RandomForestRegressor(n_estimators=100, random_state=42)
        hum_model.fit(x_hum, y_hum)
        return temp_model, hum_model
    except Exception:
        return None, None

def get_future_forecasts(weather, temp_model, hum_model):
    if not temp_model or not hum_model:
        return []
    timezone = pytz.timezone('Asia/Kolkata')
    now = datetime.now(timezone)
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    temp = float(weather['current_temp'])
    hum = float(weather['humidity'])
    forecasts = []
    for i in range(5):
        future_time = next_hour + timedelta(hours=i)
        temp = round(float(temp_model.predict([[temp]])[0]), 1)
        hum = round(float(hum_model.predict([[hum]])[0]), 1)
        forecasts.append({
            'time': future_time.strftime("%H:00"),
            'temp': temp,
            'humidity': hum
        })
    return forecasts

# ----- LAYOUT SETUP -----
left, right = st.columns([1, 2.5]) 
weather = None
default_bg_image = 'https://images.unsplash.com/photo-1501630834273-4b5604d2ee31?w=1600'

# ----- LEFT PANEL -----
with left:
    city = st.text_input("", placeholder="🔍 Enter City Name...", label_visibility="collapsed")
    
    if city:
        weather = get_current_weather(city)
        if weather:
            st.markdown(f"""
<div style="background: rgba(255,255,255,0.08); border-radius: 20px; padding: 30px 20px; color: white; backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.2); margin-top: 15px; height: 100%;">
<div style='font-size:70px; font-weight:300;'>{weather['current_temp']}°</div>
<div style='font-size:16px; opacity:0.8;'>Feels like: {weather['feels_like']}°</div>
<br>
<div style='font-size:18px;'>{weather['humidity']}% &nbsp; Humidity</div>
<br>
<div style='font-size:18px;'>{weather['clouds']}% &nbsp; Clouds</div>
</div>
""", unsafe_allow_html=True)
        else:
            st.error("City not Found!")

# ----- DYNAMIC BACKGROUND -----
big_image = get_weather_image(weather['description']) if weather else default_bg_image

st.markdown(f"""
<style>
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.6)), url('{big_image}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
</style>
""", unsafe_allow_html=True)

# ----- RIGHT PANEL -----
with right:
    if weather:
        timezone = pytz.timezone('Asia/Kolkata')
        now = datetime.now(timezone)
        temp_model, hum_model = prepare_models()
        forecasts = get_future_forecasts(weather, temp_model, hum_model)

        cards_html = ""
        for f in forecasts:
            cards_html += f"""
<div style='flex:1; text-align:center; backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.1); border-radius: 15px; padding: 20px;'>
<div style='font-size:14px; opacity:0.8;'>{f['time']}</div>
<div style='font-size:36px; font-weight:300; margin: 10px 0;'>{f['temp']}°</div>
<div style='font-size:13px; opacity:0.7;'>Hum: {f['humidity']}%</div>
</div>
"""

        st.markdown(f"""
<div style="padding: 20px; color: white; display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
<div>
<div style='font-size:14px; opacity:0.8; letter-spacing:2px; text-transform: uppercase;'>Weather Forecast</div>
<div style='font-size:54px; font-weight:300; margin:5px 0; text-transform: capitalize;'>{weather['description']}</div>
<div style='font-size:16px; opacity:0.9;'>📍 {weather['city']}, {weather['country']} &nbsp;|&nbsp; {now.strftime("%b. %d, %Y, %I:%M %p")}</div>
<br>
<div style='font-size:15px; opacity:0.8; line-height:1.8; background: rgba(0,0,0,0.2); padding: 15px; border-radius: 10px; max-width: 600px;'>
Wind is at <b>{weather['wind_speed']} km/h</b>. Pressure is <b>{weather['pressure']} mb</b>.<br>
Maximum temperature is <b>{weather['temp_max']}°</b>. Minimum temperature is <b>{weather['temp_min']}°</b>.
</div>
</div>
<div style='display:flex; gap:20px; margin-top: 40px; flex-wrap: wrap;'>
{cards_html}
</div>
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
<div style='color:white; text-align:center; padding-top: 150px;'>
<div style='font-size:16px; opacity:0.8; letter-spacing:3px;'>WEATHER FORECAST</div>
<br>
<div style='font-size:24px; opacity:0.6; font-weight: 300;'>Please enter a city name in the search bar.</div>
</div>
""", unsafe_allow_html=True)
        
                           
