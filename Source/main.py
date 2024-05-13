import sys
import utils
from PyQt5.QtWidgets import QApplication

from frontend.mainwindow import MainWindow
from backend.device_discovery import DeviceDiscovery
from backend.apk_extractor import ApkExtractor
from backend.apk_analyzer import ApkAnalyzer
from errors import NoDeviceError, NoApplicationError, AnalyzerError, InvalidFolderError

class Main():
    def __init__(self, windows):
        self.window = window

        self.device_discovery = DeviceDiscovery()
        self.apk_extractor = ApkExtractor()
        self.apk_analyzer = ApkAnalyzer()

        self.bind_signals()

    def bind_signals(self):
        self.device_discovery.signal.connect(self.completed_device_detection)

        self.apk_extractor.current_package_signal.connect(self.update_apk_extraction_package_name)
        self.apk_extractor.progress_signal.connect(self.update_apk_extraction_progress)
        self.apk_extractor.completed_signal.connect(self.completed_apk_extraction)

        self.apk_analyzer.current_package_signal.connect(self.update_apk_analyzing_package_name)
        self.apk_analyzer.progress_signal.connect(self.update_apk_analyzing_progress)
        self.apk_analyzer.completed_signal.connect(self.completed_apk_analyzing)

        self.window.start_analysis_requested.connect(self.extract_apk)
        self.window.stop_analysis_requested.connect(self.stop_analysis)

    def start(self):
        self.device_discovery.start()

    def stop_analysis(self):
        self.apk_extractor.stop_analysis()
        self.apk_analyzer.stop_analysis()

    def completed_device_detection(self, result):
        if result == True:
            self.window.show_device_info(
                self.device_discovery.get_device_brand(),
                self.device_discovery.get_device_model(),
                self.device_discovery.get_device_android_version(),
                self.device_discovery.get_device_battery_status(),
                )

    def extract_apk(self):
        self.apk_extractor.start()

    def update_apk_extraction_package_name(self, package):
        self.window.update_extraction_package_name(package)

    def update_apk_extraction_progress(self, progress):
        self.window.update_progress_widget(progress)

    def completed_apk_extraction(self):
        self.window.update_progress_widget(0)
        self.apk_analyzer.start()

    def update_apk_analyzing_package_name(self, package):
        self.window.update_analyzing_package_name(package)
        
    def update_apk_analyzing_progress(self, progress):
        self.window.update_progress_widget(progress)

    def completed_apk_analyzing(self, global_security_score, severity_count_by_package, vulnerabilities_list, package_list):
        self.window.show_results_dashboard(global_security_score, severity_count_by_package, vulnerabilities_list, package_list)

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)

        window = MainWindow()
        main = Main(window)

        main.start()

        window.show()
        sys.exit(app.exec_())

    except NoDeviceError:
        print("Nessun dispositivo trovato.")
    except NoApplicationError:
        print("Nessuna applicazione trovata.")
    except AnalyzerError as e:
        print(f"Errore: {e}")
    except InvalidFolderError as e:
        print(f"Errore: {e}")
    except Exception as e:
        print(f"Errore generico: {e}")
