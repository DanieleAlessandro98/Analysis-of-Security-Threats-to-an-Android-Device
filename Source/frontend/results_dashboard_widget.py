from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtGui import *

from frontend.package_analysis_details_widget import PackageAnalysisDetailsWidget
from frontend.custom_elements.vulnerabilities_analysis_table_list import VulnerabilitiesAnalysisList
from frontend.custom_elements.stacked_bar_chart import StackedBarChart

import sys

class ResultsDashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Risultato Analisi")
        self.resize(1000, 600)

        self.main_layout = QHBoxLayout(self)

        self.menu_frame = QFrame(self)
        self.menu_frame.setStyleSheet("QFrame { background-color: #ecf0f1; border: 2px solid #bdc3c7; border-radius: 5px; }")
        self.menu_frame.setFrameShape(QFrame.StyledPanel)
        self.menu_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.menu_layout = QVBoxLayout(self.menu_frame)

        self.dashboard_button = QPushButton("Dashboard")
        self.dashboard_button.setStyleSheet("QPushButton { background-color: #3498db; color: white; border: 2px solid #2980b9; border-radius: 5px; }")
        self.dashboard_button.clicked.connect(self.show_dashboard)
        self.menu_layout.addWidget(self.dashboard_button)

        self.vulnerabilities = QPushButton("Vulnerabilità")
        self.vulnerabilities.setStyleSheet("QPushButton { background-color: #3498db; color: white; border: 2px solid #2980b9; border-radius: 5px; }")
        self.vulnerabilities.clicked.connect(self.show_vulnerabilities)
        self.menu_layout.addWidget(self.vulnerabilities)

        self.detail_button = QPushButton("Dettagli")
        self.detail_button.setStyleSheet("QPushButton { background-color: #2ecc71; color: white; border: 2px solid #27ae60; border-radius: 5px; }")
        self.detail_button.clicked.connect(self.show_detail)
        self.menu_layout.addWidget(self.detail_button)




        self.dashboard_content = QWidget(self)
        self.dashboard_layout = QVBoxLayout(self.dashboard_content)

        self.overview_label = QLabel("Overview", self)
        self.overview_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.dashboard_layout.addWidget(self.overview_label)

        self.pie_chart_view = QChartView()
        self.dashboard_layout.addWidget(self.pie_chart_view)

        self.stacked_bar_chart = StackedBarChart()
        self.stacked_bar_chart.order_combo_box.currentIndexChanged.connect(self.update_stacked_bar_chart)
        self.dashboard_layout.addWidget(self.stacked_bar_chart)






        self.detail_content = QWidget(self)
        self.detail_layout = QVBoxLayout(self.detail_content)

        self.package_analisys_details_widget = PackageAnalysisDetailsWidget()
        self.detail_layout.addWidget(self.package_analisys_details_widget)








        self.vulnerabilities_content = QWidget(self)
        self.vulnerabilities_layout = QVBoxLayout(self.vulnerabilities_content)

        self.vulnerabilities_analisys_widget = VulnerabilitiesAnalysisList()
        self.vulnerabilities_layout.addWidget(self.vulnerabilities_analisys_widget)





        self.main_layout.addWidget(self.menu_frame)
        self.main_layout.addWidget(self.dashboard_content)
        self.main_layout.addWidget(self.vulnerabilities_content)
        self.main_layout.addWidget(self.detail_content)


        self.show_dashboard()

    def create_pie_chart(self, global_security_score):
        max_value = 100
        value = global_security_score

        percentage = (value / max_value) * 100

        series = QPieSeries()
        series.append(f"Valore: {value}", percentage)
        series.append(f"Rimanente: {max_value - value}", 100 - percentage)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Punteggio di sicurezza globale")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        series.setHoleSize(0.5)

        slice_item = series.slices()[0]
        slice_item.setLabelVisible()
        slice_item.setLabel(f"{value}/{max_value}")
        if value <= 15:
            slice_item.setColor(QColor("#FF0000"))  # Rosso forte per CRITICAL
        elif value <= 40:
            slice_item.setColor(QColor("#FFA07A"))  # Rosso per HIGH
        elif value <= 70:
            slice_item.setColor(QColor("#FFA500"))  # Arancione per MEDIUM
        else:
            slice_item.setColor(QColor("#008000"))  # Verde per LOW

        slice_item = series.slices()[1].setBrush(QColor("#CCCCCC"))

        chart.legend().setVisible(False)

        self.pie_chart_view.setChart(chart)




    def create_stacked_chart(self, severity_count_by_package):
        categories = list(severity_count_by_package.keys())
        values_high = [severity_count_by_package[package_name]['high'] for package_name in categories]
        values_warning = [severity_count_by_package[package_name]['warning'] for package_name in categories]
        values_info = [severity_count_by_package[package_name]['info'] for package_name in categories]
        values_secure = [severity_count_by_package[package_name]['secure'] for package_name in categories]
        
        ## ordinamento 1
        sum_values = {}
        for cat, crit, high, med, low in zip(categories, values_high, values_warning, values_info, values_secure):
            sum_values[cat] = crit + high + med + low

        sorted_categories1 = sorted(categories, key=lambda cat: sum_values[cat], reverse=False)

        sorted_values_high1 = [values_high[categories.index(cat)] for cat in sorted_categories1]
        sorted_values_warning1 = [values_warning[categories.index(cat)] for cat in sorted_categories1]
        sorted_values_info1 = [values_info[categories.index(cat)] for cat in sorted_categories1]
        sorted_values_secure1 = [values_secure[categories.index(cat)] for cat in sorted_categories1]


        ## ordinamento 2
        sorted_categories2 = sorted(categories, key=lambda cat: sum_values[cat], reverse=False)
        sorted_categories_values = sorted(zip(sorted_categories2, values_high, values_warning, values_info, values_secure), key=lambda x: x[1], reverse=False)

        sorted_categories2, sorted_values_high2, sorted_values_warning2, sorted_values_info2, sorted_values_secure2 = zip(*sorted_categories_values)


        values_groups1 = [sorted_values_high1, sorted_values_warning1, sorted_values_info1, sorted_values_secure1]
        values_groups2 = [sorted_values_high2, sorted_values_warning2, sorted_values_info2, sorted_values_secure2]

        colors = ['#FF0000', '#FFA500', '#FFD700', '#00A000']

        group_labels = ['HIGH', 'WARNING', 'INFO', 'SECURE']

        self.stacked_bar_chart.sorted_categories1 = sorted_categories1
        self.stacked_bar_chart.values_groups1 = values_groups1
        self.stacked_bar_chart.colors1 = colors
        self.stacked_bar_chart.group_labels1 = group_labels

        self.stacked_bar_chart.sorted_categories2 = sorted_categories2
        self.stacked_bar_chart.values_groups2 = values_groups2
        self.stacked_bar_chart.colors2 = colors
        self.stacked_bar_chart.group_labels2 = group_labels

        self.stacked_bar_chart.update_chart_with_order(self.stacked_bar_chart.order_combo_box.currentIndex())


    def create_vulnerabilities_list(self, vulnerabilities_list):
        self.vulnerabilities_analisys_widget.create_vulnerabilities_list(vulnerabilities_list)

    def create_package_list(self, package_list):
        self.package_analisys_details_widget.create_package_list(package_list)

    def show_dashboard(self):
        self.overview_label.show()
        self.pie_chart_view.show()
        self.stacked_bar_chart.show()
        self.vulnerabilities_analisys_widget.hide()
        self.package_analisys_details_widget.hide()

    def show_detail(self):
        self.overview_label.hide()
        self.pie_chart_view.hide()
        self.stacked_bar_chart.hide()
        self.vulnerabilities_analisys_widget.hide()
        self.package_analisys_details_widget.show()

    def show_vulnerabilities(self):
        self.overview_label.hide()
        self.pie_chart_view.hide()
        self.stacked_bar_chart.hide()
        self.vulnerabilities_analisys_widget.show()
        self.package_analisys_details_widget.hide()

    def update_stacked_bar_chart(self, index):
        self.stacked_bar_chart.update_chart_with_order(index)
