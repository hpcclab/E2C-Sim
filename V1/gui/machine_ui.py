from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QColor
from PyQt5.QtCore import Qt, QPoint, QRect


class MachineUI:

    def __init__(self):
        self.ids = [0,1,2,3]
        self.progress = 0
        
        


    def draw(self,painter, x_machines,y_machines, w, h):
        machine_colors=[QColor(93,168,154),
                     QColor(206,208,80),
                     QColor(191,82,89),
                     QColor(82,126,91)]
        gap_machines = 20
        for i in self.ids:
            color = machine_colors[i]
            # draw the background rectangle
            x = x_machines
            y = y_machines + i*1.5*(h+gap_machines)
            bcg_color = QtGui.QColor(75,72,72)
            painter.setPen(QPen(bcg_color,  4, Qt.SolidLine))                       
            painter.setBrush(QBrush(bcg_color))        
            xRound = 0.25*h
            yRound = 0.25*h        
            painter.drawRoundedRect(x, y, w, h , xRound, yRound)
            #draw the extended line out of background rectangle
            extended_line_len = 0.75*h
            painter.drawLine(x+w , y+0.5*h, x+w+extended_line_len, y+0.5*h)
            #draw the machine circle
            painter.setPen(QPen(Qt.white,  4, Qt.SolidLine)) 
            painter.setBrush(QBrush(color))        
            r = 0.75*h
            painter.drawEllipse(x+w+extended_line_len, y+0.5*h-r, 2*r,2*r)
            #draw machine name text
            painter.setPen(Qt.transparent)        
            painter.setBrush(QBrush(Qt.transparent))
            rect = QRect(x+w+extended_line_len, y+0.5*h-r, 2*r,2*r)
            painter.drawRect(rect)
            painter.setPen(Qt.black)
            painter.setFont(QFont("Arial", 16))
            painter.drawText(rect, Qt.AlignCenter, f'M{i}')
        
        
        # for idx, task in enumerate(tasks):
        #     painter.setBrush(QBrush(bcg_color[idx+1]))
        #     painter.setPen(QPen(bcg_color[idx+1],  4, Qt.SolidLine))
        #     ygap = 0.03
        #     xi = x + 0.1*w
        #     hi = (1 - (len(items)+1) *ygap)*h*items[idx]
        #     y += ygap*h
        #     wi = 0.8*w
        #     xRound = 0.25*wi
        #     yRound = 0.25*wi
        #     print(x,y,w,hi)
        #     painter.drawRoundedRect(xi, y, wi, hi , xRound, yRound)            
        #     y += hi
        
        def progress(self, x,y,r,p):
            pass
        





