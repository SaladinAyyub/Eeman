method = None


def get_method_manual():
    global method
    method = input("Which calculation method you want to use ?")


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
