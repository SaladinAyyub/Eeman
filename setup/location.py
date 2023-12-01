import geocoder


city = None
country = None


def get_location_auto():
    g = geocoder.ip("me")
    global city
    global country
    city = g.city
    country = g.country


def get_location_manual():
    global city
    global country
    city = input("What is your city\n")
    country = input("What is your country\n")


def get_location_response():
    location_response = input(
        "Do you want to your location to be automatically set using your IP ?\n Type y/yes for automatic location \n n/no for manually selecting your location\n"
    ).lower()

    if location_response == "yes" or location_response == "y":
        get_location_auto()
    elif location_response == "no" or location_response == "n":
        get_location_manual()
    else:
        print("Invalid Input")
        exit()
