from PyQt5.QtWidgets import (QGraphicsView,QGraphicsPathItem, QGraphicsTextItem,
 QLabel,QGraphicsEllipseItem, QLineEdit, QGroupBox,QFormLayout,QPushButton,QWidget)
from PyQt5.QtGui import QBrush,  QPen, QFont, QPainterPath, QColor,QTransform
from PyQt5.QtCore import Qt, pyqtSignal
from utils.task import Task



class WorkloadUi(QGraphicsView):
    
    def __init__(self, scene, x, y):
        super().__init__()
        self.scene = scene  
        self.x = x 
        self.y = y
               
        
    
    def draw_frame(self):
        self.label = QGraphicsTextItem(f'Workload')
        self.label.setFont(QFont('Arial',14))
        self.label.setDefaultTextColor(Qt.white)
        self.label.setFlag(self.label.ItemIsSelectable, False)
        w_label = self.label.boundingRect().width()
        h_label = self.label.boundingRect().height()   

        self.d_frame = max(w_label, h_label)      
        y = self.y - 0.5*self.d_frame
        self.frame = QGraphicsEllipseItem(self.x, y, self.d_frame, self.d_frame)        
        bcg = QColor(72,72,72)
        pen = QPen(bcg,  1, Qt.SolidLine)
        brush = QBrush(bcg)
        self.frame.setPen(pen)
        self.frame.setBrush(brush)
        self.frame.setData(0,'workload')
                          
        self.label.setPos(self.x+(self.d_frame-w_label)/2, y + (self.d_frame-h_label)/2)

        self.scene.addItem(self.frame)
        self.scene.addItem(self.label)


    
        
    


