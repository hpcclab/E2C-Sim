from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class HelpMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help Menu")
        self.setContentsMargins(10,10,10,10)

        self.layout = QVBoxLayout()
        self.title = QLabel("Edge-to-Cloud Simulator (E2C)")
        self.title.setStyleSheet("font-size: 30px;")
        self.title.setAlignment(Qt.AlignHCenter)

        self.title2 = QLabel("version: Beta")
        self.title2.setStyleSheet("font-size: 15px; color: grey;")
        self.title2.setAlignment(Qt.AlignHCenter)

        self.title3 = QLabel("\nE2C is an open-source simulator developed at High Performance Cloud Computing (HPCC) laboratory, University of Louisiana Lafayette. The simulator was developed in a project sponsored by National Science Foundation (NSF).")
        self.title3.setStyleSheet("font-size: 20px; padding: 15px;")
        self.title3.setWordWrap(True)
        self.title3.setAlignment(Qt.AlignHCenter)

        self.logos = QHBoxLayout()

        hpcc_label = QLabel(self)
        pixmap1 = QPixmap(f'./gui/icons/hpccLogo.png')
        hpcc_label.setPixmap(pixmap1)
        self.logos.addWidget(hpcc_label)
        hpcc_label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)

        ull_label = QLabel(self)
        pixmap2 = QPixmap(f'./gui/icons/ullLogo.png')
        ull_label.setPixmap(pixmap2)
        self.logos.addWidget(ull_label)
        ull_label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)

        nsf_label = QLabel(self)
        pixmap3 = QPixmap(f'./gui/icons/nsfLogo.png')
        nsf_label.setPixmap(pixmap3)
        self.logos.addWidget(nsf_label)
        nsf_label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.title2)
        self.layout.addWidget(self.title3)
        self.layout.addLayout(self.logos, Qt.AlignBottom)

        self.layout.addStretch()

        self.setLayout(self.layout)
        self.resize(800, 400)

        self.show()