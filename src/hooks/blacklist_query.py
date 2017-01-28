from src.blacklist import Blacklist


def run_blacklist_check(directory, child=False):
    if child:
        return bool(Blacklist.check_child_entry(directory))
    else:
        return bool(Blacklist.check_entry_existence(directory, inverted=True))