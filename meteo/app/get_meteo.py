"""
- получаем данные о погоде через данные о широте и долготе
"""
import requests
import datetime

from . import models
from . import get_coordinats


class Meteo:
    """
    - получаем данные о погоде через API
    """
    url = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, city: str):
        self.city = city

    def __get_coordinates(self):
        """
        - получаем словарь с координатами города, если в БД нет города,
        то через Coordinates получаем их и заносим в БД
        :return: словарь с координатами долготы и широты типа float
        """
        result = False  # если данных о координатах города нет, то возвращается False
        coordinates = models.City.objects.filter(city=self.city)
        if coordinates:  # если координаты города есть в БД
            latitude = coordinates[0].latitude  # широта
            longitude = coordinates[0].longitude  # долгота
            result = {
                "latitude": latitude,
                "longitude": longitude,
            }
        else:  # если в БД нет города
            coordinates_new = get_coordinats.Coordinates(city=self.city)()  # получаем новые координаты города
            if coordinates_new:
                latitude, longitude = coordinates_new
                models.City.objects.create(
                    city=self.city.lower(), latitude=latitude, longitude=longitude)
                result = {
                    "latitude": latitude,
                    "longitude": longitude,
                }
        return result

    def __get_temperature(self):
        coordinates = self.__get_coordinates()
        if not coordinates:
            return False
        params = {
            "latitude": coordinates.get("latitude"),
            "longitude": coordinates.get("longitude"),
            "hourly": "temperature_2m",
        }
        response = requests.post(self.url, data=params).json()
        times = response.get("hourly").get("time")
        temperatures = response.get("hourly").get("temperature_2m")
        temperature_dict = dict(zip(times, temperatures))
        return temperature_dict

    def __call__(self):
        date_time_now = datetime.datetime.now().strftime('%Y-%m-%dT%H:00')  # дата и время на сейчас
        if self.__get_temperature():  # если получили данные о температуре
            temperature_now = self.__get_temperature().get(date_time_now)
            return temperature_now
        return False


if __name__ == "__main__":
    temperature = Meteo(city="москва")()
    print(temperature)
