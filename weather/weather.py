import os
from dotenv import load_dotenv
import requests
load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")


city = input('Enter city: ')
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    wind_speed = data['wind']['speed']
    description = data['weather'][0]['description']
    print(f"Погода в городе {city}:")
    print(f"🌡️ Температура: {temp}°C")
    print(f"🌡️ Ощущается как: {feels_like}°C")
    print(f"💧 Влажность: {humidity}%")
    print(f"🌀 Давление: {pressure} гПа")
    print(f"💨 Ветер: {wind_speed} м/с")
    print(f"☁️ Описание: {description}")
else:
    print('Error name city!')
