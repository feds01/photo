import os
from src.core.exceptions import *
from src.utilities.arrays import center_array


def __path_size(path, include_sep, separator):
    return len(path) if include_sep else sum([len(chunk) for chunk in path.split(separator)])


def shorten(path, max_len=30, sep_char=False, separator=os.sep):
    chunk_replacer: str = '...'
    replace_chunks: list = []
    centered_list: list = []
    chunks: list = []
    # print('path_len: %s' % len(path))
    # initial analysis
    overflow = (__path_size(path, sep_char, separator) - max_len) + len(chunk_replacer)
    # print('overflow: %s' % overflow)
    # is actual path overflowing
    if overflow <= 0:
        return path
    # begin processing path
    #print(path)
    chunks = path.split(separator)
    usable_chunks = chunks[2:-1]  # parts of the directory which can be used to shorten the overall path

    def simple_shorten(overflow_size):
        # if the list length was even, the center is duplicated (thus it needs to be cut in half)
        if centered_list[0] == centered_list[1]:
            centered_list.pop(0)

        # initial selection for candidates to be removed
        for position in centered_list:
            #print(overflow_size, position)
            if overflow_size > 0:
                replace_chunks.append(position)
                overflow_size -= len(position)
            elif overflow_size <= 0:
                break
        #print(replace_chunks)
        if overflow_size > 0:
            pass
        #print(replace_chunks)
        for chunk in replace_chunks:
            if not chunk_replacer in chunks:
                chunks.insert(chunks.index(chunk), chunk_replacer)
            chunks.remove(chunk)

    #print('centered: %s\n useable: %s\n chunks: %s' % (centered_list, usable_chunks, chunks))
    if len(usable_chunks) < 1:
        usable_chunks = chunks[1:-1]

    centered_list = center_array(usable_chunks)
    simple_shorten(overflow)

    for chunk in replace_chunks:
        if not chunk_replacer in chunks:
            chunks.insert(chunks.index(chunk), chunk_replacer)
            chunks.remove(chunk)

    return separator.join(chunks)


def global_get(data_structure, req):
    keys = []
    pos = 0
    found_dot = False
    while True:
        if pos > len(req) - 1:
            break
        else:
            symbol = req[pos]

        if req[0] == "'" and not found_dot:
            pos = (req[1:]).index("'")
            keys.append(req[1: pos + 1])
            found_dot = True

        if symbol == '.':
            if not found_dot:
                keys.append(req[0: pos])
                found_dot = True

            if req[pos + 1] == "'":
                pos += 2
                o_pos = pos
                symbol = ''
                while symbol != "'":
                    if pos > len(req) - 1:
                        keys.append(req[o_pos: pos])
                        break
                    else:
                        symbol = req[pos]
                        if symbol == "'":
                            keys.append(req[o_pos: pos])
                    pos += 1

            else:
                symbol = ''
                pos += 1
                o_pos = pos
                while symbol != '.':
                    if pos > len(req) - 1:
                        keys.append(req[o_pos: pos])
                        break
                    else:
                        symbol = req[pos]
                        if symbol == '.':
                            keys.append(req[o_pos: pos])
                    pos += 1
                pos -= 1
        else:
            pos += 1

    if len(keys) == 0:
        keys.append(req)

    for key in keys:
        if key in data_structure.keys():
            data_structure = data_structure.get(key)
            continue
        else:
            Fatal('Unreadable information', True, 'key was not found, but expected', 'key=%s' % req, 'given_data=%s' % data_structure)
    try:
        return data_structure.keys()
    except:
        return data_structure