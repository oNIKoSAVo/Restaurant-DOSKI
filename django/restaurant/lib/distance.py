from django.db.models import query
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from dadata import Dadata

token = "5870aa5579db3be0faff6aa85d1caf810be3baca"
secret = "31f241bf49919a8fe86effcae6ef2a224466a560"
dadata = Dadata(token, secret)
structure = ["ADDRESS"]

class Distance:

    def __init__(self):
        self.dist = None
        self.origin = None
        self.address1 = None
        self.address2 = None

    def calculate(self, address1=None, address2=None):

        geolocator = Nominatim(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36")

        if self.address1 != address1 and address1 is not None:
            self.address1 = address1
            # location1 = geolocator.geocode(address1)
            # print(location1.address)
            # print((location1.latitude, location1.longitude))
            result = dadata.suggest(name="address", query=self.address1)
            print(result[0]["data"]["geo_lat"])
            print(result[0]["data"]["geo_lon"])
            self.origin = (result[0]["data"]["geo_lat"], result[0]["data"]["geo_lon"])

        if self.address2 != address2 and address2 is not None:
            self.address2 = address2
            # location2 = geolocator.geocode(address2)
            # print(location2.address)
            # print((location2.latitude, location2.longitude))
            result = dadata.suggest(name="address", query=self.address2)
            print(result[0]["data"]["geo_lat"])
            print(result[0]["data"]["geo_lon"])
            self.dist = (result[0]["data"]["geo_lat"], result[0]["data"]["geo_lon"])

        return geodesic(self.origin, self.dist)