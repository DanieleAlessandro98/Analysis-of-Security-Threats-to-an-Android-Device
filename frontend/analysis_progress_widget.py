from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel
from PyQt5.QtCore import QTimer

class AnalysisProgressWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.status_label = QLabel("Analisi in corso")
        self.layout.addWidget(self.status_label)

        self.progress_label = QLabel("Estrazione APK in corso")
        self.layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.progress_bar.setValue(0)

        self.dot_timer = QTimer()
        self.dot_timer.timeout.connect(self.update_dots)
        self.dot_count = 0
        self.dot_chars = ["", ".", ".", "."]

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_extraction_package_name(self, package):
        self.progress_label.setText(f"Estrazione del pacchetto: {package}")

    def update_analyzing_package_name(self, package):
        self.progress_label.setText(f"Analisi del pacchetto: {package}")
        self.dot_timer.start(1000)

    def update_dots(self):
        if self.dot_count >= len(self.dot_chars):
            self.dot_count = 0
            self.status_label.setText("Analisi in corso")
        else:
            dots = self.dot_chars[self.dot_count]
            current_text = self.status_label.text()
            self.status_label.setText(current_text + dots)
            self.dot_count += 1
