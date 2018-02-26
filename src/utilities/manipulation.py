__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


def sizeof_fmt(num, suffix="b"):
    if num < 1024.0:
        return [num, "0Kb"]
    for unit in [" ", "K", "M", "G", "T", "P"]:
        if abs(num) < 1024.0:
            return [num, "%3.1f%s%s" % (num, unit, suffix)]

        num /= 1024.0
    return [num, "%.1f%s%s" % (num, 'E', suffix)]


def query_user(message, options, on_error=""):
    user_input = ''
    while user_input not in options:
        user_input = input(message)

        try:
            user_input = int(user_input)
        except ValueError:
            user_input = user_input.lower()
        finally:
            if user_input not in options:
                print(on_error)

    return user_input