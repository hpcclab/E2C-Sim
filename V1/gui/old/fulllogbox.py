
from logging.handlers import QueueListener
import statistics
import sys
import json
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QLabel,
    QFrame,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSlider,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QScrollArea,
    QComboBox,
    QLineEdit,
    QDial
)

from PyQt5.QtCore import (Qt,pyqtSignal)
from os import makedirs
import sys
import utils.config as config

# A message box that contains the full logs, can be sort by event type and task id.
class FullLogBox(QMessageBox):
    finished = pyqtSignal()
    def __init__(self, l, ms, title, *args, **kwargs):
        QMessageBox.__init__(self, *args, **kwargs)
        self.task = l
        self.machine_stats = ms
        self.arriving = []
        self.running = []
        self.deferred = []
        self.cancelled = []
        self.dropped = []
        self.completed = []
        self.comboBoxWidget()
        self.searchBarWidget()

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.content = QWidget()
        self.scroll.setWidget(self.content)
        self.lay = QVBoxLayout(self.content)

        for i, item in enumerate(self.task):
            self.lay.addWidget(QLabel("{}. {}".format(i, item), self))

        self.layout().addWidget(self.scroll, 0, 0, 1, self.layout().columnCount())
        self.layout().addWidget(self.comboBox, 1, 0, 1, 1)
        self.layout().addWidget(self.searchbar, 1, 1, alignment=Qt.AlignCenter)
        self.layout().addWidget(self.searchBarButton, 1, 1, alignment=Qt.AlignRight)

        self.setStyleSheet("QScrollArea{min-width:900 px; min-height: 400px}")
        self.setWindowTitle(title)

    def comboBoxWidget(self):
        """
        The function creates a comboBox widget with the following options: All, Arriving tasks, Executed
        tasks, Completed tasks, Deferred tasks, Cancelled tasks, Dropped tasks, Machine Statistics
        """
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("All")
        self.comboBox.addItem("Arriving tasks")
        self.comboBox.addItem("Executed tasks")
        self.comboBox.addItem("Completed tasks")
        self.comboBox.addItem("Deferred tasks")
        self.comboBox.addItem("Cancelled tasks")
        self.comboBox.addItem("Dropped tasks")
        self.comboBox.addItem("Machine Statistics")
        self.comboBox.setFixedWidth(300)
        self.comboBox.activated.connect(self.activated)

    def searchBarWidget(self):
        """
        It creates a search bar widget with a line edit and a button.
        """
        self.searchbar = QLineEdit()
        self.searchbar.setStyleSheet("border: 1px solid black")
        self.searchbar.setFixedWidth(180)
        self.searchbar.setPlaceholderText("Search task id")
        self.searchBarButton = QPushButton("Search")
        self.searchBarButton.clicked.connect(self.searchTask)
        self.searchBarButton.setDefault(True)
        self.searchBarButton.setAutoDefault(False)

    def searchTask(self):
        """
        It takes the text from the searchbar, and if it's not empty, it searches the task list for the
        task id, and if it finds it, it adds it to the layout.
        """
        self.clearLayout()
        if self.searchbar.text():
            for i, item in enumerate(self.task):
                if 'Type' in item and item['Task id'] == int(self.searchbar.text()):
                    self.lay.addWidget(QLabel("{}. {}".format(i, item), self))
        else:
            for i, item in enumerate(self.task):
                self.lay.addWidget(QLabel("{}. {}".format(i, item), self))

    def activated(self, index):
        """
        The function takes in an index, and depending on the index, it will display the corresponding
        information in the QListWidget

        :param index: the index of the activated item in the combobox
        """
        self.clearLayout()
        if index == 0:
            for i, item in enumerate(self.task):
                self.lay.addWidget(QLabel("{}. {}".format(i, item), self))
        elif index == 1:
            for i, item in enumerate(self.task):
                if 'Type' in item and item['Event Type'] == "ARRIVING":
                    self.lay.addWidget(QLabel("{}. {}".format(i, item), self))

        elif index == 2:
            for i, item in enumerate(self.task):
                if 'Type' in item and item['Event Type'] == 'RUNNING':
                    self.lay.addWidget(QLabel("{}. {}".format(i, item), self))

        elif index == 3:
            for i, item in enumerate(self.task):
                if 'Type' in item and item['Event Type'] == 'COMPLETED':
                    self.lay.addWidget(QLabel("{}. {}".format(i, item), self))

        elif index == 4:
            for i, item in enumerate(self.task):
                if 'Type' in item and item['Event Type'] == 'DEFERRED':
                    self.lay.addWidget(QLabel("{}. {}".format(i, item), self))

        elif index == 5:
            for i, item in enumerate(self.task):
                if 'Type' in item and item['Event Type'] == 'CANCELLED':
                    self.lay.addWidget(QLabel("{}. {}".format(i, item), self))

        elif index == 6:
            for i, item in enumerate(self.task):
                if 'Type' in item and item['Event Type'] == 'DROPPED_RUNNING_TASK':
                    self.lay.addWidget(QLabel("{}. {}".format(i, item), self))

        elif index == 7:
            for i, item in enumerate(self.machine_stats):
                if 'Machine id' in item:
                    self.lay.addWidget(QLabel("{}. {}".format(i, item), self))

    def clearLayout(self):
        """
        It takes a layout, and recursively removes all widgets from it
        """
        if self.lay is not None:
            while self.lay.count():
                item = self.lay.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
