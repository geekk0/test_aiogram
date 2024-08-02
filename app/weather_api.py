import os
import httpx
import asyncio

from dotenv import load_dotenv

from app.bot_setup import logger

load_dotenv()
api_key = os.getenv('API_KEY')


async def get_city_weather(city_name):

    url = "http://api.weatherapi.com/v1/current.json"

    params = {
        'q': city_name,
        'key': api_key
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10.0)
            if response.status_code == 200:
                return format_weather(response.json()['current'])
        except Exception as e:
            logger.error(f"ReadError: {str(e)}")


def format_weather(weather):
    output = (f'Температура: {weather['temp_c']}C \n '
              f'Ощущеается как: {weather['feelslike_c']}С\n '
              f'Скорость ветра: {weather['wind_kph']} Км\ч\n '
              f'Давление: {weather['pressure_mb']} мм.рт.ст\n '
              f'Влажность: {weather['humidity']}%')
    return output


# weather = asyncio.run(get_city_weather('Chicago'))
# print(format_weather(weather))



