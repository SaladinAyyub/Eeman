import json
from configparser import ConfigParser

import geocoder
import requests

prayer = {"Fajr": "", "Sunrise": "", "Dhuhr": "", "Asr": "", "Maghrib": "", "Isha": ""}
date = None
timezone = None
hijri_date = None

config = ConfigParser()


def get_response():
    global config
    config.read("config.ini")
    method = config["Prayer"]["method"]
    hanafi_school = config["Prayer"]["hanafi_school"]
    location_mode = config["Prayer"]["location_mode"]
    if location_mode == "Automatic":
        get_location_auto()
        config.read("config.ini")
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
        global hijri_date
        date = data["data"]["date"]["readable"]
        timezone = data["data"]["meta"]["timezone"]
        hijri_date = "%s %s, %s %s" % (
            data["data"]["date"]["hijri"]["month"]["en"],
            data["data"]["date"]["hijri"]["month"]["number"],
            data["data"]["date"]["hijri"]["year"],
            data["data"]["date"]["hijri"]["designation"]["abbreviated"],
        )
    else:
        print(f"Error: {response.status_code}")


def get_location_auto():
    g = geocoder.ip("me")
    set_config("Prayer", "city", g.city)
    set_config("Prayer", "country", g.country)


def set_config(section, option, value):
    global config
    config.read("config.ini")
    config.set(section, option, value)
    with open("config.ini", "w") as file:
        config.write(file)


def get_response_quran_surah_data():
    url = "https://api.alquran.cloud/v1/surah"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data


def get_quran_surah_name_english(surah, data):
    return data["data"][surah - 1]["englishName"]


def get_quran_surah_name_arabic(surah, data):
    return data["data"][surah - 1]["name"]


def get_number_of_ayahs(surah, data):
    return data["data"][surah - 1]["numberOfAyahs"]


def get_response_quran_ayah_data_english(surah):
    url = f"https://api.alquran.cloud/v1/surah/{surah}/en.sahih"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data


def get_response_quran_ayah_data_arabic(surah):
    url = f"https://api.alquran.cloud/v1/surah/{surah}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data


def get_quran_ayah_text(data, ayah):
    return data["data"]["ayahs"][ayah - 1]["text"]
