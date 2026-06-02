# app.py
import streamlit as st
import datetime
from zoneinfo import ZoneInfo
import requests

# --- CONFIG ---
WEATHER_API_KEY = "YOUR_API_KEY_HERE"
 
def get_weather(city: str) -> dict:
    """Fetch current weather for any city using OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        temp_c = data["main"]["temp"]
        temp_f = temp_c * 9/5 + 32
        description = data["weather"][0]["description"].capitalize()
        return {
            "status": "success",
            "report": f"The weather in {city} is {description}, {temp_c:.1f}°C ({temp_f:.1f}°F)."
        }
    else:
        return {"status": "error", "error_message": f"Could not fetch weather for {city}."}

def get_current_time(city: str) -> dict:
    """Fetch current time for any city using OpenWeatherMap timezone info."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        tz_offset = data["timezone"]  # seconds offset from UTC
        now_utc = datetime.datetime.utcnow()
        now_local = now_utc + datetime.timedelta(seconds=tz_offset)
        report = f"The current time in {city} is {now_local.strftime('%Y-%m-%d %H:%M:%S')} (UTC{tz_offset//3600:+d})"
        return {"status": "success", "report": report}
    else:
        return {"status": "error", "error_message": f"Could not fetch time for {city}."}

# --- STREAMLIT UI ---
st.title("🌍 Weather & Time Agent")

city = st.text_input("Enter a city name:", "New York")
option = st.radio("Choose what you want:", ["Weather", "Time"])

if st.button("Get Report"):
    if option == "Weather":
        result = get_weather(city)
    else:
        result = get_current_time(city)

    if result["status"] == "success":
        st.success(result["report"])
    else:
        st.error(result["error_message"])

