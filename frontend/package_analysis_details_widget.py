import os
import webbrowser
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *

import utils

class PackageAnalysisDetailsWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Applicazione", "Punteggio di sicurezza", "Dettagli"])

        layout.addWidget(self.table)

        self.setLayout(layout)

    def create_package_list(self, package_dict):
        self.table.setRowCount(len(package_dict))

        row = 0
        for name, score in package_dict.items():
            name_item = QTableWidgetItem(name)
            score_item = QTableWidgetItem(f"{score}/100")
            button = QPushButton("Dettagli")
            button.clicked.connect(lambda _, name=name: self.open_file(name))

            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, score_item)
            self.table.setCellWidget(row, 2, button)

            row += 1
        
        self.table.resizeColumnsToContents()

    def open_file(self, name):
        filename = os.path.join(utils.SCAN_RESULT_FOLDER, f"{name}.pdf")
        if os.path.exists(filename):
            webbrowser.open(filename)
        else:
            QMessageBox.warning(self, "File non trovato", f"Il file {filename} non è stato trovato.")
