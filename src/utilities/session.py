import os

from src.core.fileio import File, Config, check_file
from src.utilities.arrays import organise_array

root = Config.get("application_root")
artifacts = {"session": Config.get("session"), "blacklist": Config.get("blacklist.location")}
file = File()

def open_session():
    for key in artifacts.keys():
        artifact = os.path.join(root, artifacts.get(key))

        file.set_file(artifact)

        # if file does not exist write an empty json to it
        if not check_file(artifact):
            file.write_json({})

        # write session settings to session file
        if key == "session":
            file.write_json({"session": Config.session}, indent=None)


def close_session(jobs=None):
    for key in artifacts.keys():
        artifact = os.path.join(root, artifacts.get(key))

        file.set_file(artifact)

        # if file does not exist write an empty json to it
        if not check_file(artifact):
            file.write_json({})
        # write session settings to session file
        if key == "session":
            file.write_json({}, indent=None)

        if key == "blacklist" and not jobs is None:
            info = file.read_json()
            data = []

            try:
                data = organise_array(info.get("completed"))
                data.extend(jobs)
            except KeyError:
                data = jobs
            finally:
                info.update({"completed": data})
                file.write_json(info)
    exit()