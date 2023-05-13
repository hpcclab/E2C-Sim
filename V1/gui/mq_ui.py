from PyQt5.QtWidgets import (QGraphicsView,QGraphicsPathItem, QGraphicsTextItem,
QGraphicsEllipseItem, QLabel, QLineEdit, QGroupBox,QFormLayout,QPushButton,QWidget, QGraphicsPixmapItem)
from PyQt5.QtGui import QBrush,  QPen, QFont, QPainterPath, QColor,QTransform, QFontMetrics,QPixmap, QPolygonF
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QPointF
import random
import numpy as np



class MachineUi(QGraphicsView):

    def __init__(self, scene,machines, qsize, colors, x_outer, y_outer, w_outer, h_outer, max_h_q, x_machine_trash, y_trash, trash_size):
        super().__init__()
        self.scene = scene
        self.max_h_q = max_h_q
        self.x_outer = x_outer
        self.y_outer = y_outer
        self.w_outer = w_outer
        self.h_outer = h_outer
        self.x_trash = x_machine_trash
        self.y_trash = y_trash
        self.trash_size = trash_size
        self.machine_colors = []

        if colors:
            self.machine_colors = colors
        else:
            np.random.seed(0)
        for m in range(len(machines)):
            c = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
            self.machine_colors.append(c)


        self.max_qsize = qsize
        self.machines = machines
        self.machine_circles = {}
        self.m_runnings = {}
        self.m_queues={}
        self.missed_tasks_machines = []

        for machine in self.machines:
            m_id = machine.id
            self.m_queues[m_id] = []
            self.m_runnings[m_id] = []

        self.queue_frames = {}
        self.no_of_machines = len(self.machines)
        self.colors = [QColor(150,0,0),
                        QColor(93,168,154),
                        QColor(191,82,89),
                        QColor(82,126,191),
                        QColor(86,208,128) ]


    def reset(self):
        self.m_runnings = {}
        self.m_queues={}
        self.missed_tasks_machines = []
        np.random.seed(0)
        for m in range(len(self.machines)):
            c = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
            self.machine_colors.append(c)

        for machine in self.machines:
            m_id = machine.id
            self.m_queues[m_id] = []
            self.m_runnings[m_id] = []
        self.queue_frames = {}

    def update_machines(self, machines):
        self.machines = machines
        self.reset()
        self.draw_queues()
        self.fill_queues()




    def machines_frame(self, x,y, w, h):
        r = 0.05*h
        p = QPainterPath()
        p.addRoundedRect(x, y, w, h, r, r)
        o_frame = QGraphicsPathItem(p)
        bcg = QColor(250,250,250)
        pen = QPen(Qt.white,  1, Qt.SolidLine)
        brush = QBrush(bcg)
        o_frame.setBrush(brush)
        o_frame.setPen(pen)
        o_frame.setData(0,'machines_frame')

        self.m_lbl = QGraphicsTextItem('Machines')
        self.m_lbl.setFont(QFont('Arial',16))
        self.m_lbl.setFlag(self.m_lbl.ItemIsSelectable, False)
        w_lbl = self.m_lbl.boundingRect().width()
        h_lbl = self.m_lbl.boundingRect().height()
        self.m_lbl.setPos(x+0.5*w-0.5*w_lbl, y+h+0.5*h_lbl)

        self.scene.addItem(self.m_lbl)
        self.scene.addItem(o_frame)

    def outer_frame(self):
        r = 0.1* self.h_outer
        p = QPainterPath()
        p.addRoundedRect(self.x_outer, self.y_outer, self.w_outer, self.h_outer, r, r)
        o_frame = QGraphicsPathItem(p)
        o_frame.setData(0, 'machine_queues_frame')
        bcg = QColor(250,250,250)
        pen = QPen(Qt.white,  1, Qt.SolidLine)
        brush = QBrush(bcg)
        o_frame.setBrush(brush)
        o_frame.setPen(pen)

        self.mq_lbl = QGraphicsTextItem('Machine Queues')
        self.mq_lbl.setFont(QFont('Arial',16))
        self.mq_lbl.setFlag(self.mq_lbl.ItemIsSelectable, False)
        w_lbl = self.mq_lbl.boundingRect().width()
        h_lbl = self.mq_lbl.boundingRect().height()
        self.mq_lbl.setPos(self.x_outer+0.5*self.w_outer-0.5*w_lbl, self.y_outer+self.h_outer+0.5*h_lbl)

        self.scene.addItem(o_frame)
        self.scene.addItem(self.mq_lbl)


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
        for idx, machine in enumerate(self.machines):
            m_id = machine.id
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
        self.mq_placeholders()

    def mq_placeholders(self):
        for m_id, _ in self.m_queues.items():
            [x,y] = self.queue_frames[m_id]
            task_xspace = 0.05 * self.w_q
            task_yspace = 0.1 * self.h_q
            self.w_task = (self.w_q - (self.max_qsize+1)*task_xspace)/ self.max_qsize
            self.h_task = self.h_q - 2*task_yspace
            w_task = self.w_task
            h_task = self.h_task
            x_task = x + self.w_q
            y_task = y + task_yspace
            for idx in range(self.max_qsize):
                if idx <= (self.max_qsize-2) :
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

                elif idx == self.max_qsize-1:
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

            for idx, task in enumerate(tasks):

                if idx <= (self.max_qsize-2) :
                    x_task -= (w_task +  task_xspace)
                    r = 0.25*h_task
                    p = QPainterPath()
                    p.addRoundedRect(x_task, y_task, w_task, h_task, r, r)
                    t_frame = QGraphicsPathItem(p)
                    bcg = self.colors[task.type.id%len(self.colors)]
                    pen = QPen(Qt.white,  2, Qt.SolidLine)
                    brush = QBrush(bcg)
                    t_frame.setBrush(brush)
                    t_frame.setPen(pen)
                    t_frame.setData(0, 'task_in_mq')
                    t_frame.setData(1, task)

                    text = QGraphicsTextItem(f'{task.id}')
                    font_size = 16
                    font = QFont('Arial',font_size)
                    # font_metrics = QFontMetrics(font)
                    # font_width = font_metrics.width(text)
                    # font_height = font_metrics.height(text)
                    # while font_width > w_task or font_height> h_task:
                    #     font_size -= 0.5
                    #     font = QFont('Arial',font_size)
                    #     font_metrics = QFontMetrics(font)
                    #     font_width = font_metrics.width(text)
                    #     font_height = font_metrics.height(text)

                    text.setFont(font)
                    text.adjustSize()
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
                    bcg = self.colors[task.type.id%len(self.colors)]
                    pen = QPen(Qt.white,  2, Qt.SolidLine)
                    brush = QBrush(bcg)
                    t_frame.setBrush(brush)
                    t_frame.setPen(pen)
                    t_frame.setData(0,'task_in_mq_others')
                    t_frame.setData(1,m_id)

                    text = QGraphicsTextItem('o o o')
                    text.setFont(QFont('Arial',12))
                    text.setFlag(text.ItemIsSelectable, False)
                    w_text = text.boundingRect().width()
                    h_text = text.boundingRect().height()
                    text.setPos(x_task+(w_task-w_text)/2, y_task + (h_task-h_text)/2)

                    self.scene.addItem(t_frame)
                    self.scene.addItem(text)


    def runnings(self,machines):
        length = 1.0*self.h_q
        self.machine_r = 0.8*self.h_q
        gap = 0.05*length
        [x,y] = self.queue_frames[0]
        self.machines_frame(x+self.w_q+length+self.machine_r-0.5*2.5*self.machine_r,
                            self.y_outer,
                            2.5*self.machine_r, self.h_outer)
        # self.machine_colors = []
        # np.random.seed(0)
        # for m in range(len(machines)):
        #     c = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        #     self.machine_colors.append(c)

        i = 0
        self.machines = machines
        print(40*'=!')
        print(f'\t\t\mq_ui.py id 263')
        print([f'{m.type.name}:{m.id}' for m in self.machines])

        for machine in self.machines:
            m_id = machine.id
            [x,y] = self.queue_frames[m_id]
            x += self.w_q
            y += 0.5*self.h_q

            pen = QPen(QColor(72,72,72),  4, Qt.SolidLine)
            connecting_line = self.scene.addLine(x,y,x+length,y,pen)
            print([f'{self.machine_colors}'])
            print(f'\t\t i = {i}')
            c_1 = self.machine_colors[i][0]
            c_2 = self.machine_colors[i][1]
            c_3 = self.machine_colors[i][2]

            pen = QPen(QColor(c_1,c_2,c_3),  1, Qt.SolidLine)
            brush = QBrush(QColor(c_1,c_2,c_3))
            self.machine_circles[m_id] = [x+length, y-self.machine_r]
            machine_circle = QGraphicsEllipseItem (x+length, y-self.machine_r, 2*self.machine_r,2*self.machine_r)

            # m_text = QGraphicsTextItem("M"+str(i+1), parent=machine_circle)
            m_text = QGraphicsTextItem(f'{machine.type.name}', parent=machine_circle)
            m_text.setFont(QFont("Arial", 16))
            m_text.adjustSize()
            m_text.setFlag(m_text.ItemIsSelectable, False)
            w_m_text = m_text.boundingRect().width()
            h_m_text = m_text.boundingRect().height()
            m_text.setPos(x+length+self.machine_r-0.5*w_m_text, y - 0.5*h_m_text)


            machine_circle.setPen(pen)
            machine_circle.setBrush(brush)
            machine_circle.setData(0, 'machine')
            machine_circle.setData(1,machine)

            self.scene.addItem(machine_circle)
            self.scene.addItem(m_text)

            i += 1

            if  self.m_runnings[m_id]:
                machine_circle.setData(3,'busy')
                running_task = self.m_runnings[m_id][0]
                w = self.w_task
                h = self.h_task
                w = 1.2*self.machine_r
                h= 1.2*self.machine_r

                rounded_radius = 0.25*h
                p = QPainterPath()
                p.addRoundedRect(x+length+self.machine_r-0.5*w, y-0.5*h,w, h, rounded_radius, rounded_radius)
                t_frame = QGraphicsPathItem(p)
                bcg = self.colors[running_task.type.id%len(self.colors)]
                pen = QPen(Qt.white,  2, Qt.SolidLine)
                brush = QBrush(bcg)
                t_frame.setBrush(brush)
                t_frame.setPen(pen)
                text = QGraphicsTextItem(f'{running_task.id}')
                font_size = 16
                font = QFont('Arial',font_size)
                font_metrics = QFontMetrics(font)
                font_width = font_metrics.width(f'{running_task.id}')
                font_height = font_metrics.height()
                while font_width > w or font_height> h:
                    font_size -= 0.5
                    font = QFont('Arial',font_size)
                    font_metrics = QFontMetrics(font)
                    font_width = font_metrics.width(f'{running_task.id}')
                    font_height = font_metrics.height()

                text.setFont(font)
                text.adjustSize()
                text.setFlag(text.ItemIsSelectable, False)
                w_text = text.boundingRect().width()
                h_text = text.boundingRect().height()
                text.setPos(x+length+self.machine_r-0.5*w_text, y - 0.5*h_text)
                t_frame.setData(0,'task_in_machine')
                t_frame.setData(1, running_task)

                self.scene.addItem(t_frame)
                self.scene.addItem(text)



    def trash(self):
        self.trash_pix= QPixmap('./gui/icons/trash.png')
        self.trash_pix = self.trash_pix.scaled(QSize(int(self.trash_size),int(self.trash_size)), Qt.IgnoreAspectRatio)
        self.trash_item = QGraphicsPixmapItem(self.trash_pix)
        self.trash_item.setOffset(self.x_trash, self.y_trash)
        self.trash_item.setData(0,'trash_missed')

        self.missed_lbl = QGraphicsTextItem('Missed Tasks')
        self.missed_lbl.setFont(QFont('Arial',14))
        self.missed_lbl.setFlag(self.missed_lbl.ItemIsSelectable, False)
        w_lbl = self.missed_lbl.boundingRect().width()
        h_lbl = self.missed_lbl.boundingRect().height()
        self.missed_lbl.setPos(self.x_trash+0.5*(self.trash_size-w_lbl),self.y_trash + self.trash_size+0.5*h_lbl)

        self.scene.addItem(self.trash_item)
        self.scene.addItem(self.missed_lbl)

    def connect_machine_running_to_trash(self, task, machine, pen, color):
        x1,y1 = self.machine_circles[machine.id]
        y1 += self.machine_r
        x1 += 2*self.machine_r
        x2,y2 = self.x_trash + 0.5*self.trash_size, y1
        x3,y3 = x2, self.y_trash

        l1 = self.scene.addLine(x1,y1,x2,y2,pen)
        l2 = self.arrow1(x2,y2,x3,y3, pen, color)



    def arrow1(self, x1,y1,x2,y2, pen,color):
        w = pen.width()
        line = self.scene.addLine(x1,y1,x2,y2-w,pen)

        head_w = 4*w
        head_h = 6*w
        poly = QPolygonF([QPointF(x2 + 0.5*head_w, y2-head_h),
                        QPointF(x2 , y2),
                        QPointF(x2 - 0.5*head_w, y2-head_h)])
        head = self.scene.addPolygon(poly)
        head.setBrush(color)
        pen.setWidthF(1)
        head.setPen(pen)











