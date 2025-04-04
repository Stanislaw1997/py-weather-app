import requests

def get_weather_data(city, api_key):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    geo_response = requests.get(geo_url)
    geo_response.raise_for_status()
    geo_data = geo_response.json()

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    weather_response = requests.get(weather_url)
    weather_response.raise_for_status()
    weather_data = weather_response.json()

    return geo_data[0], weather_data

def get_weather_emoji(weather_id):
    if 200 <= weather_id <= 232:
        return "⛈️"
    elif 300 <= weather_id <= 321:
        return "🌦️"
    elif 500 <= weather_id <= 531:
        return "🌧️"
    elif 600 <= weather_id <= 622:
        return "🌨️"
    elif 700 <= weather_id <= 781:
        return "🌫️"
    elif weather_id == 762:
        return "🌋"
    elif weather_id == 771:
        return "💨"
    elif weather_id == 781:
        return "🌪️"
    elif weather_id == 800:
        return "☀️"
    elif 801 <= weather_id <= 804:
        return "☁️"
    else:
        return ""