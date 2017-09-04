import os

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

def get_config_file_location():
    directory = os.path.dirname(__file__)

    def file_index(path):
        file_list = []
        for root, dirs, files in os.walk(path):
                for _file in files:
                    file_list.append(os.path.join(root, _file))
        return file_list

    if directory.endswith("src"):
        directories = file_index(os.path.dirname(directory))
    else:
        directories = file_index(directory)
    # TODO: remove hard-code in main build, just for finder to run quicker on this method
    for file in list(directories):
        if ".git" in file:
            directories.remove(file)
        if ".idea" in file:
            directories.remove(file)
        else:
            continue

    for file in list(directories):
        if os.path.split(file)[1] == "config.yml":
            return file
        else:
            pass
