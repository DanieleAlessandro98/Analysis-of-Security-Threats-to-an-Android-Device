import os
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices

class VulnerabilitiesAnalysisList(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Titolo", "OWASP Mobile Top 10", "OWASP MASVS", "Reindizzamento"])

        layout.addWidget(self.table)

        self.setLayout(layout)

    def create_vulnerabilities_list(self, vulnerabilities_list):
        self.table.setRowCount(len(vulnerabilities_list))

        for row, vulnerability in enumerate(vulnerabilities_list):
            formatted_title = self.format_title(vulnerability['title'])
            title_item = QTableWidgetItem(formatted_title)
            owasp_mobile = QTableWidgetItem(vulnerability.get('owasp-mobile', ''))
            masvs = QTableWidgetItem(vulnerability.get('masvs', ''))
            button = QPushButton("Maggiori info")
            button.clicked.connect(lambda _, ref=vulnerability['ref']: self.open_link(ref))

            self.table.setItem(row, 0, title_item)
            self.table.setItem(row, 1, owasp_mobile)
            self.table.setItem(row, 2, masvs)
            self.table.setCellWidget(row, 3, button)

        self.table.resizeColumnsToContents()

    def format_title(self, title):
        title = title[1]
        words = title.split('_')
        formatted_title = ' '.join(word.capitalize() for word in words)
        return formatted_title

    def open_link(self, url):
        QDesktopServices.openUrl(QUrl(url))

