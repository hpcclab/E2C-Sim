
from PyQt5.QtWidgets import (    
    QLabel,
    QFrame,    
    QVBoxLayout,
    
)

from PyQt5.QtCore import Qt
from os import makedirs



# This class holds the code for statistic box on the top. The stats are arranged vertically with QVBoxLayout
# and each stat is made from QLabel


# It's a QFrame with a QVBoxLayout that contains a bunch of QLabels.
class Statistic(QFrame):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.width = 400
        self.TotalTasks = QLabel(self)
        self.TotalTasks.setText("Total Tasks: {}".format(0))
        self.TotalTasks.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.TotalTasks.setMaximumWidth(self.width)
        self.TotalTasks.setStyleSheet("border:1px solid;")
        self.layout.addWidget(self.TotalTasks)

        self.TotalCompletion = QLabel(self)
        self.TotalCompletion.setText("Total Completion: {}%".format(0))
        self.TotalCompletion.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.TotalCompletion.setMaximumWidth(self.width)
        self.TotalCompletion.setStyleSheet("border:1px solid;")
        self.layout.addWidget(self.TotalCompletion)

        self.TotalxCompletion = QLabel(self)
        self.TotalxCompletion.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.TotalxCompletion.setText(
            "Total Extended Completion: {}%".format(0))
        self.TotalxCompletion.setMaximumWidth(self.width)
        self.TotalxCompletion.setStyleSheet("border:1px solid;")
        self.layout.addWidget(self.TotalxCompletion)

        self.deffered = QLabel(self)
        self.deffered.setText("Deferred: {}%".format(0))
        self.deffered.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.deffered.setMaximumWidth(self.width)
        self.deffered.setStyleSheet("border:1px solid;")
        self.layout.addWidget(self.deffered)

        self.dropped = QLabel(self)
        self.dropped.setText("Dropped: {}%".format(0))
        self.dropped.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.dropped.setMaximumWidth(self.width)
        self.dropped.setStyleSheet("border:1px solid;")
        self.layout.addWidget(self.dropped)

        self.totalCompletion = QLabel(self)
        self.totalCompletion.setText("Total Completion: {}%".format(0))
        self.totalCompletion.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.totalCompletion.setMaximumWidth(self.width)
        self.totalCompletion.setStyleSheet("border:1px solid;")
        self.layout.addWidget(self.totalCompletion)

        self.consumedEnergy = QLabel(self)
        self.consumedEnergy.setText("Consumed Energy: {}%".format(0))
        self.consumedEnergy.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.consumedEnergy.setMaximumWidth(self.width)
        self.consumedEnergy.setStyleSheet("border:1px solid;")
        self.layout.addWidget(self.consumedEnergy)

        self.energyPerCompletion = QLabel(self)
        self.energyPerCompletion.setText("Energy per completion: {}".format(0))
        self.energyPerCompletion.setTextInteractionFlags(
            Qt.TextSelectableByMouse)
        self.energyPerCompletion.setMaximumWidth(self.width)
        self.energyPerCompletion.setStyleSheet("border:1px solid;")
        self.layout.addWidget(self.energyPerCompletion)

        self.layout.setContentsMargins(20, 600, 0, 0)
        self.layout.setSpacing(0)
