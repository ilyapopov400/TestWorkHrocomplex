"""
- получаем данные о погоде через данные о широте и долготе
"""
import requests

from . import models
from . import get_coordinats


class Meteo:
    url = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, city: str):
        self.city = city

    @staticmethod
    def __conversion_to_number(number):  # TODO
        return number

    def __get_coordinates(self):
        """
        :return: словарь с координатами долготы и широты типа float
        """
        coordinates = models.City.objects.filter(city=self.city)
        if coordinates:
            latitud = self.__conversion_to_number(number=coordinates[0].latitude)  # широта
            longitude = self.__conversion_to_number(number=coordinates[0].longitude)  # долгота
        else:  # если в БД нет города
            try:
                latitude, longitude = get_coordinats.Coordinates(city=self.city)()
                models.City.objects.create(
                    city=self.city.lower(), latitude=latitude, longitude=longitude)
                return {
                    "latitud": latitude,
                    "longitude": longitude,
                }
            except:
                return False
        return {
            "latitud": latitud,
            "longitude": longitude,
        }

    def __call__(self, *args, **kwargs):
        coordinates = self.__get_coordinates()
        if not coordinates:
            return False
        params = {
            "latitude": coordinates.get("latitud"),
            "longitude": coordinates.get("longitude"),
            "hourly": "temperature_2m",
        }
        response = requests.post(self.url, data=params).json()
        temperature_now = response.get("hourly").get("temperature_2m")[0]
        return temperature_now


if __name__ == "__main__":
    temperature = Meteo(city="москва")()
    print(temperature)
