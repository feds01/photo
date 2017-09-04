def query_user(message, options):
    user_input = ''
    while user_input not in options:
        user_input = input(message).lower()
    return user_input


def join_lists(*lists):
    joined_list: list = []

    if len(lists) == 1:
        return lists

    else:
        for element_list in lists:
            joined_list.extend(element_list)
        return joined_list


def organise_list(_list):
    unorganised_list: list = [x for x in _list if x]
    organised_list:   list = []

    for element in unorganised_list:
        if type(element) == list:
            organised_list.extend(element)
        else:
            organised_list.append(element)

    return organised_list

