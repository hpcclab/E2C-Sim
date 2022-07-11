
from PyQt5.QtWidgets import (
    QWidget,    
    QLabel,
    QVBoxLayout,
    QMessageBox,
    QScrollArea
)


# Generate a message box that contains report of the machine
class MachinesSummaryBox(QMessageBox):
    def __init__(self, l, finishTasks, title, *args, **kwargs):
        QMessageBox.__init__(self, *args, **kwargs)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        self.content = QWidget()
        scroll.setWidget(self.content)
        lay = QVBoxLayout(self.content)
        for i, j in l.items():
            if i == '%Completion':
                lay.addWidget(
                    QLabel("{}: {:2.1f}%".format("Completion", j), self))
            elif i == '# of %Completion':
                lay.addWidget(QLabel("{}: {:2.1f}".format(
                    "# of Completed Tasks", j), self))
            elif i == '%XCompletion':
                lay.addWidget(QLabel("{}: {:2.1f}%".format(
                    "Extended Completion", j), self))
            elif i == '# of %XCompletion':
                lay.addWidget(QLabel("{}: {:2.1f}".format(
                    "# of Extended Completed Tasks", j), self))
            elif i == '#Missed URG':
                lay.addWidget(QLabel("{}: {:2.1f}".format(
                    "# Urgent tasks missed deadline", j), self))
            elif i == 'Missed BE':
                lay.addWidget(QLabel("{}: {:2.1f}".format(
                    "# Best Effort tasks missed deadline", j), self))

            elif i == '%Energy':
                lay.addWidget(QLabel("{}: {:2.1f}%".format("Energy", j), self))
            elif i == '%Wasted Energy':
                lay.addWidget(
                    QLabel("{}: {:2.1f}%".format("Wasted Energy", j), self))
            else:
                lay.addWidget(QLabel("{}: {}".format(i, j), self))
        lay.addWidget(QLabel("Finished tasks: {}".format(finishTasks), self))

        self.layout().addWidget(scroll, 0, 0, 1, self.layout().columnCount())
        self.setStyleSheet("QScrollArea{min-width:900 px; min-height: 400px}")
        self.setWindowTitle(title)