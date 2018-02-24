from src.core.core import *
from src.utilities.infrequents import open_file
from src.utilities.manipulation import sizeof_fmt

__author__ = "Alexander Fedotov <alexander.fedotov.uk@gmail.com>"
__company__ = "(C) Wasabi & Co. All rights reserved."

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
            option = query_user(f"Delete the file {file} ? ", ["y", "n", "open", "close"])

            if option == "n":
                to_remove.remove(file)
                break
            elif option == "open":
                open_file(file)
            else:
                break

        if option == "stop":
            print("aborted operation")
            return []

    return to_remove

class Delete:
    def __init__(self, to_delete):
        self.to_delete = to_delete
        self.total_size = 0
        self.file_path = ""

    def calculate_size(self):
        for file in self.to_delete:
            self.total_size += file_size(file)

    def delete_file(self):
        size = file_size(self.file_path)

        if not Config.get_session("verbose"):
            file_info = sizeof_fmt(size)
            print(f"deleting: {os.path.basename(self.file_path)} size: {str(file_info[1])}")

        try:
            os.remove(self.file_path)

        except Exception as e:
            Fatal(f"could not remove file {self.file_path}", 'error=%s' % e)

        finally:
            self.total_size -= size

    def deletion_manager(self):
        self.calculate_size()
        for file in self.to_delete:
            self.file_path = file
            self.delete_file()
        self.total_size = sizeof_fmt(self.total_size)
        print(f"saved: {self.total_size[1]} of disk space with operation.")
        return True
