import requests
import os 
from datetime import datetime
import random
import json

OUTPUT_FILE = "docs/weather_update.html"

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

    html_content = f"""
    ----------------
    Ciudad {town}
    ----------------
    <div style="font-family: Arial, sans-serif; padding: 15px; border: 1px solid #ccc; max-width: 300px;">
        <h3>Tiempo en {town}</h3>
        <p><strong>Fecha:</strong> {datetime.now().strftime("%d/%m/%Y")}</p>
        <p><strong>Hora (UTC):</strong> {datetime.now().strftime("%H:%M:%S")}</p>
        <hr>
        <p><strong>Temperatura:</strong> {temperature}°C</p>
        <p><strong>Sensación Térmica:</strong> {feelsLike}°C</p>
        <p><strong>Condición:</strong> {weatherType}</p>
        <p><strong>Humedad:</strong> {humidity}%</p>
    </div>
    """
    return html_content

def updateWeatherPage():
    htmlTownContent = ""
    for town in final_locations:
            htmlTownContent += getWeather(town)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
         f.write(htmlTownContent)


updateWeatherPage()