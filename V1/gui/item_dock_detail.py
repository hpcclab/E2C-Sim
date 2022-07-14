from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys



class ItemDockDetail(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_dock()
    

    def init_dock(self):   
        self.dock=QDockWidget(self)
        self.dock.setFloating(False)        
        self.addDockWidget(Qt.RightDockWidgetArea,self.dock)
    
    def task_in_bq(self, task):
        # title = QLabel("Task", self)
        # self.dock.setTitleBarWidget(title)

        self.tabs = QTabWidget()
        self.tab_task = QWidget()        
        self.tab_perf = QWidget()        

        self.tabs.addTab(self.tab_task, "Task")        
        self.tabs.addTab(self.tab_perf, "Performance")        
        self.tab_task.layout = QVBoxLayout(self)
        self.tab_perf.layout = QVBoxLayout(self)
        
        self.task_grid = QGridLayout(self)
        self.id_lbl = QLabel('ID')
        self.id_text = QLineEdit()
        self.id_text.setText(f'{task.id}')
        self.id_text.setReadOnly(True)
        self.id_text.setAlignment(Qt.AlignLeft)
        
        self.type_lbl = QLabel('Type')
        self.type_text = QLineEdit()
        self.type_text.setText(f"{task.type.name}")
        self.type_text.setReadOnly(True)
        self.type_text.setAlignment(Qt.AlignLeft)

        self.eet_lbl = []
        self.eet_text = []
        print(task.estimated_time)
        for m_type, eet in task.estimated_time.items():
            lbl = QLabel(f'{m_type.upper()}')            
            txt = QLineEdit(f"{eet}")
            txt.setReadOnly(True)
            txt.setAlignment(Qt.AlignLeft)
            self.eet_lbl.append(lbl)
            self.eet_text.append(txt)

        

        self.task_grid.addWidget(self.id_lbl,0,0)
        self.task_grid.addWidget(self.id_text,0,1)
        self.task_grid.addWidget(self.type_lbl,1,0)
        self.task_grid.addWidget(self.type_text,1,1)
        
        for idx, lbl in enumerate(self.eet_lbl):
            self.task_grid.addWidget(lbl,2+idx,0)
            self.task_grid.addWidget(self.eet_text[idx],idx+2,1)


        self.perf_grid = QGridLayout(self)
        self.arr_lbl = QLabel('Arrival Time')
        self.arr_text = QLineEdit()
        self.arr_text.setText(f'{task.arrival_time:6.4f}')
        self.arr_text.setReadOnly(True)
        self.arr_text.setAlignment(Qt.AlignLeft)
        

        self.start_lbl = QLabel('Start Time')
        self.start_text = QLineEdit()
        if task.start_time == float('inf'):
            self.start_text.setText(f'N/A')
        else:
            self.start_text.setText(f'{task.start_time:6.4f}')
        self.start_text.setReadOnly(True)
        self.start_text.setAlignment(Qt.AlignLeft)

        self.deferred_lbl = QLabel('Deferred#')
        self.deferred_text = QLineEdit()
        self.deferred_text.setText(f'{task.no_of_deferring}')
        self.deferred_text.setReadOnly(True)
        self.deferred_text.setAlignment(Qt.AlignLeft)

        self.assigned_lbl = QLabel('Assigned To (ID)')
        self.assigned_text = QLineEdit()
        if task.assigned_machine == None:
            self.assigned_text.setText(f'N/A')
        else:
            self.assigned_text.setText(f'{task.assigned_machine.id}')
        self.assigned_text.setReadOnly(True)
        self.assigned_text.setAlignment(Qt.AlignLeft)

        self.completion_lbl = QLabel('Completion Time')
        self.completion_text = QLineEdit()
        if task.completion_time == float('inf'):
            self.completion_text.setText(f'N/A')
        else:
            self.completion_text.setText(f'{task.completion_time:6.4f}')
        self.completion_text.setReadOnly(True)
        self.completion_text.setAlignment(Qt.AlignLeft)

        self.missed_lbl = QLabel('Missed Time')
        self.missed_text = QLineEdit()
        if task.missed_time == float('inf'):
            self.missed_text.setText(f'N/A')
        else:
            self.missed_text.setText(f'{task.missed_time:6.4f}')
        
        self.missed_text.setReadOnly(True)
        self.missed_text.setAlignment(Qt.AlignLeft)

        self.cancel_lbl = QLabel('Cancelation Time')
        self.cancel_text = QLineEdit()
        if task.drop_time == float('inf'):
            self.cancel_text.setText(f'N/A')
        else:
            self.cancel_text.setText(f'{task.drop_time:6.4f}')        
        self.cancel_text.setReadOnly(True)
        self.cancel_text.setAlignment(Qt.AlignLeft)

        self.energy_lbl = QLabel('Energy Usuage')
        self.energy_text = QLineEdit()
        self.energy_text.setText(f'{task.energy_usage:6.4f}')
        self.energy_text.setReadOnly(True)
        self.energy_text.setAlignment(Qt.AlignLeft)

        self.wasted_lbl = QLabel('Wasted Energy Usuage')
        self.wasted_text = QLineEdit()
        self.wasted_text.setText(f'{task.wasted_energy:6.4f}')
        self.wasted_text.setReadOnly(True)
        self.wasted_text.setAlignment(Qt.AlignLeft)

        
        self.perf_grid.addWidget(self.arr_lbl,0,0)
        self.perf_grid.addWidget(self.arr_text,0,1)
        self.perf_grid.addWidget(self.assigned_lbl,1,0)
        self.perf_grid.addWidget(self.assigned_text,1,1)
        self.perf_grid.addWidget(self.start_lbl,2,0)
        self.perf_grid.addWidget(self.start_text,2,1)
        self.perf_grid.addWidget(self.completion_lbl,3,0)
        self.perf_grid.addWidget(self.completion_text,3,1)
        self.perf_grid.addWidget(self.missed_lbl,4,0)
        self.perf_grid.addWidget(self.missed_text,4,1)
        self.perf_grid.addWidget(self.cancel_lbl,5,0)
        self.perf_grid.addWidget(self.cancel_text,5,1)
        self.perf_grid.addWidget(self.deferred_lbl,6,0)
        self.perf_grid.addWidget(self.deferred_text,6,1)
        self.perf_grid.addWidget(self.energy_lbl,7,0)
        self.perf_grid.addWidget(self.energy_text,7,1)
        self.perf_grid.addWidget(self.wasted_lbl,8,0)
        self.perf_grid.addWidget(self.wasted_text,8,1)

        self.tab_task.layout.addLayout(self.task_grid)                
        self.tab_task.layout.addStretch(1)
        self.tab_task.setLayout(self.tab_task.layout)

        self.tab_perf.layout.addLayout(self.perf_grid) 
        self.tab_perf.layout.addStretch(1)               
        self.tab_perf.setLayout(self.tab_perf.layout)

        self.dock.setWidget(self.tabs)



    def machine_data(self, machine):
        # title = QLabel("Machine", self)
        # self.dock.setTitleBarWidget(title)

        self.tabs = QTabWidget()
        self.tab_machine = QWidget()
        self.tab_perf = QWidget()

        self.tabs.addTab(self.tab_machine, "Machine")
        self.tabs.addTab(self.tab_perf, "Performance")
        self.tab_machine.layout = QVBoxLayout(self)
        self.tab_perf.layout = QVBoxLayout(self)
        
        
        self.machine_grid = QGridLayout(self)
        self.id_lbl = QLabel('ID')
        self.id_text = QLineEdit()
        self.id_text.setText(f'{machine.id}')
        self.id_text.setReadOnly(True)
        self.id_text.setAlignment(Qt.AlignLeft)
        
        self.p_lbl = QLabel('Power')
        self.p_text = QLineEdit()
        self.p_text.setText(f"{machine.specs['power']}")
        self.p_text.setReadOnly(True)
        self.p_text.setAlignment(Qt.AlignLeft)
        
        self.q_lbl = QLabel('Queue Size')
        self.q_text = QLineEdit()
        self.q_text.setText(f'{machine.queue_size}')
        self.q_text.setReadOnly(True)
        self.q_text.setAlignment(Qt.AlignLeft)
        
        self.machine_grid.addWidget(self.id_lbl,0,0)
        self.machine_grid.addWidget(self.id_text,0,1)
        self.machine_grid.addWidget(self.p_lbl,1,0)
        self.machine_grid.addWidget(self.p_text,1,1)
        self.machine_grid.addWidget(self.q_lbl,2,0)
        self.machine_grid.addWidget(self.q_text,2,1)


        self.perf_grid = QGridLayout(self)
        self.assigned_lbl = QLabel('Assigned Tasks#')
        self.assigned_text = QLineEdit()
        self.assigned_text.setText(f"{machine.stats['assigned_tasks']}")
        self.assigned_text.setReadOnly(True)
        self.assigned_text.setAlignment(Qt.AlignLeft)

        self.completed_lbl = QLabel('Completed Tasks#')
        self.completed_text = QLineEdit()
        self.completed_text.setText(f"{machine.stats['completed_tasks']}")
        self.completed_text.setReadOnly(True)
        self.completed_text.setAlignment(Qt.AlignLeft)

        self.missed_lbl = QLabel('Missed Tasks#')
        self.missed_text = QLineEdit()
        self.missed_text.setText(f"{machine.stats['missed_BE_tasks']}")
        self.missed_text.setReadOnly(True)
        self.missed_text.setAlignment(Qt.AlignLeft)

        self.energy_lbl = QLabel('Energy Usage')
        self.energy_text = QLineEdit()
        self.energy_text.setText(f"{machine.stats['energy_usage']:6.3f}")
        self.energy_text.setReadOnly(True)
        self.energy_text.setAlignment(Qt.AlignLeft)


        self.wasted_lbl = QLabel('Wasted Energy')
        self.wasted_text = QLineEdit()
        self.wasted_text.setText(f"{machine.stats['wasted_energy']:6.3f}")
        self.wasted_text.setReadOnly(True)
        self.wasted_text.setAlignment(Qt.AlignLeft)

        self.idle_lbl = QLabel('Idle Energy Usage')
        self.idle_text = QLineEdit()
        self.idle_text.setText(f"{machine.stats['idle_energy_usage']:6.3f}")
        self.idle_text.setReadOnly(True)
        self.idle_text.setAlignment(Qt.AlignLeft)

        self.perf_grid.addWidget(self.assigned_lbl,0,0)
        self.perf_grid.addWidget(self.assigned_text,0,1)
        self.perf_grid.addWidget(self.completed_lbl,1,0)
        self.perf_grid.addWidget(self.completed_text,1,1)
        self.perf_grid.addWidget(self.missed_lbl,2,0)
        self.perf_grid.addWidget(self.missed_text,2,1)
        self.perf_grid.addWidget(self.energy_lbl,3,0)
        self.perf_grid.addWidget(self.energy_text,3,1)
        self.perf_grid.addWidget(self.wasted_lbl,4,0)
        self.perf_grid.addWidget(self.wasted_text,4,1)
        self.perf_grid.addWidget(self.idle_lbl,5,0)
        self.perf_grid.addWidget(self.idle_text,5,1)

        self.tab_machine.layout.addLayout(self.machine_grid)                
        self.tab_machine.layout.addStretch(1)
        self.tab_machine.setLayout(self.tab_machine.layout)

        self.tab_perf.layout.addLayout(self.perf_grid) 
        self.tab_perf.layout.addStretch(1)               
        self.tab_perf.setLayout(self.tab_perf.layout)

        self.dock.setWidget(self.tabs)

        
    def trash_data(self, cancelled_tasks):        
        widget = QWidget(self)
        vlayout=QVBoxLayout()        
        self.tableWidget = QTableWidget()        
        self.tableWidget.setRowCount(len(cancelled_tasks)) 
        self.tableWidget.setColumnCount(4) 

        for idx, task in enumerate(cancelled_tasks):
            self.tableWidget.setItem(idx,0, QTableWidgetItem(f"{task.id}"))
            self.tableWidget.setItem(idx,1, QTableWidgetItem(f"{task.type.name}"))
            self.tableWidget.setItem(idx,2, QTableWidgetItem(f"{task.arrival_time:6.2f}"))
            self.tableWidget.setItem(idx,3, QTableWidgetItem(f"{task.drop_time:6.2f}"))

            self.tableWidget.item(idx,0).setTextAlignment(Qt.AlignHCenter)
            self.tableWidget.item(idx,1).setTextAlignment(Qt.AlignHCenter)
            self.tableWidget.item(idx,2).setTextAlignment(Qt.AlignHCenter)
            self.tableWidget.item(idx,3).setTextAlignment(Qt.AlignHCenter)
        
            if idx%2 == 0 :
                self.tableWidget.item(idx,0).setBackground(Qt.white )
                self.tableWidget.item(idx,1).setBackground(Qt.white )
                self.tableWidget.item(idx,2).setBackground(Qt.white)
                self.tableWidget.item(idx,3).setBackground(Qt.white)
            else:
                self.tableWidget.item(idx,0).setBackground(QColor(205,205,205) )
                self.tableWidget.item(idx,1).setBackground(QColor(205,205,205) )
                self.tableWidget.item(idx,2).setBackground(QColor(205,205,205))
                self.tableWidget.item(idx,3).setBackground(QColor(205,205,205))

            
        self.tableWidget.setHorizontalHeaderLabels(["Task ID", "Type", f"Arrival\nTime", f"Cancellation\nTime"])
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        vlayout.addWidget(self.tableWidget)
        vlayout.addStretch(1)
        widget.setLayout(vlayout)
        self.dock.setWidget(widget)