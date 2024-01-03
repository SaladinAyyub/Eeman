import geocoder
import requests
import json


city = None
country = None
method = None
hanafi_school = 0


prayer = {"Fajr": "", "Sunrise": "", "Dhuhr": "", "Asr": "", "Maghrib": "", "Isha": ""}
date = None
timezone = None


def get_response():
    url = "http://api.aladhan.com/v1/timingsByCity"
    params = {"city": city, "country": country, "school": hanafi_school}
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
    global city
    global country
    city = g.city
    country = g.country
