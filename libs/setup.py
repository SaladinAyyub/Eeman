import geocoder
import requests
import json
from configparser import ConfigParser

prayer = {"Fajr": "", "Sunrise": "", "Dhuhr": "", "Asr": "", "Maghrib": "", "Isha": ""}
date = None
timezone = None

config = ConfigParser()


def get_response():
    global config
    config.read("config.ini")
    method = config["Prayer"]["method"]
    hanafi_school = config["Prayer"]["hanafi_school"]
    location_mode = config["Prayer"]["location_mode"]
    if location_mode == "Automatic":
        get_location_auto()
    city = config["Prayer"]["city"]
    country = config["Prayer"]["country"]
    method_mode = config["Prayer"]["method_mode"]
    url = "http://api.aladhan.com/v1/timingsByCity"
    params = {"city": city, "country": country, "school": hanafi_school}
    if method_mode == "Manual":
        params["method"] = method

    response = requests.get(
        url,
        params,
    )
    if response.status_code == 200:
        data = json.loads(response.text)
        global prayer
        prayer["Fajr"] = data["data"]["timings"]["Fajr"]
        prayer["Sunrise"] = data["data"]["timings"]["Sunrise"]
        prayer["Dhuhr"] = data["data"]["timings"]["Dhuhr"]
        prayer["Asr"] = data["data"]["timings"]["Asr"]
        prayer["Maghrib"] = data["data"]["timings"]["Maghrib"]
        prayer["Isha"] = data["data"]["timings"]["Isha"]

        global date
        global timezone
        date = data["data"]["date"]["readable"]
        timezone = data["data"]["meta"]["timezone"]
    else:
        print(f"Error: {response.status_code}")


def get_location_auto():
    g = geocoder.ip("me")
    global config
    config.read("config.ini")
    config.set("Prayer", "city", g.city)
    config.set("Prayer", "country", g.country)
    with open("config.ini", "w") as file:
        config.write(file)
