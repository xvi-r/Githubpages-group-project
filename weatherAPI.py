import requests
import os 
from datetime import datetime
import random
import json

#Para sacar el diccionario del .env
location_string = os.environ.get("TOWN_LOCATIONS_JSON")
final_locations = {}

if location_string:
   
    location_dict = json.loads(location_string)

    final_locations = {
        town: tuple(coords) 
        for town, coords in location_dict.items()
    }
#-----------------
#---WEATHER API---
#-----------------
def getWeather(town):
    global final_locations
    API_KEY = os.environ.get("WEATHER_API_KEY")

    #LAT y LON
    lat = float(final_locations.get(town)[0])
    lon = float(final_locations.get(town)[1])
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
    print(f"Localidad: {town}")
    print(f"Date: {datetime.now().strftime("%A %B %Y")}")
    print(f"Time: {datetime.now().strftime("%H:%M")}")
    print("--------------------")
    print(f"Temperature: {temperature}°C")
    print(f"Weather: {weatherType}")
    print(f"Feels Like: {feelsLike}°C")
    print(f"Humidity: {humidity}%")

for town in final_locations:
    getWeather(town)
    print()