import os
from adbutils import adb, AdbTimeout
from PyQt5.QtCore import QThread, pyqtSignal

import utils
from errors import NoDeviceError
from errors import NoApplicationError

class ApkExtractor(QThread):
    current_package_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    completed_signal = pyqtSignal()

    def run(self):
        utils.create_folder(utils.PACKAGE_FOLDER)
        self.device = adb.device()
        self.stopped = False

        self.extract_apks()

    def stop_analysis(self):
        self.stopped = True

    def get_installed_packages_list(self):
        if not self.device:
            return None

        packages_list = self.device.shell('pm list packages -3 | tr -d "\r" | sed "s/package://g"')
        if not packages_list:
            return None

        print(packages_list)
        return packages_list.strip().splitlines()

    def get_installed_package_path(self, package):
        package_file_path = self.device.shell(f'pm path {package} | grep "base.apk" | tr -d "\r" | sed "s/package://g"')
        if package_file_path:
            print(package_file_path.strip().split(":")[-1].strip())
            return package_file_path.strip().split(":")[-1].strip()

        return None

    def pull_packages(self, packages):
        total_packages = len(packages)
        completed_packages = 0
        
        for package in packages:
            if self.stopped:
                break

            self.current_package_signal.emit(package.strip())
            self.pull_package(package)
            completed_packages += 1
            self.progress_signal.emit(int(completed_packages / total_packages * 100))

        self.completed_signal.emit()

    def pull_package(self, package):
        if self.stopped:
            return

        package = package.strip()
        if package:
            package_file_path = self.get_installed_package_path(package)

            if package_file_path:
                self.device.sync.pull(package_file_path, utils.get_package_output_path(f"{package}.apk"))

    def extract_apks(self):
        packages = self.get_installed_packages_list()
        if not packages:
            raise NoApplicationError()

        self.pull_packages(packages)
