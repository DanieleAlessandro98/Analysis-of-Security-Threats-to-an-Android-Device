import sys
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class StackedBarChart(QWidget):
    def __init__(self):
        super().__init__()
        self.figure = Figure()
        self.figure.subplots_adjust(left=0.2, right=0.9, top=0.95, bottom=0.1)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        layout = QVBoxLayout(self)

        hbox_layout = QHBoxLayout()
        
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hbox_layout.addItem(spacer_item)

        self.order_combo_box = QComboBox()
        self.order_combo_box.addItems(["Ordinamento per numero", "Ordinamento per criticità"])
        hbox_layout.addWidget(self.order_combo_box)
        
        layout.addLayout(hbox_layout)
        layout.addWidget(self.canvas)

    def update_chart_with_order(self, index):
        if index == 0:
            self.update_chart(self.sorted_categories1, self.values_groups1, self.colors1, self.group_labels1)
        elif index == 1:
            self.update_chart(self.sorted_categories2, self.values_groups2, self.colors2, self.group_labels2)


    def set_size(self, width, height):
        self.canvas.setMinimumSize(width, height)
        self.canvas.setMaximumSize(width, height)

    def update_chart(self, categories, values_groups, colors, group_labels, category_spacing=1.3):
        self.ax.clear()

        num_categories = len(categories)
        num_groups = len(values_groups)
        bar_height = 1.7
        total_bar_height = bar_height * num_categories

        y_positions = range(num_categories)

        for i, category in enumerate(categories):
            left = 0
            for j in range(num_groups):
                value = values_groups[j][i]

                bar_width = max(value, 0.11)

                if value == 0:
                    text_x_position = left
                    ha_alignment = 'left'
                else:
                    text_x_position = left + bar_width / 2
                    ha_alignment = 'center'

                self.ax.barh(y_positions[i] + i * category_spacing, bar_width, left=left, height=bar_height, color=colors[j],
                            label=group_labels[j] if i == 0 else None, edgecolor='white')
                
                self.ax.text(text_x_position, y_positions[i] + i * category_spacing, str(value),
                            ha=ha_alignment, va='center', color='black')
                
                left += max(value, 0.11)


        self.ax.set_yticks([i + i * category_spacing for i in y_positions])
        self.ax.set_yticklabels(categories)
        self.ax.set_ylabel('')
        self.ax.set_xlabel('Values')
        self.ax.legend(loc='best')

        self.ax.xaxis.set_visible(False)

        self.ax.set_ylim(-0.5, num_categories - 0.5 + (num_categories - 1) * category_spacing + 0.4)

        self.canvas.draw()
