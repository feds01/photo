import os

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."


def config_generation():
    with open(get_config_file_location(), "w") as file:
        file.write("""\nfolders:\n   good_folder_name:\n   - \"_Good\"\n   - \"_GOOD\"\n   - \"Good\"\n\
   - \"GOOD\"\n   - \"good\"\n   all_folder_name:\n   - \"_all\"\n   - \"_ALL\"\
  \n   - \"all\"\n   - \"All\"\n   - \"ALL\"\n   crt_folder_name:\n   - \"_DNG\"\n   - \"DNG\"\n
  - \"crt\"\n   - \"CRT\"\n   - \"Crt\"\n   - \"CRT\"\nblacklist:\n\
    enabled: true\n    location: \"artifact\\\\blacklist.txt\"\n\nfile_extensions:\n\
   crt:\n   - \".CR2\"\n   - \".dng\"\n   - \".TIF\"\n   good:\n   - \".jpg\"\n\
  \ndata:\n   index_data: \"temp\\\\photo_directories_data.txt\"\n   table_data: \"\
  temp\\\\table_data.txt\"\n   size_data: \"temp\\\\size_data.txt\"\n   removed_files_data:\
   \"temp\\\\removed_files_data.txt\"\n   completed_directories: \"artifact\\\\completed_directories.txt\"\
  \n"""), file.close()


def check_config_stability():
    pass


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
    # TODO: remove code in main build, just for finder to run quicker on this method
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
