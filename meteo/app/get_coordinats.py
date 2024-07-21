import requests
from .keys import KEY


url = "https://catalog.api.2gis.com/3.0/items/geocode?q=город {}&fields=items.point&key={}".format("волгоград", KEY)

response = requests.get(url).json()


class Coordinates:
    key = KEY
    url = "https://catalog.api.2gis.com/3.0/items/geocode?q=город {}&fields=items.point&key={}"

    def __init__(self, city: str):
        self.city = city

    def __date(self):
        response = requests.get(self.url.format(
            self.city, self.key
        )).json()
        return response

    def __call__(self):
        result = self.__date()
        latitude = result.get("result").get("items")[0].get("point").get("lat")
        longitude = result.get("result").get("items")[0].get("point").get("lon")
        return latitude, longitude


if __name__ == "__main__":
    date = Coordinates(city="москва")()
    print(date)
    pass
