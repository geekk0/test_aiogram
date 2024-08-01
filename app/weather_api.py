import os
import httpx
import asyncio

from dotenv import load_dotenv

from app.bot_setup import logger

load_dotenv()
api_key = os.getenv('API_KEY')


async def get_city_weather(city_name):
    coordinates = await get_city_coordinates(city_name)
    if coordinates:
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

    headers = {
        'Accept': 'application/json',
        'User-Agent': 'test_aiogram'
    }

    max_retries = 5
    backoff_factor = 1

    async with httpx.AsyncClient() as client:
        for attempt in range(max_retries):
            try:
                response = await client.get(url, params=params, headers=headers, timeout=10.0)
                if response.status_code == 200:
                    return {"latitude": response.json()[0]['lat'], 'longitude': response.json()[0]['lon']}
            except httpx.RequestError as e:
                logger.error(f"RequestError: {str(e)} \n attempt: {attempt}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(backoff_factor * (2 ** attempt))
                else:
                    raise
            except Exception as e:
                logger.error(f"ReadError: {str(e)} \n attempt: {attempt}")
                raise


async def get_location_weather(coordinates: dict):
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'lat': coordinates['latitude'],
        'lon': coordinates['longitude'],
        'appid': api_key,
        'units': 'metric'
    }

    headers = {
        'Accept': 'application/json',
        'User-Agent': 'test_aiogram'
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, headers=headers, timeout=10.0)
            if response.status_code == 200:
                return response.json()['main']
        except Exception as e:
            logger.error(f"ReadError: {str(e)}")


def format_weather(weather):
    output = (f'Температура: {weather['temp']} C, Ощущается как: {weather['feels_like']} C\n '
              f'Давление: {weather['pressure']}, Влажность: {weather['humidity']}')
    return output



