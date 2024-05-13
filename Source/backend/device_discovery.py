from PyQt5.QtCore import QThread, pyqtSignal
from adbutils import adb, AdbTimeout

class DeviceDiscovery(QThread):
    signal = pyqtSignal(bool)

    def run(self):
        self.device = None

        try:
            adb.connect("192.168.89.103:5555", timeout = 3.0)
            self.device = adb.device()
            if self.device != None:
                self.signal.emit(True)
                return
        except AdbTimeout:
            pass

        try:
            self.device = adb.device()
            if self.device != None:
                self.signal.emit(True)
                return
        except Exception:
            self.signal.emit(False)

    def get_device_brand(self):
        return self.device.prop.get('ro.product.brand')

    def get_device_model(self):
        return self.device.prop.get('ro.product.model')

    def get_device_android_version(self):
        return self.device.prop.get('ro.build.version.release')

    def get_device_battery_status(self):
        return self.device.shell("dumpsys battery | grep 'level' | sed 's/level: //' | sed 's/$/%/'")