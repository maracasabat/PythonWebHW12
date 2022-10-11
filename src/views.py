import asyncio

import aiohttp_jinja2
import aiohttp
from bs4 import BeautifulSoup

from src.urls import weather_url


async def get_weather_1(session, url):
    async with session.get(url) as response:
        data = await response.text()
        soup = BeautifulSoup(data, 'html.parser')

        temp = soup.find('a', {'class': 'summaryTemperatureCompact-E1_1'}).text
        wind = soup.find('div', {'id': 'CurrentDetailLineWindValue'}).text
        desc = soup.find('div', {'class': 'summaryCaptionCompact-E1_1'}).text
        return temp, wind, desc


async def get_weather_2(session, url):
    async with session.get(url) as response:
        data = await response.text()
        soup = BeautifulSoup(data, 'html.parser')

        temp = soup.find('span', {'class': 'CurrentConditions--tempValue--3a50n'}).text
        wind = soup.find('span', {'class': 'Wind--windWrapper--3aqXJ undefined'}).text[-5:]
        desc = soup.find('div', {'class': 'CurrentConditions--phraseValue--2Z18W'}).text
        return temp, wind, desc


async def get_weather_3(session, url):
    async with session.get(url) as response:
        data = await response.text()
        soup = BeautifulSoup(data, 'html.parser')

        temp = soup.find('span', {'class': 'temp'}).text
        wind = soup.find('span', {'class': 'windp'}).text
        desc = soup.find('div', {'class': 'mid'}).text[5:-1]
        return temp, wind, desc


async def start():
    async with aiohttp.ClientSession() as session:
        task1, task2, task3 = await asyncio.gather(get_weather_1(session, weather_url[0]),
                                                   get_weather_2(session, weather_url[1]),
                                                   get_weather_3(session, weather_url[2]))
        return task1, task2, task3


@aiohttp_jinja2.template('index.html')
async def index(request):
    task1, task2, task3 = await start()
    return {'task1': task1, 'task2': task2, 'task3': task3}


def setup_routes(app):
    app.router.add_get('/', index)
