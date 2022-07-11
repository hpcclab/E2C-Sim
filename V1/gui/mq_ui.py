from PyQt5.QtWidgets import (QGraphicsView,QGraphicsPathItem, QGraphicsTextItem,
 QLabel, QLineEdit, QGroupBox,QFormLayout,QPushButton,QWidget)
from PyQt5.QtGui import QBrush,  QPen, QFont, QPainterPath, QColor,QTransform
from PyQt5.QtCore import Qt, pyqtSignal




class MachineUi(QGraphicsView):
    
    def __init__(self, scene,machines, qsize, x_outer, y_outer, w_outer, h_outer, max_h_q):
        super().__init__()
        self.scene = scene 
        self.max_h_q = max_h_q
        self.x_outer = x_outer
        self.y_outer = y_outer
        self.w_outer = w_outer
        self.h_outer = h_outer
        self.max_qsize = qsize
        self.machines = machines
        self.m_runnings = {}
        self.m_queues={}
        for m_id in self.machines:
            self.m_queues[m_id] = []
            self.m_runnings[m_id] = []
        self.queue_frames = {}
        self.no_of_machines = len(self.machines)
    
    def reset(self):
        self.m_runnings = {}
        self.m_queues={}
        for m_id in self.machines:
            self.m_queues[m_id] = []
            self.m_runnings[m_id] = []
        self.queue_frames = {}

        



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
        self.scene.addItem(o_frame)
    

    def draw_queues(self):
        
        if self.no_of_machines==0:
            return
        q_xspace = 0.02 * self.w_outer
        q_yspace = 0.1 * self.h_outer
        self.h_q = (self.h_outer - (self.no_of_machines+1)*q_yspace)/ self.no_of_machines        
        if self.h_q > self.max_h_q:
            self.h_q = self.max_h_q
            q_yspace = (self.h_outer - self.no_of_machines*self.h_q) / (self.no_of_machines+1)
        self.w_q = self.w_outer - 4*q_xspace
        x_q = self.x_outer + 2*q_xspace
        y_q = self.y_outer  - self.h_q
        for idx, m_id in enumerate(self.machines): 
            y_q += (self.h_q +  q_yspace)    
            self.queue_frames[m_id] = [x_q,y_q] 
            r = 0.25*self.h_q
            p = QPainterPath()
            p.addRoundedRect(x_q, y_q, self.w_q, self.h_q, r, r)
            t_frame = QGraphicsPathItem(p)
            bcg = QColor(72,72,72)
            pen = QPen(bcg,  2, Qt.SolidLine)
            brush = QBrush(bcg)
            t_frame.setBrush(brush)
            t_frame.setPen(pen) 
            self.scene.addItem(t_frame)
        

    def fill_queues(self):
        for m_id, tasks in self.m_queues.items():
            [x,y] = self.queue_frames[m_id]
            task_xspace = 0.05 * self.w_q
            task_yspace = 0.1 * self.h_q
            self.w_task = (self.w_q - (self.max_qsize+1)*task_xspace)/ self.max_qsize        
            self.h_task = self.h_q - 2*task_yspace
            w_task = self.w_task
            h_task = self.h_task
            x_task = x + self.w_q
            y_task = y + task_yspace
            
            for idx, task_id in enumerate(tasks): 
                
                if idx <= (self.max_qsize-2) : 
                    x_task -= (w_task +  task_xspace)     
                    r = 0.25*h_task
                    p = QPainterPath()
                    p.addRoundedRect(x_task, y_task, w_task, h_task, r, r)
                    t_frame = QGraphicsPathItem(p)
                    bcg = QColor(150+idx*10,0,0)
                    pen = QPen(Qt.white,  2, Qt.SolidLine)
                    brush = QBrush(bcg)
                    t_frame.setBrush(brush)
                    t_frame.setPen(pen) 
                    
                    text = QGraphicsTextItem(f'{task_id}')
                    text.setFont(QFont('Arial',16))
                    text.setFlag(text.ItemIsSelectable, False)
                    w_text = text.boundingRect().width()
                    h_text = text.boundingRect().height()                            
                    text.setPos(x_task+(w_task-w_text)/2, y_task + (h_task-h_text)/2)
                
                    self.scene.addItem(t_frame)
                    self.scene.addItem(text)
                elif idx == self.max_qsize-1:
                    x_task = x_task - (w_task +  task_xspace)                 
                    r = 0.25*h_task
                    p = QPainterPath()
                    p.addRoundedRect(x_task, y_task, w_task, h_task, r, r)
                    t_frame = QGraphicsPathItem(p)
                    bcg = QColor(150+idx*10,0,0)
                    pen = QPen(Qt.white,  2, Qt.SolidLine)
                    brush = QBrush(bcg)
                    t_frame.setBrush(brush)
                    t_frame.setPen(pen) 
                    
                    text = QGraphicsTextItem('o o o')
                    text.setFont(QFont('Arial',12))
                    text.setFlag(text.ItemIsSelectable, False)
                    w_text = text.boundingRect().width()
                    h_text = text.boundingRect().height()                            
                    text.setPos(x_task+(w_task-w_text)/2, y_task + (h_task-h_text)/2)
                
                    self.scene.addItem(t_frame)
                    self.scene.addItem(text)
    
    

    def runnings(self):
       
        for m_id in self.machines:
            [x,y] = self.queue_frames[m_id]
            x += self.w_q
            y += 0.5*self.h_q
            length = 1.5*self.h_q
            r = 0.65*self.h_q
            pen = QPen(QColor(72,72,72),  4, Qt.SolidLine)
           
            connecting_line = self.scene.addLine(x,y,x+length,y,pen)

            pen = QPen(QColor(82,126,191),  1, Qt.SolidLine)
            brush = QBrush(QColor(82,126,191))
            machine_circle = self.scene.addEllipse(x+length, y-r, 2*r,2*r,pen, brush)

            if  self.m_runnings[m_id]:
                w = self.w_task
                h = self.h_task
                rounded_radius = 0.25*h         
                p = QPainterPath()
                p.addRoundedRect(x+length+r-0.5*w, y-0.5*h,w, h, rounded_radius, rounded_radius)
                t_frame = QGraphicsPathItem(p)
                bcg = QColor(150,0,0)
                pen = QPen(Qt.white,  2, Qt.SolidLine)
                brush = QBrush(bcg)
                t_frame.setBrush(brush)
                t_frame.setPen(pen)                 
                text = QGraphicsTextItem(f'{self.m_runnings[m_id][0]}')
                text.setFont(QFont('Arial',16))
                text.setFlag(text.ItemIsSelectable, False)
                w_text = text.boundingRect().width()
                h_text = text.boundingRect().height()                            
                text.setPos(x+length+r-0.5*w_text, y - 0.5*h_text)

                
                self.scene.addItem(t_frame)
                self.scene.addItem(text)
            #self.scene.addItem(machine_circle)



            
            
        

    

        
        
    


