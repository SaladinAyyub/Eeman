import requests

import setup.location as location

location.get_location_response()

url = "http://api.aladhan.com/v1/timingsByCity"
params = {"city": location.city, "country": location.country}

response = requests.get(
    url,
    params,
    headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    },
)
print(f"response code:{response.status_code}")
print(f"response:{response.text}")
