import sys, time
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
from utils.simulator import Simulator
from gui.graphic_view import GraphicView
from gui.item_dock_detail import ItemDockDetail
import utils.config as config
from utils.task import Task


class SimUi(QMainWindow):
    
    def __init__(self,workload_name, scenario, etc, workload_id):
        super().__init__()
        self.workload_name = workload_name
        self.scenario = scenario
        self.etc = etc
        self.workload_id = workload_id
        self.title = "E2C Simulator"
        self.top= 0
        self.left= 0      
        self.width = 1200 
        self.height = 600        
        self.setWindowTitle(self.title)        
        self.setStyleSheet(f"background-color: rgb(217,217,217);")
        self.setGeometry(self.top, self.left, self.width, self.height)
        #self.setFixedSize(self.width, self.height)

        self.initUI()
    
    def initUI(self):
        self.general_layout = QVBoxLayout() 
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.general_layout)
        self.label = QLabel('simulator')
        self.general_layout.addWidget(self.label)
        self.gv = GraphicView(self.width, self.height)   
        
        #self.dock_left = ItemDockDetail()
        self.dock_right = ItemDockDetail()
        self.gv.itemClicked.connect(self.dock_update)     
        hlayout = QHBoxLayout()
        #hlayout.addWidget(self.dock_left)

        hlayout.addWidget(self.gv)
        #hlayout.addWidget(self.dock_right)
        #self.general_layout.addWidget(self.gv)
        self.addDockWidget(Qt.RightDockWidgetArea,self.dock_right.dock)
        self.general_layout.addLayout(hlayout)
        self.create_ctrl_buttons()
        self.connect_signals()
       

    def dock_update(self,item):
         
        if item.data(0) == 'task_in_bq' or item.data(0) == 'task_in_mq' or item.data(0)=='task_in_machine' :      
            brush = QBrush(Qt.yellow)
            item.setBrush(brush) 
            self.dock_right.task_in_bq(item.data(1)) 
        elif item.data(0) == 'machine':
            brush = QBrush(Qt.yellow)
            item.setBrush(brush) 
            self.dock_right.machine_data(item.data(1))
        elif item.data(0) == 'trash':
            self.dock_right.trash_data(self.gv.mapper_ui.cancelled_tasks)
        self.gv.scene.update()
               
    def create_ctrl_buttons(self):
        self.buttons = {'reset':None,
                        'simulate':None,
                        'skip':None}
        bcg_style = "{color: #333; border: 1 px solid #555; \
                    border-radius: 12px; border-style: outset; \
                    background: qradialgradient( cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, radius: 1.35, stop: 0 #fff, stop: 1 #888 ); \
                    padding: 5px;}"         
        self.btn_layout =  QHBoxLayout()
        hlayout_btns = QHBoxLayout()
        vlayout_pbar = QVBoxLayout()
        dummy = QLabel('         ')
        dummy.setMinimumWidth(70)
        hlayout_btns.addWidget(dummy)
        for btn_text, _ in self.buttons.items():           
            self.buttons[btn_text] = QPushButton('',self)
            self.buttons[btn_text].setIcon(QIcon(f'./gui/icons/{btn_text}.png'))
            self.buttons[btn_text].setIconSize(QSize(128,24))
            self.buttons[btn_text].setGeometry(0,0,128,24)
            self.buttons[btn_text].setStyleSheet(f"QPushButton {bcg_style}")
            self.buttons[btn_text].setToolTip(btn_text)              
            hlayout_btns.addWidget(self.buttons[btn_text],Qt.AlignTop)        
        dummy = QLabel('         ')
        dummy.setMinimumWidth(20)
        hlayout_btns.addWidget(dummy)        
        self.progress_bar()
        vlayout_pbar.addLayout(self.pbar_layout)
        vlayout_pbar.addLayout(hlayout_btns)
        self.btn_layout.addLayout(vlayout_pbar)            
        self.buttons['speed'] = QDial(self)                  
        self.buttons['speed'].setNotchesVisible(True)
        self.buttons['speed'].setEnabled(False)
        self.buttons['speed'].setValue(95)
        self.speed_label = QLabel('speed')
        self.speed_label.setFont( QFont('Arial',12))
        self.speed_label.setAlignment(Qt.AlignHCenter )              
        self.min_label = QLabel('Min')
        self.min_label.setFont( QFont('Arial',12))
        self.min_label.setAlignment(Qt.AlignRight | Qt.AlignBottom )
        self.max_label = QLabel('Max')
        self.max_label.setFont( QFont('Arial',12))
        self.max_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom )
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.min_label)
        hlayout.addWidget(self.buttons['speed'])
        hlayout.addWidget(self.max_label)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.speed_label)
        vlayout.addLayout(hlayout)
        self.btn_layout.addLayout(vlayout)
        self.general_layout.addLayout(self.btn_layout)    
    
            
    def simulate_start(self):
        self.thread = QThread() 
        self.simulator =  Simulator(self.workload_name, self.scenario, self.etc, self.workload_id) 
        self.simulator.moveToThread(self.thread)
        self.thread.started.connect(self.simulator.run)         
        self.thread.finished.connect(self.thread.deleteLater)  
        self.simulator.simulation_done.connect(self.report)         
        self.simulator.simulation_done.connect(self.simulator.deleteLater) 
        self.simulator.event_signal.connect(self.msg_handler)
        self.simulator.scheduler.decision.connect(self.msg_handler)
        #self.simulator.scheduler.decision.connect(self.msg_handler)
        self.simulator.simulation_done.connect(self.thread.quit)
        self.simulator.simulation_done.connect(lambda: self.buttons['reset'].setEnabled(True))
        self.simulator.simulation_done.connect(lambda: self.buttons['simulate'].setEnabled(False))
        self.simulator.simulation_done.connect(lambda: self.buttons['speed'].setEnabled(False))
        self.buttons['speed'].setEnabled(True)
        for machine in config.machines:
            machine.machine_signal.connect(self.msg_handler)
        self.buttons['simulate'].clicked.disconnect()
        self.buttons['simulate'].clicked.connect(self.simulate_start_pause)
        self.buttons['simulate'].setIcon(QIcon(f'./gui/icons/pause.png')) 
        self.simulator.pause = False
        self.buttons['reset'].setEnabled(False)
        self.thread.start() 
        

    def simulate_start_pause(self):  
        print('pause clicked!')
        if self.simulator.pause:
            self.buttons['simulate'].setIcon(QIcon(f'./gui/icons/pause.png'))             
            self.simulator.pause = False            
        else:            
            self.buttons['simulate'].setIcon(QIcon(f'./gui/icons/simulate.png'))             
            self.simulator.pause = True
            

    def reset(self):
        #config.log.close()        
        self.gv.scene.clear()
        self.progress=0
        self.pbar.setValue(0)
        self.gv.batch_queue.tasks = []
        self.gv.machine_queues.reset()
        self.buttons['simulate'].setEnabled(True)
        self.buttons['speed'].setEnabled(False)
        for machine in config.machines:
            machine.machine_signal.disconnect()
        self.simulate_start() 
        
        
        
   

    def msg_handler(self,d):
        signal_type = d['type']
        signal_data = d['data']
        time = d['time']       
        location = d['where']
        self.gv.scene.clear()
        self.gv.display_time(time)
        selected_task = None
        
        if signal_type =='arriving':            
            task = signal_data['task']
            #print(f'{location} @{time} Task {task.id} arrived')                     
            self.gv.batch_queue.tasks.append(task)

        
        elif signal_type == 'choose':
            task = signal_data['task']            
            selected_task = task
            
        elif signal_type == 'admitted':
            task = signal_data['task']
            machine = signal_data['assigned_machine']
            m_id = machine.id            
            #print(f'@{location} {time} Task {task.id} map to Machine {m_id}')
            self.gv.batch_queue.tasks.remove(task)               
            self.gv.connect_mapper_machine(m_id, QPen(Qt.red, 4), Qt.red)
            self.gv.machine_queues.m_queues[m_id].append(task)            
        
        elif signal_type == 'cancelled':
            self.progress +=100*(1/self.simulator.total_no_of_tasks)
            self.pbar.setValue(self.progress)
            task = signal_data['task']             
            self.gv.connect_to_trash(QPen(Qt.red, 4), Qt.red)
            print(f'{location} @{time} Task {task.id} cacncelled')
            self.gv.batch_queue.tasks.remove(task)
            self.gv.mapper_ui.cancelled_tasks.append(task)
                    
        elif signal_type == 'running':
            task = signal_data['task']
            machine = signal_data['assigned_machine']             
            m_id = machine.id
            #print(f'{location} @{time} Task {task.id} start running at Machine {m_id}')            
            self.gv.machine_queues.m_queues[m_id].remove(task)            
            self.gv.machine_queues.m_runnings[m_id].append(task)
        
        elif signal_type == 'completion':
            self.progress +=100*(1/self.simulator.total_no_of_tasks)
            self.pbar.setValue(self.progress)
            task = signal_data['task']
            machine= signal_data['assigned_machine']   
            m_id = machine.id
            #print(f'{location} @{time} Task {task.id} completed at Machine {m_id}')                     
            self.gv.machine_queues.m_runnings[m_id].remove(task)

        elif signal_type == 'missed':
            self.progress +=100*(1/self.simulator.total_no_of_tasks)
            self.pbar.setValue(self.progress)
            task = signal_data['task']
            machine= signal_data['assigned_machine']   
            m_id = machine.id   
            #print(f'{location} @{time} Task {task.id} dropped from Machine {m_id}')                      
            self.gv.machine_queues.m_runnings[m_id].remove(task)

        self.gv.batch_queue.outer_frame()
        self.gv.batch_queue.inner_frame()
        self.gv.mapper_ui.mapper()
        self.gv.mapper_ui.trash()
        self.gv.connecting_lines()
        
        self.gv.batch_queue.draw_tasks(selected_task)
        self.gv.machine_queues.draw_queues()
        self.gv.machine_queues.fill_queues()
        self.gv.machine_queues.runnings()        
        self.update()
    
    def report(self):
        self.simulate_pause = True
        self.report_data = self.simulator.report()
        self.buttons['simulate'].setIcon(QIcon(f'./gui/icons/simulate.png'))       
        #config.log.close()
        

    def set_timer(self,value):
       sleep_time = 0.01*(100-value)*2
       self.simulator.sleep_time = sleep_time
       self.simulator.scheduler.sleep_time = sleep_time
       for machine in config.machines:
            machine.sleep_time = sleep_time
        

    def progress_bar(self):
        self.pbar_layout = QHBoxLayout()
        self.pbar_label = QLabel('Progress')
        self.pbar_label.setFont(QFont('Arial',12))
        self.pbar = QProgressBar()
        self.progress = 0
        self.pbar.setValue(self.progress)
        self.pbar_layout.addWidget(self.pbar_label)
        self.pbar_layout.addWidget(self.pbar)

    def connect_signals(self):        
        self.buttons['simulate'].clicked.connect(self.simulate_start)
        self.buttons['reset'].clicked.connect(self.reset)
        self.buttons['speed'].valueChanged.connect(self.set_timer)
        