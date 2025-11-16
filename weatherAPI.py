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
  <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tiempo en {town}</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" 
          rel="stylesheet" crossorigin="anonymous">

    <style>
        .weather-card {{
            max-width: 360px;
        }}
    </style>
</head>
<body class="bg-light">

    <div class="container py-4">
        <div class="weather-card mx-auto">
            
            <div class="card shadow border-0 rounded-3">
                <div class="card-body p-4">

                    <h3 class="h4 card-title fw-bold text-primary mb-3">
                        Tiempo en {town}
                    </h3>

                    <hr class="mt-0 mb-3">

                    <div class="row g-2 mb-3">
                        <div class="col-6">
                            <p class="mb-0 text-muted small">Temperatura:</p>
                            <p class="mb-0 fs-5 fw-bold">{temperature}°C</p>
                        </div>

                        <div class="col-6">
                            <p class="mb-0 text-muted small">Sensación Térmica:</p>
                            <p class="mb-0 fs-5 fw-bold text-secondary">{feelsLike}°C</p>
                        </div>

                        <div class="col-12 mt-3">
                            <p class="mb-0 fw-semibold text-success">
                                Condición: {weatherType}
                            </p>
                        </div>
                    </div>

                    <div class="d-flex justify-content-between align-items-center border-top pt-2">
                        <p class="mb-0 small text-muted">
                            <span class="fw-bold">Humedad:</span> {humidity}%
                        </p>

                        <p class="mb-0 small text-end text-secondary" style="font-size: 0.75rem;">
                            <span class="d-block">Fecha: {datetime.now().strftime("%d/%m/%Y")}</span>
                            <span class="d-block">Hora (UTC): {datetime.now().strftime("%H:%M:%S")}</span>
                        </p>
                    </div>

                </div>
            </div>

        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
            crossorigin="anonymous"></script>
</body>
</html>

    """
    return html_content

def updateWeatherPage():
    htmlTownContent = ""
    for town in final_locations:
            htmlTownContent = ""
            htmlTownContent += getWeather(town)
            with open(f"docs/{town}.html", "w", encoding="utf-8") as f:
                f.write(htmlTownContent)


updateWeatherPage()