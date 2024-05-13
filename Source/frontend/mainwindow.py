from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from frontend.device_discovery_widget import DeviceDiscoveryWidget
from frontend.device_info_widget import DeviceInfoWidget
from frontend.analysis_progress_widget import AnalysisProgressWidget
from frontend.results_dashboard_widget import ResultsDashboardWidget

class MainWindow(QMainWindow):
    start_analysis_requested = pyqtSignal()
    stop_analysis_requested = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.device_discovery_widget = None
        self.device_info_widget = None
        self.analysis_progress_widget = None
        self.results_dashboard_widget = None
        self.analysis_started = False

        self.setWindowTitle("Analisi minacce alla sicurezza Android")
        self.resize(413, 268)
        self.center()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.title_label = QLabel("Dispositivo individuato")
        title_font = QFont()
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.layout.addWidget(self.title_label)
        self.title_label.hide()

        self.device_info_widget = DeviceInfoWidget("", "")
        self.layout.addWidget(self.device_info_widget)
        self.device_info_widget.hide()

        self.analysis_button = QPushButton("Analisi")
        self.analysis_button.clicked.connect(self.on_click_button_analysis)
        self.setAnalysisButtonStyle()
        self.layout.addWidget(self.analysis_button)

        self.show_usb_popup()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2

        self.move(int(x), int(y))

    #def resizeEvent(self, event):
    #    window_size = event.size()
    #    print("Dimensione finestra: {}x{}".format(window_size.width(), window_size.height()))
    #    super().resizeEvent(event)

    def setAnalysisButtonStyle(self):
        if not self.analysis_started:
            self.analysis_button.setText("Avvia Analisi")
            self.analysis_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    border: none;
                    color: white;
                    padding: 10px 20px;
                    text-align: center;
                    font-size: 16px;
                    border-radius: 5px;
                }
                
                QPushButton:hover {
                    background-color: #45a049;
                }
                
                QPushButton:pressed {
                    background-color: #357a38;
                }
            """)
        else:
            self.analysis_button.setText("Interrompi Analisi")
            self.analysis_button.setStyleSheet("""
                QPushButton {
                    background-color: #FF5733;
                    border: none;
                    color: white;
                    padding: 10px 20px;
                    text-align: center;
                    font-size: 16px;
                    border-radius: 5px;
                }
                
                QPushButton:hover {
                    background-color: #E64A19;
                }
                
                QPushButton:pressed {
                    background-color: #FF5733;
                }
            """)

    def show_usb_popup(self):
        self.device_discovery_widget = DeviceDiscoveryWidget()
        self.layout.addWidget(self.device_discovery_widget)

        self.device_discovery_widget.show()
        self.analysis_button.hide()

    def show_device_info(self, device_brand, device_model, device_android_model, device_battery_status):
        self.title_label.show()

        self.device_info_widget.set_infos(device_brand, device_model, device_android_model, device_battery_status)
        self.device_info_widget.display_device_info()
        self.device_info_widget.show()

        spacer_item = QSpacerItem(0, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer_item)

        self.analysis_button.show()
        self.device_discovery_widget.hide()

    def on_click_button_analysis(self):
        if not self.analysis_started:
            self.start_analysis()
        else:
            self.ask_stop_analysis()

    def start_analysis(self):
        self.analysis_started = True
        self.setAnalysisButtonStyle()

        self.analysis_progress_widget = AnalysisProgressWidget()
        self.layout.addWidget(self.analysis_progress_widget)
        self.start_analysis_requested.emit()

    def ask_stop_analysis(self):
        reply = QMessageBox.question(self, "Conferma",
                                     "Sei sicuro di voler interrompere l'analisi?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.stop_analysis()

    def stop_analysis(self):
        self.analysis_started = False
        self.setAnalysisButtonStyle()

        self.analysis_progress_widget.hide()
        self.stop_analysis_requested.emit()

    def update_extraction_package_name(self, package):
        self.analysis_progress_widget.update_extraction_package_name(package)

    def update_analyzing_package_name(self, package):
        self.analysis_progress_widget.update_analyzing_package_name(package)

    def update_progress_widget(self, progress):
        self.analysis_progress_widget.update_progress(progress)

    def show_results_dashboard(self, global_security_score, severity_count_by_package, vulnerabilities_list, package_list):
        self.results_dashboard_widget = ResultsDashboardWidget()
        self.results_dashboard_widget.create_pie_chart(global_security_score)
        self.results_dashboard_widget.create_stacked_chart(severity_count_by_package)
        self.results_dashboard_widget.create_vulnerabilities_list(vulnerabilities_list)
        self.results_dashboard_widget.create_package_list(package_list)
        self.results_dashboard_widget.show()
