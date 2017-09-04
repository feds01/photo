def get_largest_element(arr):
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

