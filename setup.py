import geocoder


city = None
country = None


def get_location_auto():
    g = geocoder.ip("me")
    global city
    global country
    city = g.city
    country = g.country
