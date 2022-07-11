from PyQt5.QtWidgets import (QComboBox, QLabel,QWidget, QVBoxLayout)
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import QApplication
import sys




class MapperUi(QWidget):
    
    def __init__(self,schedulers):
        super().__init__()        
        self.schedulers = schedulers

        self.initUi()
    

    def initUi(self):

        #self.mapper_layout = QVBoxLayout()
        self.mapper_label = QLabel(self)         
        self.pixmap = QPixmap('./gui/icons/mapper.png') 
        self.pixmap.scaled(200,200)
        self.mapper_label.setPixmap(self.pixmap)
        self.mapper_label.setStyleSheet(f"background-color: rgb(217,217,217);")

        # Optional, resize label to image size
        # self.mapper_label.resize(100,
        #                   100)
        #self.mapper_label.setFixedSize(500,500)

        #self.mapper_cb = QComboBox(self)
        #self.cb_schedulers.setGeometry(200, 150, 120, 40) 

        #for scheduler in self.schedulers:
            #self.mapper_cb.addItem(scheduler)
        
        #self.cb_schedulers.activated.connect(self.do_something)
        # self.mapper_layout.addWidget(self.mapper_label)
        #self.mapper_layout.addWidget(self.mapper_cb)

        #self.setLayout(self.mapper_layout)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    schedulers = ['MinCompletion-MinCompletion','FCFS']
    ex = MapperUi(schedulers)
    ex.show()
    sys.exit(app.exec_())




