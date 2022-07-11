import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRectF, QObject, pyqtSignal, QPointF
from PyQt5.QtGui import QBrush, QPainter, QPen, QFont, QPainterPath, QColor,QTransform
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsPathItem,
    QGraphicsTextItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
    
)
from PyQt5.QtCore import Qt, QThread
from gui.bq_ui import BatchQueueUI
from gui.mq_ui import MachineUi
from gui.mapper_ui import MapperUi

import utils.config as config


class GraphicView(QGraphicsView):
    itemClicked = pyqtSignal(object)


    def __init__(self, parent=None):
        super(GraphicView, self).__init__(parent)
        self.scene = QGraphicsScene(0,0,1200,600)
        self.setScene(self.scene)
        self.setFixedSize(1500, 600)
        self.setRenderHint(QPainter.Antialiasing)
        self.initView()
        
    
    def initView(self):
        self.current_time = 0.0
        self.x_bq = 50
        self.y_bq = 400-125
        self.bq_w_outer = 400
        self.bq_h_outer = 150
        self.bq_w_innre = 350
        self.bq_h_inner = 50

        self.mq_h_outer = 250
        self.mq_w_outer = 300
        self.x_mq = self.x_bq + self.bq_w_outer +400
        self.y_mq = self.y_bq + 0.5*(self.bq_h_outer - self.mq_h_outer)

        self.x_mapper = self.x_bq+self.bq_w_outer+100
        self.y_mapper = self.y_bq+0.5*(self.bq_h_outer-100)

        self.batch_queue = BatchQueueUI(self.scene, 5, self.x_bq, self.y_bq ,self.bq_w_outer,self.bq_h_outer, self.bq_w_innre,self.bq_h_inner)        
        self.batch_queue.outer_frame()
        self.batch_queue.inner_frame()
        schedulers = ['MinCompletion-MinCompletion','FCFS']        
        self.mapper()
        machines = [m.id for m in config.machines]
        self.machine_queues = MachineUi(self.scene,machines = machines, qsize = 5,
        x_outer =  self.x_mq, y_outer = self.y_mq , w_outer = self.mq_w_outer,h_outer = self.mq_h_outer, max_h_q=self.bq_h_inner)        
        self.machine_queues.outer_frame()
        self.machine_queues.draw_queues()
        self.machine_queues.runnings()
        self.display_time(0.0)
        self.connecting_lines()

        # self.time_lbl= QLabel(f'Current Time:{self.current_time}')
        # self.time_lbl.setFont(QFont('Arial', 10))
        # #self.time_lbl.setGeometry(0, 0, 300, 30)
        # self.time_lbl.setFixedSize(150,30)
        # self.scene.addWidget(self.time_lbl)


        


        self.itemClicked.connect(self.gv_update)
    
    def mouseMoveEvent(self, event):
        mousePos = self.mapToScene(event.pos())
        #c = self.scene.addEllipse(mousePos.x(), mousePos.y(), 10,10)
        
        items = self.scene.items(mousePos,Qt.IntersectsItemShape,
                                Qt.DescendingOrder, QTransform())        
        if items is not None: 
            for item in items:
                if isinstance(item, QGraphicsPathItem) and item.data(0)!=None: 
                    print(item.data(0))       
                    self.itemClicked.emit(item)
        self.scene.update()   
       
    

    def display_time(self, time):
        self.current_time = time
        self.time_lbl = QGraphicsTextItem(f'Time {self.current_time:5.3f}')
        self.time_lbl.setFont(QFont('Arial',10))
        self.time_lbl.setFlag(self.time_lbl.ItemIsSelectable, False)                                
        self.time_lbl.setPos(-140,0)
        self.scene.addItem(self.time_lbl)
        self.update()


    def mapper(self):              
        self.mapper_pix= QPixmap('./gui/icons/mapper.png') 
        self.mapper_pix = self.mapper_pix.scaled(QSize(100,100), Qt.IgnoreAspectRatio)
        self.mapper_item = QGraphicsPixmapItem(self.mapper_pix) 
        self.mapper_item.setOffset(self.x_mapper, self.y_mapper)       
        self.scene.addItem(self.mapper_item)

    
    def connecting_lines(self):
        x_bq_to_mapper = self.x_bq+self.bq_w_outer
        y_bq_to_mapper = self.y_bq+0.5*self.bq_h_outer        
        self.arrow(x_bq_to_mapper, y_bq_to_mapper,
        self.x_mapper,y_bq_to_mapper,QPen(Qt.red, 4), Qt.red)
    
    def connect_mapper_machine(self, m_id, pen, color):
        [xq,yq] = self.machine_queues.queue_frames[m_id]
        
        x1 = self.x_mapper + self.mapper_pix.width()
        y1 = self.y_mapper + 0.5*self.mapper_pix.height()

        x2 = x1 + 0.5*(self.x_mq - x1)
        y2 = y1

        x3 = x2
        y3 = yq + 0.5 * self.machine_queues.h_q

        l1 = self.scene.addLine(x1,y1,x2,y2, pen)
        l2 = self.scene.addLine(x2,y2,x3,y3, pen)

        l3 = self.arrow(x3,y3,xq,y3, pen, color)

        
        
    def arrow(self, x1,y1,x2,y2, pen,color):
        w = pen.width()
        line = self.scene.addLine(x1,y1,x2-w,y2,pen)
        
        head_size = [6*w, 4*w]
        poly = QPolygonF([QPointF(x2 - head_size[0], y2-0.5*head_size[1]),
                        QPointF(x2 , y2),
                        QPointF(x2 - head_size[0], y2+0.5*head_size[1])])
        head = self.scene.addPolygon(poly)
        head.setBrush(color)
        pen.setWidthF(1)
        head.setPen(pen)

    
    def gv_update(self, item):  
        pass                  
        # brush = QBrush(Qt.yellow)
        # item.setBrush(brush)
        # self.scene.update()