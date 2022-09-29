import sys, time, csv
from gui.reports import FullReport, MachineReport, TaskReport, SummaryReport
from gui.help import HelpMenu
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
import pandas as pd


class SimUi(QMainWindow):
    
    def __init__(self,w,h,path_to_arrivals, path_to_etc, path_to_reports):
        super().__init__()
        self.path_to_arrivals = path_to_arrivals
        self.path_to_etc= path_to_etc
        self.path_to_reports = path_to_reports

        self.title = "E2C Simulator"
        self.top= 20
        self.left= 20      
        self.width = w
        self.height = h        
        self.setWindowTitle(self.title)        
        self.setStyleSheet(f"background-color: rgb(217,217,217);")
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.configs ={ 'scheduler': 'default',
                        'immediate_scheduling': True,
                        'mq_size':'unlimited',
                        'workload': 'default',
                        'machines':'default',
                        'etc':'default',
                         }
        self.sim_done = 0

        menu = self.menuBar()
        self.report_menu = menu.addMenu("Reports")
        self.help_menu = menu.addMenu("Help")

        self.full_report = QAction("&Full Report", self)
        self.full_report.setToolTip("Display full report of simulation")
        self.full_report.triggered.connect(self.full_report_action)

        self.task_report = QAction("&Task Report", self)
        self.task_report.setToolTip("Display task-centric report of simulation")
        self.task_report.triggered.connect(self.task_report_action)

        self.mach_report = QAction("&Machine Report", self)
        self.mach_report.setToolTip("Display machine-centric report of simulation")
        self.mach_report.triggered.connect(self.mach_report_action)

        self.summary_report = QAction("&Summary Report", self)
        self.summary_report.setToolTip("Display a summary report of simulation")
        self.summary_report.triggered.connect(self.summary_report_action)

        help = QAction("About ...", self)
        help.triggered.connect(self.help_menu_action)

        self.report_menu.addAction(self.full_report)
        self.report_menu.addAction(self.task_report)
        self.report_menu.addAction(self.mach_report)
        self.report_menu.addAction(self.summary_report)
        self.report_menu.setToolTipsVisible(True)
        self.report_menu.setEnabled(True)
        self.full_report.setEnabled(False)
        self.task_report.setEnabled(False)
        self.mach_report.setEnabled(False)
        self.summary_report.setEnabled(False)

        self.help_menu.addAction(help)

        self.report_menu.setStyleSheet("""QMenu::item::selected { background-color: blue; } """)
        self.help_menu.setStyleSheet("""QMenu::item::selected { background-color: blue; } """)

        self.center()
        #self.showMaximized()
        
        self.initUI()

    def full_report_action(self):
        self.report = FullReport(self.path_to_reports, config.scheduling_method)

    def task_report_action(self):
        self.report = TaskReport(self.path_to_reports, config.scheduling_method)

    def mach_report_action(self):
        self.report = MachineReport(self.path_to_reports, config.scheduling_method)
    
    def summary_report_action(self):
        self.report = SummaryReport(self.path_to_reports, config.scheduling_method)
    
    def help_menu_action(self):
        self.simulate_pause = True
        self.help_menu = HelpMenu()

    def initUI(self):
        self.general_layout = QVBoxLayout() 
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.general_layout)
        #self.label = QLabel('simulator')
        #self.general_layout.addWidget(self.label)
        self.gv = GraphicView(self.width, self.height)   
        
        
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
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

       

    def dock_update(self,item):
         
        if item.data(0) == 'task_in_bq' or item.data(0) == 'task_in_mq' or item.data(0)=='task_in_machine' :      
            self.dock_right.task_in_bq(item.data(1)) 
        elif item.data(0) == 'task_in_bq_others':            
            self.dock_right.task_others(self.gv.batch_queue.tasks[self.gv.batch_queue.size-1:])

        elif item.data(0) == 'task_in_mq_others':           
            m_id = item.data(1)
            self.dock_right.task_others(self.gv.machine_queues.m_queues[m_id][self.gv.machine_queues.max_qsize-1:])

        elif item.data(0) == 'machine':            
            self.dock_right.machine_data(item.data(1))

        elif item.data(0) == 'machines_frame':            
            # tt = config.task_type_names
            # mt = config.machine_type_names            
            # self.dock_right.machine_etc(tt, mt)
            # self.dock_right.etc_generate.clicked.connect(self.set_etc)
            pass
            
        elif item.data(0) == 'machine_queues_frame': 
            self.dock_right.set_mq()
            self.dock_right.mq_size.returnPressed.connect(self.set_mq_size)
        
        # elif item.data(0) == 'batch_queue_frame': 
        #     self.dock_right.set_bq()
        #     self.dock_right.bq_size.returnPressed.connect(self.set_bq_size)

        elif item.data(0) == 'trash':
            self.dock_right.trash_data(self.gv.mapper_ui.cancelled_tasks)

        elif item.data(0) == 'trash_missed':
            self.dock_right.trash__missed_data(self.gv.machine_queues.missed_tasks_machines)

        elif item.data(0) == 'mapper':                        
            try:
                scheduler = self.simulator.scheduler.name
                self.dock_right.mapper_data(0)
            except:
                self.dock_right.mapper_data(1)
                self.dock_right.rb_immediate.toggled.connect(lambda:self.rb_policy_state(self.dock_right.rb_immediate))
                self.dock_right.rb_batch.toggled.connect(lambda:self.rb_policy_state(self.dock_right.rb_batch))
                self.dock_right.immediate_cb.activated.connect(self.set_scheduler)
                self.dock_right.batch_cb.activated.connect(self.set_scheduler)

        elif item.data(0) == 'workload':   
            tt = config.task_type_names
            mt = config.machine_type_names  
            self.dock_right.workload_data(0,tt, mt)
            self.dock_right.path_entry.textChanged.connect(self.set_arrival_path)
            self.dock_right.etc_generate.clicked.connect(self.set_etc)
            
            try:
                self.simulator
                self.dock_right.etc_generate.setEnabled(False)
                self.dock_right.etc_load.setEnabled(False)
                self.dock_right.etc_edit.setEnabled(False)
                self.dock_right.load_wl_btn.setEnabled(False)
                self.dock_right.etc_matrix.setEditTriggers(QAbstractItemView.NoEditTriggers)
            except:
                pass
            
        self.gv.scene.update()

    def rb_policy_state(self, rb):        
        if rb.isChecked():
            if rb.text() == 'Immediate Scheduling':
                self.dock_right.configs['mapper']['immediate'] = True
                mq_size = float('inf')
                config.machine_queue_size = mq_size
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Machine queue size is unlimited for immediate scheduling!")
                msg.setWindowTitle("Warning MessageBox")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                config.machine_queue_size = mq_size
                for machine in config.machines:
                    machine.queue_size = config.machine_queue_size
                    machine.recreate_queue()
                self.gv.machine_queues.max_qsize = 5        
                self.gv.machine_queues.draw_queues()
                self.gv.scene.update()
            else:
                self.dock_right.configs['mapper']['immediate'] = False        
        self.configs['immediate_scheduling'] = self.dock_right.configs['mapper']['immediate']        
        
            
    
    def set_arrival_path(self):
        print(f'wlPath: {self.dock_right.workload_path}')
        print(f'txt_entry: {self.dock_right.path_entry.text()}')
        self.path_to_arrivals = self.dock_right.path_entry.text()
        #self.path_to_arrivals = self.dock_right.workload_path
        

    def set_mq_size(self):
        mq_size = int(self.dock_right.mq_size.text())
        if self.configs['immediate_scheduling']:
            print('here')
            mq_size = float('inf')
            config.machine_queue_size = mq_size
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Machine queue size is unlimited for immediate scheduling!")
            msg.setWindowTitle("Warning MessageBox")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()

        config.machine_queue_size = mq_size
        for machine in config.machines:
            machine.queue_size = config.machine_queue_size
            machine.recreate_queue()
        if mq_size >5 :
            mq_size = 5        
        self.gv.machine_queues.max_qsize = mq_size
        self.dock_right.mq_size.setReadOnly(True)
        self.gv.machine_queues.draw_queues()
        self.gv.scene.update()
    
    def set_bq_size(self):
        bq_size = int(self.dock_right.bq_size.text())
        config.batch_queue_size = bq_size        
        if bq_size >5 :
            bq_size = 5        
        self.gv.batch_queue.size = bq_size
        self.dock_right.bq_size.setReadOnly(True)
        self.gv.batch_queue.inner_frame()
        self.gv.scene.update()

    
    def activate_mapper(self, enabled):
        if enabled:
            self.dock_right.mapper_enabled = True
        else:
            self.dock_right.mapper_enabled = False

    def create_logos(self, hlayout_btns):
        #--------------------------------------------
        right_dummy = QLabel('         ')
        logo_dummy = QLabel(' ')

        hpcc_label = QLabel(self)
        pixmap = QPixmap(f'./gui/icons/hpccLogo.png')
        hpcc_label.setPixmap(pixmap)
        hlayout_btns.addWidget(hpcc_label,Qt.AlignLeft)
        hlayout_btns.addWidget(logo_dummy) 

        ull_label = QLabel(self)
        pixmap = QPixmap(f'./gui/icons/ullLogo.png')
        ull_label.setPixmap(pixmap)
        hlayout_btns.addWidget(ull_label,Qt.AlignLeft)
        hlayout_btns.addWidget(logo_dummy) 

        nsf_label = QLabel(self)
        pixmap = QPixmap(f'./gui/icons/nsfLogo.png')
        nsf_label.setPixmap(pixmap)
        hlayout_btns.addWidget(nsf_label,Qt.AlignLeft)

        
        right_dummy.setMinimumWidth(20)
        hlayout_btns.addWidget(right_dummy) 
        #--------------------------------------------


    def create_ctrl_buttons(self):
        self.buttons = {'reset':None,
                        'simulate':None,
                        'increment':None}
        bcg_style = "{color: #333; border: 1 px solid #555; \
                    border-radius: 12px; border-style: outset; \
                    background: qradialgradient( cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, radius: 1.35, stop: 0 #fff, stop: 1 #888 ); \
                    padding: 5px;}"         
        self.btn_layout =  QHBoxLayout()
        hlayout_btns = QHBoxLayout()
        vlayout_pbar = QVBoxLayout()
        # dummy = QLabel('         ')
        # dummy.setMinimumWidth(70)
        # hlayout_btns.addWidget(dummy)
        self.create_logos(hlayout_btns)
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
        self.buttons['increment'].setEnabled(False)          
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
    

    def set_etc(self):
        etc_matrix = self.dock_right.etc_matrix
        not_matched_tt = self.check_etc_format(etc_matrix)

        if not_matched_tt:
            return
        self.dock_right.path_to_etc = './task_machine_performance/gui_generated/etc.csv'
        with open(self.dock_right.path_to_etc,'w') as etc_file:
            etc_writer = csv.writer(etc_file)
            machine_types = []
            for clmn_idx in range(etc_matrix.columnCount()):                
                machine_types.append(etc_matrix.horizontalHeaderItem(clmn_idx).text())            
            machine_types = [''] + machine_types
            etc_writer.writerow(machine_types)
            task_types= []
            for row_count in range(etc_matrix.rowCount()):                
                row = [etc_matrix.item(row_count, column_count).text() for column_count in range(etc_matrix.columnCount())]                                
                task_type_name = etc_matrix.verticalHeaderItem(row_count).text()
                task_types.append(task_type_name)
                row = [task_type_name] + row                
                etc_writer.writerow(row) 
        for idx, mt in enumerate(config.machine_types):
            mt.name = machine_types[idx+1]
        for idx, tt in enumerate(config.task_types):
            tt.name = task_types[idx]
        
        for machine in config.machines:
                machine.reset_tt_stats()
                
        

        self.path_to_etc = f'./task_machine_performance/gui_generated/etc.csv'
        self.dock_right.etc_matrix.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dock_right.etc_editable = False  
    
    def check_etc_format(self, etc_matrix):
        task_types_etc = []
        workload = pd.read_csv(self.dock_right.workload_path)
        for row_count in range(etc_matrix.rowCount()):
            task_type_name = etc_matrix.verticalHeaderItem(row_count).text()
            task_types_etc.append(task_type_name)
            workload = workload.replace(to_replace=f'T{row_count+1}', value = task_type_name)
        
        task_types_wl = workload['task_type'].unique()        
        not_matched_tt = [tt for tt in task_types_wl if tt not in task_types_etc]
        if not_matched_tt:
            err_txt = f"Task type {not_matched_tt} in workload are not found in ETC"
            self.err_msg('Format Error', err_txt)
            return not_matched_tt
        else:
            workload.to_csv(self.dock_right.workload_path, index = False)
            self.dock_right.rewrite_workload_table()

        

        
        return not_matched_tt
    
    def err_msg(self, err_title, err_txt):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(f"{err_txt}")
        msg.setWindowTitle(f"{err_title}")
        msg.setStandardButtons(QMessageBox.Cancel)
        msg.exec_()

    def set_scheduler(self):
        if self.dock_right.rb_immediate.isChecked():
            self.dock_right.configs['mapper']['policy'] = self.dock_right.immediate_cb.currentText()
            # self.dock_right.configs['mapper']['immediate'] = True
        else:
            self.dock_right.configs['mapper']['policy'] = self.dock_right.batch_cb.currentText()
            # self.dock_right.configs['mapper']['immediate'] = False
        
        self.policy = self.dock_right.configs['mapper']['policy']
        
        if self.policy ==   'MinCompletion-MinCompletion':
            self.policy = 'MM'
        elif self.policy ==   'MinCompletion-SoonestDeadline':
            self.policy = 'MSD'
        elif self.policy == 'MinCompletion-MaxUrgency':
            self.policy = 'MMU'
        elif self.policy == 'FELARE':
            self.policy == 'FEE'
        elif self.policy == 'ELARE':
            self.policy = 'EE'
        elif self.policy == 'FirstCome-FirstServe':
            self.policy = 'FCFS'
        elif self.policy == 'Min-Expected-Completion-Time':
            self.policy = 'MECT'
        elif self.policy == 'Min-Expected-Execution-Time':
            self.policy = 'MEET'
        self.configs['scheduler'] = self.policy
        

    def setup_config(self, simulator):
        if self.configs['scheduler'] == 'default':
            self.policy = 'FCFS'                      
        else:
            self.policy = self.configs['scheduler']                    
        simulator.set_scheduling_method(self.policy)

            
    def simulate_start(self):
        self.thread = QThread() 
        self.simulator =  Simulator(self.path_to_arrivals,self.path_to_etc, self.path_to_reports,  seed=123)         
        self.setup_config(self.simulator)       
        self.simulator.moveToThread(self.thread)
        self.thread.started.connect(self.simulator.reset)
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
        
        
        
        #self.simulator.simulation_done.connect(lambda: self.report_menu.setEnabled(True))
        self.simulator.simulation_done.connect(lambda: self.full_report.setEnabled(True))
        self.simulator.simulation_done.connect(lambda: self.mach_report.setEnabled(True))
        self.simulator.simulation_done.connect(lambda: self.task_report.setEnabled(True))
        self.simulator.simulation_done.connect(lambda: self.summary_report.setEnabled(True))
        self.simulator.simulation_done.connect(lambda: self.activate_mapper(1))
        
        self.buttons['speed'].setEnabled(True)
        self.dock_right.etc_editable = False

        try:
            self.dock_right.etc_edit
            self.dock_right.etc_load
            self.dock_right.load_wl_btn
            self.dock_right.etc_generate
            self.simulator.simulation_done.connect(lambda: self.dock_right.etc_edit.setEnabled(True))
            self.simulator.simulation_done.connect(lambda: self.dock_right.etc_load.setEnabled(True))
            self.simulator.simulation_done.connect(lambda: self.dock_right.load_wl_btn.setEnabled(True))
            self.simulator.simulation_done.connect(lambda: self.dock_right.etc_generate.setEnabled(True))
        except:
            pass

        try:            
            self.dock_right.etc_generate.setEnabled(False)
            self.dock_right.etc_load.setEnabled(False)
            self.dock_right.etc_edit.setEnabled(False)
            self.dock_right.load_wl_btn.setEnabled(False)
            self.dock_right.etc_matrix.setEditTriggers(QAbstractItemView.NoEditTriggers)
        except:
            pass
        
        for machine in config.machines:
            machine.machine_signal.connect(self.msg_handler)
        self.buttons['simulate'].clicked.disconnect()
        self.buttons['simulate'].clicked.connect(self.simulate_start_pause)
        self.buttons['simulate'].setIcon(QIcon(f'./gui/icons/pause.png')) 
        

        self.simulator.pause = False
        self.buttons['reset'].setEnabled(False)
        self.thread.start() 
        

    def simulate_start_pause(self):          
        if self.simulator.pause:
            self.buttons['simulate'].setIcon(QIcon(f'./gui/icons/pause.png'))  
            self.buttons['increment'].setEnabled(False)
            self.simulator.pause = False           
        else:            
            self.buttons['simulate'].setIcon(QIcon(f'./gui/icons/simulate.png')) 
            self.buttons['increment'].setEnabled(True)            
            self.simulator.pause = True
            

    def reset(self):
        try:
            del self.simulator
        except:
            pass
        try:
            config.log = open(f"{config.settings['path_to_output']}/log.txt",'w')
        except OSError as err:
            print(err)  
        self.full_report.setEnabled(False)
        self.task_report.setEnabled(False)
        self.mach_report.setEnabled(False)              
        self.summary_report.setEnabled(False)
        self.progress=0
        self.p_count = 0        
        self.pbar.setFormat(f'{self.p_count}/0 tasks ({self.progress}%)')
        self.pbar.setValue(self.progress)        
        self.gv.batch_queue.reset()
        self.gv.machine_queues.reset()        
        self.buttons['simulate'].setEnabled(True)
        self.buttons['speed'].setEnabled(False)
        config.time.sct(0.0)
        config.available_energy = config.total_energy
        for machine in config.machines:
            machine.reset()
            try:
                machine.machine_signal.disconnect()
            except:
                pass
        self.buttons['simulate'].clicked.disconnect()
        self.buttons['simulate'].clicked.connect(self.simulate_start)
        self.gv.scene.update()
         
        
        
        
   

    def msg_handler(self,d):
        signal_type = d['type']
        signal_data = d['data']
        time = d['time']       
        location = d['where']
        self.gv.scene.clear()
        self.gv.display_time(time)
        #self.gv.display_logos()
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
            # self.progress +=100*(1/self.simulator.total_no_of_tasks)  
            self.p_count +=1
            self.progress = round(100*self.p_count/self.simulator.total_no_of_tasks)
            self.pbar.setFormat(f'{self.p_count}/{self.simulator.total_no_of_tasks} tasks ({self.progress}%)')
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
            # self.progress +=100*(1/self.simulator.total_no_of_tasks)  
            self.p_count +=1
            self.progress = round(100*self.p_count/self.simulator.total_no_of_tasks)
            self.pbar.setFormat(f'{self.p_count}/{self.simulator.total_no_of_tasks} tasks ({self.progress}%)')
            self.pbar.setValue(self.progress)
            task = signal_data['task']
            machine= signal_data['assigned_machine']   
            m_id = machine.id
            #print(f'{location} @{time} Task {task.id} completed at Machine {m_id}')                     
            self.gv.machine_queues.m_runnings[m_id].remove(task)

        elif signal_type == 'missed':
            task = signal_data['task']
            machine = signal_data['assigned_machine'] 
            # self.progress +=100*(1/self.simulator.total_no_of_tasks) 
            self.p_count +=1
            self.progress = round(100*self.p_count/self.simulator.total_no_of_tasks)
            self.pbar.setFormat(f'{self.p_count}/{self.simulator.total_no_of_tasks} tasks ({self.progress}%)')
            self.pbar.setValue(self.progress)
            task = signal_data['task']
            machine= signal_data['assigned_machine']   
            m_id = machine.id   
            #print(f'{location} @{time} Task {task.id} dropped from Machine {m_id}')                      
            self.gv.machine_queues.m_runnings[m_id].remove(task)
            self.gv.machine_queues.missed_tasks_machines.append([task, machine])
            self.gv.machine_queues.connect_machine_running_to_trash(task, machine,QPen(Qt.red, 4), Qt.red)

        elif signal_type == 'cancelled_machine':
            # self.progress +=100*(1/self.simulator.total_no_of_tasks)  
            self.p_count +=1
            self.progress = round(100*self.p_count/self.simulator.total_no_of_tasks)           
            self.pbar.setFormat(f'{self.p_count}/{self.simulator.total_no_of_tasks} tasks ({self.progress}%)')
            self.pbar.setValue(self.progress)
            task = signal_data['task']
            machine= signal_data['assigned_machine']   
            m_id = machine.id   
            self.gv.connect_machine_to_trash(QPen(Qt.red, 4), Qt.red)
            #print(f'{location} @{time} Task {task.id} dropped from Machine {m_id}')                      
            self.gv.machine_queues.m_queues[m_id].remove(task)
            self.gv.mapper_ui.cancelled_tasks.append(task)
        #print(self.p_count,self.progress)
        self.gv.batch_queue.outer_frame()
        self.gv.batch_queue.inner_frame()
        self.gv.mapper_ui.mapper()
        self.gv.mapper_ui.trash()
        self.gv.workload_ui.draw_frame()
        self.gv.connect_workload(QPen(Qt.red, 4), Qt.red)
        self.gv.connecting_lines()
        
        self.gv.batch_queue.draw_tasks(selected_task)
        self.gv.machine_queues.outer_frame()
        self.gv.machine_queues.draw_queues()
        self.gv.machine_queues.fill_queues()
        self.gv.machine_queues.runnings()        
        self.gv.machine_queues.trash()
        self.update()
    
    def report(self):
        print("********************* report **********************")
        self.simulate_pause = True
        #self.report_data = self.simulator.report()
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
        self.pbar_label = QLabel('progress')
        self.pbar_label.setFont(QFont('Arial',12))
        
        self.pbar = QProgressBar(self)        
        self.progress = 0       
        self.p_count = 0
        self.pbar.setFormat(f'0/0 task {self.progress}%')
        self.pbar.setValue(self.progress)        
        self.pbar_layout.addWidget(self.pbar_label)
        self.pbar_layout.addWidget(self.pbar)
    
    def increment(self):       
        self.pause = True
        self.simulator.is_incremented = False

    def connect_signals(self):        
        self.buttons['simulate'].clicked.connect(self.simulate_start)
        self.buttons['reset'].clicked.connect(self.reset)
        self.buttons['speed'].valueChanged.connect(self.set_timer)
        self.buttons['increment'].clicked.connect(self.increment)
        