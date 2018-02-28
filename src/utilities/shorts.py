import os
import re

from src.core.exceptions import *
from src.utilities.arrays import center_array

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


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
    # print(path)
    chunks = path.split(separator)
    usable_chunks = chunks[2:-1]  # parts of the directory which can be used to shorten the overall path

    def simple_shorten(overflow_size):
        # if the list length was even, the center is duplicated (thus it needs to be cut in half)
        if centered_list[0] == centered_list[1]:
            centered_list.pop(0)

        # initial selection for candidates to be removed
        for position in centered_list:
            # print(overflow_size, position)
            if overflow_size > 0:
                replace_chunks.append(position)
                overflow_size -= len(position)
            elif overflow_size <= 0:
                break
        # print(replace_chunks)
        if overflow_size > 0:
            pass
        # print(replace_chunks)
        for _chunk in replace_chunks:
            if chunk_replacer not in chunks:
                chunks.insert(chunks.index(_chunk), chunk_replacer)
            chunks.remove(_chunk)

    # print('centered: %s\n useable: %s\n chunks: %s' % (centered_list, usable_chunks, chunks))
    if len(usable_chunks) < 1:
        usable_chunks = chunks[1:-1]

    centered_list = center_array(usable_chunks)
    simple_shorten(overflow)

    for chunk in replace_chunks:
        if chunk_replacer not in chunks:
            chunks.insert(chunks.index(chunk), chunk_replacer)
            chunks.remove(chunk)

    return separator.join(chunks)


def global_get(data, req):
    keys = req.split('.')
    quote_keys = re.compile(r"\.\'([^\']*)\'").findall(req)

    # parse and fix-up the req
    for pos, key in enumerate(keys):
        if key == "'":
            keys.pop(pos)
            keys[pos] = quote_keys[0]

            quote_keys.pop(0)

    # extract data from the dict now
    for key in keys:
        if key in data.keys():
            data = data.get(key)
        else:
            raise Fatal('Unreadable information', 'key was not found, but expected',
                        'key=\'%s\'' % req, 'given_data:', data)

    # try first return keys, if non-existent just return data
    try:
        return data.keys()
    except AttributeError:
        return data
