__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


def organise_array(arr):
    if arr is None:
        return []

    organised_list:   list = []

    for element in arr:
        if type(element) == list:
            organised_list.extend(organise_array(element))
        else:
            organised_list.append(element)

    return organised_list


def __array_center(arr):
    middle = float(len(arr))/2
    return [middle - 0.5, middle - 0.5] if middle % 2 != 0 else [middle - 1, middle]


def center_array(arr):
    i = 0
    center = to_integer(__array_center(arr)) # returns theoretical positions
    split_object = (list(reversed(arr[:center[0]])), arr[1 + center[1]:])
    # print('arr: %s' % arr)
    centered_array = [arr[center[0]], arr[center[1]]]

    for _ in split_object[0]:
        centered_array.append([split_object[0][i], split_object[1][i]])
        i += 1

    return organise_array(centered_array)


def largest_element(arr):
    return max(arr, key=len)


def to_string(int_list):
    return [str(i) for i in int_list]


def to_integer(str_list):
    try:
        return [int(i) for i in str_list]

    except ValueError:
        return str_list