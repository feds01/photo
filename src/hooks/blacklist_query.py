from src.blacklist import Blacklist


def run_blacklist_check(directory):
    return bool(Blacklist.check_entry_existence(directory, inverted=True))