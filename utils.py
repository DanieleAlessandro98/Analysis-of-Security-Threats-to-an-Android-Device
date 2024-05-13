import os
import shutil

from errors import InvalidFolderError

OUTPUT_FOLDER = "output"
PACKAGE_FOLDER = os.path.join(OUTPUT_FOLDER, "apk_folder")
SCAN_RESULT_FOLDER = os.path.join(OUTPUT_FOLDER, "scan_result")

def create_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    os.makedirs(folder_path)

def get_package_files():
    if not os.path.exists(PACKAGE_FOLDER) or not os.path.isdir(PACKAGE_FOLDER):
        raise InvalidFolderError(f"La cartella {PACKAGE_FOLDER} non esiste o non è una directory valida.")

    package_files = [f for f in os.listdir(PACKAGE_FOLDER) if f.endswith(".apk")]

    if not package_files:
        raise InvalidFolderError(f"La cartella {PACKAGE_FOLDER} è vuota.")

    return package_files

def get_package_output_path(package):
    return os.path.join(PACKAGE_FOLDER, package)
