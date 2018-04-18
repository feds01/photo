from src.core.core import *
from src.utilities.codes import *
from src.utilities.infrequents import open_file
from src.utilities.manipulation import sizeof_fmt, query_user

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

total_saved_space = 0


def analyse(path):
    to_remove = []
    option = ""

    info = Directory(path).index_photo_directory(return_folders=True)
    files = [x for x in filter(lambda x: x not in index(info.get("good"), file=True), index(info.get("all"), file=True))]
    crt_files = index(info.get('crt'), file=True)

    for file in files:
        extensions = [(os.path.join(info.get("crt"), os.path.split(file)[1][:-4] + x)) for x in Config.get("file_extensions.crt")]

        to_remove.extend([e for e in extensions if e in crt_files])

    # filter by user preference
    for file in to_remove:
        print("use 'open' to open the current file\nuse 'stop' to abort operation\n")

        while True and option != "stop":
            option = query_user(f"Delete the file {file} ? ", ["y", "n", "open", "close", "abort"])

            if option == "n":
                to_remove.remove(file)
                break
            elif option == "open":
                open_file(file)
            else:
                break

        if option == "stop":
            return DELETE_ABORT

    return to_remove


def delete_file(file):
    global total_saved_space

    size = file_size(file)

    if not Config.get("verbose"):
        file_info = sizeof_fmt(size)
        print(f"deleting: {os.path.basename(file)} size: {str(file_info[1])}")

    try:
        os.remove(file)

    except Exception as e:
        Fatal(f"could not remove file {file}", 'error=%s' % e)
        return DELETE_FILE_FAIL

    finally:
        total_saved_space -= size
        return DELETE_FILE_SUCCESS


def delete_items(files):
    global total_saved_space

    # use canceled operation
    if files == DELETE_ABORT:
        return DELETE_ABORT

    else:
        total_saved_space = sum(list(map(lambda x: file_size(x), files)))

        file_status = [delete_file(x) for x in files]

        total_saved_space = sizeof_fmt(total_saved_space)
        print(f"saved: {total_saved_space[1]} of disk space with operation.")
        print(f"failed to delete {file_status.count(DELETE_FILE_FAIL)} items.")

        return DELETE_SUCCESS
