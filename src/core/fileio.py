import ast, os, json
from src.core.config import *


def check_file(path):
    return os.path.isfile(path)

def file_size(file, unit=1):
        return os.path.getsize(file) / unit



def get_filename(path, rp=False):
    split_path = os.path.split(path)
    return split_path if rp else split_path[1]


class File:
    def __init__(self, file):
        self.application_root = Config.get("application_root")
        self.application_dirs = Config.get("application_directories.dirs")
        self.files = Config.get("application_directories.temp")
        self.file = file
        self.data = ""

    def _do_safe_create(self):
        file = get_filename(self.file, rp=True)

        if get_filename(file[0], rp=True)[1] in self.application_dirs:
            if file[1] in Config.get('application_directories.temp'):
                self.create()
                return True

            else:
                return 0
        else:
            return -1

    def setup_directories(self):
        for directory in self.application_dirs:
            try:
                os.mkdir(os.path.join(self.application_root, directory))
            except FileExistsError:
                pass

    def setup_files(self):
        for application_dir in self.application_dirs:
            if application_dir == "temp":
                for _file in self.files:
                    self.file = os.path.join(self.application_root, application_dir, _file)
                    self.create()
        self.file = Config.join('application_root', 'blacklist.location')
        self.create()

    def clean_files(self):
        for file in self.files:
            with open(os.path.join(self.application_root, 'temp', file), "w") as f:
                f.flush(), f.truncate(), f.close()

    def clean(self):
        if check_file(self.file):
            self.write('')
        else:
            if self._do_safe_create() < 1:
                error_info = {'e_type': 'file+error', 'object': {self.file}}
                return simple_error('system requested clean-up of unrecognised file.', try_recovery=True,
                                    info=error_info)

    def write(self, data, ):
        if not check_file(self.file):
            return 0
        else:
            with open(self.file, "w") as f:
                f.write(str(data)), f.close()

    def write_json(self, data, indent=4):
        with open(self.file, "w") as f:
            json.dump(data, f, indent=indent)
            f.close()

    def read_json(self):
        if not check_file(self.file):
            return None

        with open(self.file, "r") as f:
            data = json.load(f)
            f.close()

        return {} if data is None else data

    def read(self, specific):

        if not check_file(self.file):
            if get_filename(self.file) in Config.get('application_directories.temp'):
                self.create()

            return None

        with open(self.file, 'r') as f:
            if f.read() == '':
                f.close()
                return None

        with open(self.file, "r") as f:
            try:
                self.data = f.read()
            except SyntaxError:
                if specific is "list":
                    return []
                else:
                    return {}
            finally:
                f.close()
            if specific in ["dict", "list"]:
                return ast.literal_eval(self.data)
            else:
                return self.data

    def remove(self):
        os.remove(self.file)

    def create(self):
        try:
            open(self.file, mode='w')

        except FileNotFoundError:
            if not os.path.exists(self.application_root):
                Fatal(f"improper configuration, application_root='{self.application_root}' does not exist").stop()
