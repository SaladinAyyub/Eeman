import geocoder
import requests
import json


city = None
country = None
method = None

prayer = {"Fajr": "", "Dhuhr": "", "Asr": "", "Maghrib": "", "Isha": ""}


def get_response():
    url = "http://api.aladhan.com/v1/timingsByCity"
    params = {"city": city, "country": country}
    if method is not None:
        params["method"] = method

    response = requests.get(
        url,
        params,
    )
    if response.status_code == 200:
        data = json.loads(response.text)
        global prayer
        prayer["Fajr"] = data["data"]["timings"]["Fajr"]
        prayer["Dhuhr"] = data["data"]["timings"]["Dhuhr"]
        prayer["Asr"] = data["data"]["timings"]["Asr"]
        prayer["Maghrib"] = data["data"]["timings"]["Maghrib"]
        prayer["Isha"] = data["data"]["timings"]["Isha"]
    else:
        print(f"Error: {response.status_code}")


def get_location_auto():
    g = geocoder.ip("me")
    global city
    global country
    city = g.city
    country = g.country
