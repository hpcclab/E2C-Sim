from PyQt5.QtWidgets import (QGraphicsView,QGraphicsPathItem, QGraphicsTextItem,
 QLabel, QLineEdit, QGroupBox,QFormLayout,QPushButton,QWidget)
from PyQt5.QtGui import QBrush,  QPen, QFont, QPainterPath, QColor,QTransform
from PyQt5.QtCore import Qt, pyqtSignal
from utils.task import Task



class BatchQueueUI(QGraphicsView):
    
    def __init__(self, scene, size, x_outer, y_outer, w_outer, h_outer, w_inner, h_inner):
        super().__init__()
        self.scene = scene          
        self.w_inner = w_inner
        self.h_inner = h_inner
        self.x_outer = x_outer
        self.y_outer = y_outer
        self.w_outer = w_outer
        self.h_outer = h_outer
        self.size = size
        self.tasks = []  
        self.t_frames = []
        self.others = []   
        self.colors = [QColor(150,0,0), 
                        QColor(93,168,154),
                        QColor(191,82,89),
                        QColor(82,126,191),
                        QColor(86,208,128) ]
    
    def reset(self):
        self.tasks = []  
        self.t_frames = []
        self.others = []  

        
        



    def outer_frame(self):        
        r = 0.05*self.h_outer
        r = 0.1* self.h_outer
        p = QPainterPath()
        p.addRoundedRect(self.x_outer, self.y_outer, self.w_outer, self.h_outer, r, r)
        o_frame = QGraphicsPathItem(p)
        bcg = QColor(250,250,250)
        pen = QPen(Qt.white,  1, Qt.SolidLine)
        brush = QBrush(bcg)
        o_frame.setBrush(brush)
        o_frame.setPen(pen) 
        o_frame.setData(0,'batch_queue_frame')
        self.scene.addItem(o_frame)

    def inner_frame(self): 
        inner_xspace = 0.5*(self.w_outer - self.w_inner)
        self.x_inner = self.x_outer + inner_xspace
        self.y_inner = self.y_outer + 0.5*self.h_outer - 0.5*self.h_inner
        r = 0.25*self.h_inner
        p = QPainterPath()
        p.addRoundedRect(self.x_inner, self.y_inner, self.w_inner, self.h_inner, r, r)
        i_frame = QGraphicsPathItem(p)
        bcg = QColor(75,72,72)
        pen = QPen(Qt.white,  1, Qt.SolidLine)
        brush = QBrush(bcg)
        i_frame.setBrush(brush)
        i_frame.setPen(pen) 
        self.scene.addItem(i_frame)
        self.draw_placeholders()
    

    def draw_placeholders(self):
        task_xspace = 0.02 * self.w_inner
        task_yspace = 0.1 * self.h_inner
        w_task = (self.w_inner - (self.size+1)*task_xspace)/ self.size        
        h_task = self.h_inner - 2*task_yspace
        x_task = self.x_inner + self.w_inner 
        y_task = self.y_inner + task_yspace
        
        for idx  in range(self.size): 
               
            if idx <= (self.size-2) : 
                x_task -= (w_task +  task_xspace)     
                r = 0.25*h_task
                p = QPainterPath()
                p.addRoundedRect(x_task, y_task, w_task, h_task, r, r)
                t_frame = QGraphicsPathItem(p)                                
                bcg = Qt.white
                pen = QPen(Qt.white,  2, Qt.SolidLine)
                brush = QBrush(bcg)                
                t_frame.setBrush(brush)
                t_frame.setPen(pen)            
                self.scene.addItem(t_frame)
                
            elif idx == self.size-1:
                x_task = x_task - (w_task +  task_xspace)                 
                r = 0.25*h_task
                p = QPainterPath()
                p.addRoundedRect(x_task, y_task, w_task, h_task, r, r)
                t_frame = QGraphicsPathItem(p)
                bcg = Qt.white
                pen = QPen(Qt.white,  2, Qt.SolidLine)
                brush = QBrush(bcg)
                t_frame.setBrush(brush)
                t_frame.setPen(pen)             
                self.scene.addItem(t_frame)
               
        

    def draw_tasks(self, selected_task):
        task_xspace = 0.02 * self.w_inner
        task_yspace = 0.1 * self.h_inner
        w_task = (self.w_inner - (self.size+1)*task_xspace)/ self.size        
        h_task = self.h_inner - 2*task_yspace
        x_task = self.x_inner + self.w_inner 
        y_task = self.y_inner + task_yspace
        
        for idx, task in enumerate(self.tasks): 
               
            if idx <= (self.size-2) : 
                x_task -= (w_task +  task_xspace)     
                r = 0.25*h_task
                p = QPainterPath()
                p.addRoundedRect(x_task, y_task, w_task, h_task, r, r)
                t_frame = QGraphicsPathItem(p)                                
                bcg = self.colors[task.type.id%len(self.colors)]
                pen = QPen(Qt.white,  2, Qt.SolidLine)
                brush = QBrush(bcg)
                if task == selected_task:
                    brush= Qt.yellow
                t_frame.setBrush(brush)
                t_frame.setPen(pen)
                t_frame.setData(0, 'task_in_bq')
                t_frame.setData(1, task)  
                self.t_frames.append(t_frame)   

                text = QGraphicsTextItem(f'{task.id}')
                text.setFont(QFont('Arial',16))
                text.setFlag(text.ItemIsSelectable, False)
                w_text = text.boundingRect().width()
                h_text = text.boundingRect().height()                            
                text.setPos(x_task+(w_task-w_text)/2, y_task + (h_task-h_text)/2)
            
                self.scene.addItem(t_frame)
                self.scene.addItem(text)
            elif idx == self.size-1:
                x_task = x_task - (w_task +  task_xspace)                 
                r = 0.25*h_task
                p = QPainterPath()
                p.addRoundedRect(x_task, y_task, w_task, h_task, r, r)
                t_frame = QGraphicsPathItem(p)
                bcg = self.colors[task.type.id%len(self.colors)]
                pen = QPen(Qt.white,  2, Qt.SolidLine)
                brush = QBrush(bcg)
                t_frame.setBrush(brush)
                t_frame.setPen(pen) 
                t_frame.setData(0,'task_in_bq_others')
                
                text = QGraphicsTextItem('o o o')
                text.setFont(QFont('Arial',12))
                text.setFlag(text.ItemIsSelectable, False)
                w_text = text.boundingRect().width()
                h_text = text.boundingRect().height()                            
                text.setPos(x_task+(w_task-w_text)/2, y_task + (h_task-h_text)/2)
            
                self.scene.addItem(t_frame)
                self.scene.addItem(text)
        
    def choose_task(self, task, bq_idx):
        
        print(self.t_frames[0].data(1).id)
        self.t_frames[0].setBrush(Qt.yellow)
        self.scene.update()
        


    
    
    def remove_task(self, task):
        pass

    def select_task(self, task):
        pass

    def highlight_task(self, task):
        pass


        
        
    


