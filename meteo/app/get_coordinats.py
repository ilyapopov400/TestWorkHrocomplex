import requests

from .keys import KEY  # ключ действителен на месяц до 20 августа 2024 года


class Coordinates:
    """
    - получение координат города в (float, float) через API
    """
    key = KEY
    url = "https://catalog.api.2gis.com/3.0/items/geocode?q=город {}&fields=items.point&key={}"

    def __init__(self, city: str):
        self.city = city

    def __date(self):
        try:
            response = requests.get(self.url.format(
                self.city, self.key
            ))
            return response.json()
        except:
            return False

    def __call__(self):
        result = self.__date()
        try:
            latitude = result.get("result").get("items")[0].get("point").get("lat")
            longitude = result.get("result").get("items")[0].get("point").get("lon")
            return latitude, longitude
        except:
            return False


if __name__ == "__main__":
    date = Coordinates(city="москва")()
    print(date)
