from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class DeviceInfoWidget(QWidget):
    def __init__(self, brand, model):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.brand = brand
        self.model = model

    def set_infos(self, brand, model, android_version, battery_status):
        self.brand = brand
        self.model = model
        self.android_version = android_version
        self.battery_status = battery_status

    def display_device_info(self):
        self.layout.addWidget(QLabel(f"Brand: {self.brand}"))
        self.layout.addWidget(QLabel(f"Modello: {self.model}"))
        self.layout.addWidget(QLabel(f"Versione Android: {self.android_version}"))
        self.layout.addWidget(QLabel(f"Stato batteria: {self.battery_status}"))
