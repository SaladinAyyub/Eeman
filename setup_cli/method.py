method = None


def get_method_manual():
    global method
    method = input(
        "Which calculation method you want to use ?\n"
        "0 - Shia Ithna-Ansari\n"
        "1 - University of Islamic Sciences, Karachi\n"
        "2 - Islamic Society of North America\n"
        "3 - Muslim World League\n"
        "4 - Umm Al-Qura University, Makkah\n"
        "5 - Egyptian General Authority of Survey\n"
        "7 - Institute of Geophysics, University of Tehran\n"
        "8 - Gulf Region\n"
        "9 - Kuwait\n"
        "10 - Qatar\n"
        "11 - Majlis Ugama Islam Singapura, Singapore\n"
        "12 - Union Organization islamic de France\n"
        "13 - Diyanet İşleri Başkanlığı, Turkey\n"
        "14 - Spiritual Administration of Muslims of Russia\n"
        "15 - Moonsighting Committee Worldwide\n"
        "16 - Dubai (unofficial)\n\n"
        "Type the number\n"
    )


def get_method_response():
    method_response = input(
        "Do you want to use the nearest calculation method ?\n"
        "Type Y/Yes to automatically get the nearest calculation method.\n"
        "Type N/No to set calculation method manually.\n"
    ).lower()

    if method_response == "n" or method_response == "no":
        get_method_manual()
    elif method_response == "y" or method_response == "yes":
        print("using nearest calculation method")
    else:
        print("invalid input")
        exit()
