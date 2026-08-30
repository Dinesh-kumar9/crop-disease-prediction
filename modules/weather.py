"""
modules/weather.py
OpenWeatherMap integration: 5-day forecast and agricultural risk analysis.
API key is read from the OWM_API_KEY environment variable (set via .env).
"""

import requests
import os

# OpenWeatherMap API Key — set OWM_API_KEY in your .env file.
# See .env.example for instructions.
API_KEY = os.getenv("OWM_API_KEY", "")
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

def get_weather_forecast(city="Hyderabad"):
    """
    Fetches 5-day weather forecast from OpenWeatherMap.
    Returns a simplified list of daily forecasts.
    """
    if not API_KEY:
        return {
            "error": "OWM_API_KEY not set. Add it to your .env file. See .env.example.",
            "forecast": []
        }

    try:
        url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code == 404:
            return {"error": f"City '{city}' not found. Please check the spelling.", "forecast": []}
        elif response.status_code == 401:
            # API key invalid - use mock data for testing
            print("⚠️ API Key invalid. Using mock weather data for demonstration.")
            return get_mock_weather_forecast(city)
        elif response.status_code != 200:
            return {"error": data.get("message", "Weather service error"), "forecast": []}

        # Process the raw 3-hour forecast into daily summaries
        daily_forecast = []
        # We will pick one data point per day (e.g., noon) for simplicity
        # or aggregate. For MVP, let's pick noon entries.
        
        for item in data['list']:
            if "12:00:00" in item['dt_txt']:
                daily_forecast.append({
                    "date": item['dt_txt'].split(" ")[0],
                    "temp": item['main']['temp'],
                    "humidity": item['main']['humidity'],
                    "weather": item['weather'][0]['main'],
                    "description": item['weather'][0]['description'],
                    "wind_speed": item['wind']['speed']
                })
        
        return {"error": None, "forecast": daily_forecast}

    except Exception as e:
        print(f"⚠️ Weather API error: {e}. Using mock data.")
        return get_mock_weather_forecast(city)

def get_mock_weather_forecast(city="Hyderabad"):
    """
    Returns mock weather data for testing when API is unavailable.
    """
    from datetime import datetime, timedelta
    
    mock_forecast = []
    base_date = datetime.now()
    
    # Generate 5 days of mock weather
    weather_patterns = [
        {"weather": "Clear", "description": "clear sky", "temp": 28, "wind": 12},
        {"weather": "Clouds", "description": "few clouds", "temp": 26, "wind": 15},
        {"weather": "Clear", "description": "clear sky", "temp": 30, "wind": 10},
        {"weather": "Rain", "description": "light rain", "temp": 24, "wind": 18},
        {"weather": "Clouds", "description": "scattered clouds", "temp": 27, "wind": 14},
    ]
    
    for i, pattern in enumerate(weather_patterns):
        date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
        mock_forecast.append({
            "date": date,
            "temp": pattern["temp"],
            "humidity": 65,
            "weather": pattern["weather"],
            "description": pattern["description"],
            "wind_speed": pattern["wind"]
        })
    
    return {
        "error": None, 
        "forecast": mock_forecast,
        "is_mock": True  # Flag to indicate this is mock data
    }

def analyze_weather_risks(forecast_data):
    """
    Analyzes forecast for agricultural risks.
    """
    risks = []
    for day in forecast_data:
        date = day['date']
        
        # Risk Logic
        if day['wind_speed'] > 20:
            risks.append(f"{date}: High winds ({day['wind_speed']} km/h). Avoid spraying pesticides.")
        
        if "Rain" in day['weather']:
            risks.append(f"{date}: Rain expected. Delay irrigation.")
        
        if day['temp'] > 35:
            risks.append(f"{date}: High heat ({day['temp']}°C). Ensure mulch/shade.")

    return risks
