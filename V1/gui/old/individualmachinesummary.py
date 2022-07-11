
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QMessageBox,
    QScrollArea,
)


# Show the specs of each machine
class IndividualMachineSummary(QMessageBox):
    def __init__(self, l, title, *args, **kwargs):
        QMessageBox.__init__(self, *args, **kwargs)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        self.content = QWidget()
        scroll.setWidget(self.content)
        lay = QVBoxLayout(self.content)
        for k in l:
            lay.addWidget(QLabel("{}".format(k), self))
        self.layout().addWidget(scroll, 0, 0, 1, self.layout().columnCount())
        self.setStyleSheet("QScrollArea{min-width:900 px; min-height: 400px}")
        self.setWindowTitle(title)