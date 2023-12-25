import geocoder
import requests
import json


city = None
country = None
method = None

fajr = ""
dhuhr = ""
asr = ""
maghrib = ""
isha = ""


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
        global fajr
        global dhuhr
        global asr
        global maghrib
        global isha
        fajr = data["data"]["timings"]["Fajr"]
        dhuhr = data["data"]["timings"]["Dhuhr"]
        asr = data["data"]["timings"]["Asr"]
        maghrib = data["data"]["timings"]["Maghrib"]
        isha = data["data"]["timings"]["Isha"]
        print(
            f"Fajr : {fajr}\n"
            f"Dhuhr: {dhuhr}\n"
            f"Asr: {asr}\n"
            f"Maghrib: {maghrib}\n"
            f"Isha: {isha}"
        )
    else:
        print(f"Error: {response.status_code}")


def get_location_auto():
    g = geocoder.ip("me")
    global city
    global country
    city = g.city
    country = g.country
