__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


def largest_element(arr):
    return len(max(arr, key=len))


def find_element(arr, case):
    for element in arr:
        if case in element or case == element:
            return int(arr.index(element))
        else:
            continue


def to_string(int_list):
    return [str(i) for i in int_list]


def to_integer(str_list):
    try:
        return [int(i) for i in str_list]

    except ValueError:
        return str_list


def sizeof_fmt(num, suffix="b"):
    if num < 1024.0:
        return [num, "0bytes"]
    for unit in [" ", "K", "M", "G", "T", "P"]:
        if abs(num) < 1024.0:
            return [num,"%3.1f%s%s" % (num, unit, suffix)]

        num /= 1024.0
    return [num ,"%.1f%s%s" % (num, 'E', suffix)]


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


def swap_extension(file, ext, remove_dot=False):
    return file[:-4] + ext if remove_dot else file[:-3] + ext