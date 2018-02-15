from src.blacklist import Blacklist


def run_blacklist_check(directory, child=False):
    if child:
        return bool(Blacklist.of_entry(directory))
    else:
        return bool(Blacklist.is_entry(directory, inverted=True))