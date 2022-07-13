from PyQt5.QtWidgets import (QComboBox, QLabel,QWidget, QVBoxLayout)
from PyQt5.QtGui import QPixmap

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem
import sys




class MapperUi(QGraphicsView):
    
    def __init__(self, scene,  x_mapper, y_mapper, mapper_size, x_trash, y_trash, trash_size):
        super().__init__() 
        self.scene = scene       
        
        self.x_mapper = x_mapper
        self.y_mapper = y_mapper
        self.mapper_size = mapper_size
        self.x_trash = x_trash
        self.y_trash = y_trash
        self.trash_size = trash_size
        self.cancelled_tasks = []
        
        self.mapper()
        self.trash()

        
    

    def mapper(self):              
        self.mapper_pix= QPixmap('./gui/icons/mapper.png') 
        self.mapper_pix = self.mapper_pix.scaled(QSize(self.mapper_size,self.mapper_size), Qt.IgnoreAspectRatio)
        self.mapper_item = QGraphicsPixmapItem(self.mapper_pix) 
        self.mapper_item.setOffset(self.x_mapper, self.y_mapper)  
        self.mapper_item.setData(0, 'mapper')     
        self.scene.addItem(self.mapper_item)
    

    def trash(self):
        self.trash_pix= QPixmap('./gui/icons/trash.png') 
        self.trash_pix = self.trash_pix.scaled(QSize(self.trash_size,self.trash_size), Qt.IgnoreAspectRatio)
        self.trash_item = QGraphicsPixmapItem(self.trash_pix) 
        self.trash_item.setOffset(self.x_trash, self.y_trash)         
        self.trash_item.setData(0,'trash')
        self.scene.addItem(self.trash_item)




