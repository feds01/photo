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


def query_user(message, options):
    user_input = ''
    while user_input not in options:
        user_input = input(message).lower()
    return user_input


def swap_extension(file, ext, remove_dot=False):
    return file[:-4] + ext if remove_dot else file[:-3] + ext