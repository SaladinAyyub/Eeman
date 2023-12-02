import requests

import setup_cli.location as location
import setup_cli.method as method


def run():
    location.get_location_response()
    method.get_method_response()

    url = "http://api.aladhan.com/v1/timingsByCity"
    params = {"city": location.city, "country": location.country}

    response = requests.get(
        url,
        params,
    )
    print(f"response code:{response.status_code}")
    print(f"response:{response.text}")
