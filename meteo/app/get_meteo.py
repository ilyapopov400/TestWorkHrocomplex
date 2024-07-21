"""
- получаем данные о погоде через данные о широте и долготе
"""
import requests
import datetime

from . import models
from . import get_coordinats


class Meteo:
    url = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, city: str):
        self.city = city

    def __get_coordinates(self):
        """
        :return: словарь с координатами долготы и широты типа float
        """
        coordinates = models.City.objects.filter(city=self.city)
        if coordinates:  # если координаты города есть в БД
            latitude = coordinates[0].latitude  # широта
            longitude = coordinates[0].longitude  # долгота
            return {
                "latitude": latitude,
                "longitude": longitude,
            }
        else:  # если в БД нет города
            try:
                latitude, longitude = get_coordinats.Coordinates(city=self.city)()  # получаем новые координаты города
                models.City.objects.create(
                    city=self.city.lower(), latitude=latitude, longitude=longitude)
                return {
                    "latitude": latitude,
                    "longitude": longitude,
                }
            except:
                return False

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
        temperature_now = self.__get_temperature().get(date_time_now)
        return temperature_now


if __name__ == "__main__":
    temperature = Meteo(city="москва")()
    print(temperature)
