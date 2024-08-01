import os
import httpx
import asyncio
import logging

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')


async def get_city_weather(city_name):
    coordinates = await get_city_coordinates(city_name)
    weather = await get_location_weather(coordinates)
    formatted_weather = format_weather(weather)
    return formatted_weather


async def get_city_coordinates(city_name):
    url = 'http://api.openweathermap.org/geo/1.0/direct'
    params = {
        'q': city_name,
        'limit': 5,
        'appid': api_key
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10.0)
            return {"latitude": response.json()[0]['lat'], 'longitude': response.json()[0]['lon']}
        except httpx.ReadError as e:
            logging.error(f"ReadError: {e}")


async def get_location_weather(coordinates: dict):
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'lat': coordinates['latitude'],
        'lon': coordinates['longitude'],
        'appid': api_key,
        'units': 'metric'
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10.0)
            return response.json()['main']
        except httpx.ReadError as e:
            logging.error(f"ReadError: {e}")


def format_weather(weather):
    output = (f'Температура: {weather['temp']} C, Ощущается как: {weather['feels_like']} C\n '
              f'Давление: {weather['pressure']}, Влажность: {weather['humidity']}')
    return output


# weather = asyncio.run(get_city_weather('Москва'))
# print(weather)
