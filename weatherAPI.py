import requests
import os 
from datetime import datetime
import random


#-----------------
#---WEATHER API---
#-----------------
def getSpainWeather():
    API_KEY = os.environ.get("WEATHER_API_KEY")

    #LAT y LON
    lat = float(os.environ.get("LAT_PALMA"))
    lon = float(os.environ.get("LON_PALMA"))
    units = "metric"

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={units}&appid={API_KEY}"


    response = requests.get(url).json()

    weatherType = response["weather"][0]["main"]
    temperature = response["main"]["temp"]
    feelsLike = response["main"]["feels_like"]
    humidity = response["main"]["humidity"]
    country = response["sys"]["country"]

    match weatherType:
        case "Clouds":
            weatherType+= " ☁️"
        case "Snow":
            weatherType+= " ❄️"
        case "Clear":
            weatherType+= " ☀️"

    #print(response)
    print(f"Country: {country}")
    print(f"Date: {datetime.now().strftime("%A %B %Y")}")
    print(f"Time: {datetime.now().strftime("%H:%M")}")
    print("--------------------")
    print(f"Temperature: {temperature}°C")
    print(f"Weather: {weatherType}")
    print(f"Feels Like: {feelsLike}°C")
    print(f"Humidity: {humidity}%")