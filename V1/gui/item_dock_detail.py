from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys,csv



class ItemDockDetail(QMainWindow):

    def __init__(self):
        super().__init__()
        self.configs={'mapper':{'immediate':True,
                                'policy':'FirstCome-FirstServe'}}
        self.mapper_enabled = True        
        self.workload_path = './workloads/default/workload.csv'
        self.path_to_etc = './task_machine_performance/default/etc.csv'
        self.etc_editable = True
        

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
        #print(task.estimated_time)
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

        self.deferred_lbl = QLabel('#of deferred')
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

    def machine_etc(self, tt, mt):                
        self.tabs = QTabWidget()
        self.tab_etc = QWidget()
        self.tabs.addTab(self.tab_etc, "Profiling Table (ETC)")        
        self.tab_etc.layout = QVBoxLayout(self)        
        self.etc_grid = QGridLayout(self)    

            
        self.etc_matrix = QTableWidget()        
        etc = []
        mt = []
        tt = []

        with open(self.path_to_etc,'r') as workload:
            etc_reader = csv.reader(workload) 
            mt = next(etc_reader)[1:]
            for idx, row in enumerate(etc_reader):
                tt.append(row[0])
                etc.append(row[1:])  

        self.etc_matrix.setRowCount(len(tt)) 
        self.etc_matrix.setColumnCount(len(mt)) 
        
        for i in range(len(tt)):                
                for j in range(len(mt)):        
                    cell_item = QTableWidgetItem(str(etc[i][j]))
                    self.etc_matrix.setItem(i,j, cell_item) 
                    
        if not self.etc_editable:
            self.etc_matrix.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.etc_matrix.setHorizontalHeaderLabels(mt)        
        self.etc_matrix.setVerticalHeaderLabels(tt)
        self.etc_matrix.horizontalHeader().setStretchLastSection(True)
        self.etc_matrix.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

                    

        self.etc_matrix.horizontalHeader().sectionDoubleClicked.connect(self.changeHorizontalHeader)
        self.etc_matrix.verticalHeader().sectionDoubleClicked.connect(self.changeVerticalHeader)
        self.etc_generate = QPushButton('Submit')
        self.etc_edit = QPushButton('Edit')
        self.etc_edit.clicked.connect(self.enable_etc_table)
       
        self.etc_grid.addWidget(self.etc_matrix,0,0, len(tt),len(mt))
        self.etc_grid.addWidget(self.etc_edit,1+len(tt),0,1,len(mt)/2)
        self.etc_grid.addWidget(self.etc_generate,1+len(tt),(len(mt)/2)+1,1,len(mt)/2)        
        self.tab_etc.layout.addLayout(self.etc_grid)                
        self.tab_etc.layout.addStretch(1)
        self.tab_etc.setLayout(self.tab_etc.layout)
        self.dock.setWidget(self.tabs)

    def enable_etc_table(self):
        if not self.etc_editable:
            self.etc_matrix.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)            
            self.etc_editable = True



    @pyqtSlot(int)
    def changeHorizontalHeader(self, index):
        it = self.etc_matrix.horizontalHeaderItem(index)
        if it is None:
            val = self.etc_matrix.model().headerData(index, Qt.Horizontal)
            it = QTableWidgetItem(str(val))
            self.etc_matrix.setHorizontalHeaderItem(index, it)
        oldHeader = it.text()
        newHeader, okPressed  = QInputDialog.getText(self,
            'Machine Type Name', "New machine type name:", 
            QLineEdit.Normal, oldHeader)
        if okPressed:
            it.setText(newHeader)

    @pyqtSlot(int)
    def changeVerticalHeader(self, index):
        it = self.etc_matrix.verticalHeaderItem(index)
        if it is None:
            val = self.etc_matrix.model().headerData(index, Qt.Horizontal)
            it = QTableWidgetItem(str(val))
            self.etc_matrix.setVerticalHeaderItem(index, it)
        oldHeader = it.text()
        newHeader, okPressed  = QInputDialog.getText(self,
            'Task Type Name', "New task type name:", 
            QLineEdit.Normal, oldHeader)
        if okPressed:
            it.setText(newHeader)


    def homo_selected(self):
        for row in range(self.etc_matrix.rowCount()):
            for column in range(self.etc_matrix.columnCount()):
                self.etc_matrix.setItem(row, column,QTableWidgetItem(self.homo_et.text())) 
    
    def hete_selected(self):
        self.etc_matrix.clearContents()
        self.homo_et.clear()
        self.homo_et.setReadOnly(True)


    def set_mq(self):
        self.tabs = QTabWidget()
        self.tab_mq = QWidget()
        self.tabs.addTab(self.tab_mq, "Machine Queue")        
        self.tab_mq.layout = QVBoxLayout(self)        
        self.mq_grid = QGridLayout(self)        
        
        self.mq_lbl = QLabel('Machine queue size')
        self.mq_size = QLineEdit()
        self.mq_size.setToolTip('The size of machine queues')
        if self.configs['mapper']['immediate']:
            self.mq_size.setText("unlimited")
        else:
            self.mq_size.setText("")
        self.mq_size.setReadOnly(False)
        self.mq_size.setAlignment(Qt.AlignLeft)
        
        self.mq_grid.addWidget(self.mq_lbl,0,0)
        self.mq_grid.addWidget(self.mq_size,1,0)
              
        self.tab_mq.layout.addLayout(self.mq_grid)                
        self.tab_mq.layout.addStretch(1)
        self.tab_mq.setLayout(self.tab_mq.layout)
        self.dock.setWidget(self.tabs)


    def set_bq(self):
        self.tabs = QTabWidget()
        self.tab_bq = QWidget()
        self.tabs.addTab(self.tab_bq, "Batch Queue")        
        self.tab_bq.layout = QVBoxLayout(self)        
        self.bq_grid = QGridLayout(self)        
        
        self.bq_lbl = QLabel('Batch queue size')
        self.bq_size = QLineEdit()
        self.bq_size.setText("")
        self.bq_size.setReadOnly(False)
        self.bq_size.setAlignment(Qt.AlignLeft)
        
        self.bq_grid.addWidget(self.bq_lbl,0,0)
        self.bq_grid.addWidget(self.bq_size,1,0)
              
        self.tab_bq.layout.addLayout(self.bq_grid)                
        self.tab_bq.layout.addStretch(1)
        self.tab_bq.setLayout(self.tab_bq.layout)
        self.dock.setWidget(self.tabs)


    def machine_data(self, machine):       
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
        self.assigned_lbl = QLabel('#of Assigned Tasks')
        self.assigned_text = QLineEdit()
        self.assigned_text.setText(f"{machine.stats['assigned_tasks']}")
        self.assigned_text.setReadOnly(True)
        self.assigned_text.setAlignment(Qt.AlignLeft)

        self.completed_lbl = QLabel('#of completed Tasks')
        self.completed_text = QLineEdit()
        self.completed_text.setText(f"{machine.stats['completed_tasks']}")
        self.completed_text.setReadOnly(True)
        self.completed_text.setAlignment(Qt.AlignLeft)

        self.missed_lbl = QLabel('#of Missed Tasks')
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

            self.tableWidget.item(idx,0).setTextAlignment(Qt.AlignCenter)
            self.tableWidget.item(idx,1).setTextAlignment(Qt.AlignCenter)
            self.tableWidget.item(idx,2).setTextAlignment(Qt.AlignCenter)
            self.tableWidget.item(idx,3).setTextAlignment(Qt.AlignCenter)
        
            if idx%2 == 0 :
                self.tableWidget.item(idx,0).setBackground(QColor(250,250,250) )
                self.tableWidget.item(idx,1).setBackground(QColor(250,250,250) )
                self.tableWidget.item(idx,2).setBackground(QColor(250,250,250))
                self.tableWidget.item(idx,3).setBackground(QColor(250,250,250))
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

    
    def task_others(self, other_tasks):        
        widget = QWidget(self)
        vlayout=QVBoxLayout()        
        self.tableWidget = QTableWidget()        
        self.tableWidget.setRowCount(len(other_tasks)) 
        self.tableWidget.setColumnCount(4) 

        for idx, task in enumerate(other_tasks):
            self.tableWidget.setItem(idx,0, QTableWidgetItem(f"{task.id}"))
            self.tableWidget.setItem(idx,1, QTableWidgetItem(f"{task.type.name}"))
            self.tableWidget.setItem(idx,2, QTableWidgetItem(f"{task.arrival_time:6.2f}"))
            self.tableWidget.setItem(idx,3, QTableWidgetItem(f"{task.deadline:6.2f}"))

            self.tableWidget.item(idx,0).setTextAlignment(Qt.AlignCenter)
            self.tableWidget.item(idx,1).setTextAlignment(Qt.AlignCenter)
            self.tableWidget.item(idx,2).setTextAlignment(Qt.AlignCenter)
            self.tableWidget.item(idx,3).setTextAlignment(Qt.AlignCenter)
        
            if idx%2 != 0 :
                self.tableWidget.item(idx,0).setBackground(QColor(250,250,250) )
                self.tableWidget.item(idx,1).setBackground(QColor(250,250,250) )
                self.tableWidget.item(idx,2).setBackground(QColor(250,250,250))
                self.tableWidget.item(idx,3).setBackground(QColor(250,250,250))
            else:
                self.tableWidget.item(idx,0).setBackground(QColor(205,205,205) )
                self.tableWidget.item(idx,1).setBackground(QColor(205,205,205) )
                self.tableWidget.item(idx,2).setBackground(QColor(205,205,205))
                self.tableWidget.item(idx,3).setBackground(QColor(205,205,205))

            
        self.tableWidget.setHorizontalHeaderLabels(["Task ID", "Type", f"Arrival\nTime", f"Deadline"])
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        vlayout.addWidget(self.tableWidget)
        vlayout.addStretch(1)
        widget.setLayout(vlayout)
        self.dock.setWidget(widget)

    
    def mapper_data(self, enabled):
        self.tabs = QTabWidget()
        self.tab_mapper = QWidget()

        self.tabs.addTab(self.tab_mapper, "Scheduler")        
        self.tab_mapper.layout = QVBoxLayout(self)

        self.mapper_grid = QGridLayout(self)

        self.rb_immediate = QRadioButton('Immediate Scheduling')
        self.rb_batch = QRadioButton('Batch Scheduling')
       
        self.rb_immediate.setChecked(self.configs['mapper']['immediate'])
        self.rb_batch.setChecked(not self.configs['mapper']['immediate'])

        self.rb_immediate.toggled.connect(lambda:self.rb_policy_state(self.rb_immediate))
        self.rb_batch.toggled.connect(lambda:self.rb_policy_state(self.rb_batch))

        self.immediate_lbl = QLabel('Policy')
        self.immediate_cb = QComboBox(self)        
        self.immediate_policies = ['FirstCome-FirstServe',
                            'Min-Expected-Completion-Time',
                            'Min-Expected-Execution-Time',
                            ]
        
        self.immediate_cb.addItems(self.immediate_policies) 
        self.immediate_cb.setEnabled(self.rb_immediate.isChecked())
        
         

        self.batch_lbl = QLabel('Policy')
        self.batch_cb = QComboBox(self)
        self.batch_policies = ['FELARE',
                            'ELARE',
                            'MinCompletion-MinCompletion',
                            'MinCompletion-SoonestDeadline',
                            'MinCompletion-MaxUrgency',
                        ]       
        self.batch_cb.addItems(self.batch_policies) 
        self.batch_cb.setEnabled(self.rb_batch.isChecked())        

        style =  "QComboBox QAbstractItemView {"
        style += " border: 2px solid grey;"
        style += " background: white;"
        style += " selection-background-color: blue;"
        style += " }"
        style += " QComboBox {"
        style += " background: white;"
        style += " selection-background-color: blue;"
        style += "}"
        self.immediate_cb.setStyleSheet(style)
        self.batch_cb.setStyleSheet(style)
        
        if self.rb_immediate.isChecked():
            self.immediate_cb.setCurrentText(self.configs['mapper']['policy'])
        else:
            self.batch_cb.setCurrentText(self.configs['mapper']['policy'])

        if not enabled:
            self.rb_immediate.setCheckable(False)
            self.rb_batch.setCheckable(False)

            self.immediate_cb.setEnabled(False)
            self.batch_cb.setEnabled(False)

        self.mapper_grid.addWidget(self.rb_immediate,0,0,1,2)   
        self.mapper_grid.addWidget(self.immediate_lbl,1,0)        
        self.mapper_grid.addWidget(self.immediate_cb,1,1)

        self.mapper_grid.addWidget(self.rb_batch,3,0,1,2)   
        self.mapper_grid.addWidget(self.batch_lbl,4,0)        
        self.mapper_grid.addWidget(self.batch_cb,4,1)
        
        
        self.tab_mapper.layout.addLayout(self.mapper_grid)                
        self.tab_mapper.layout.addStretch(1)
        self.tab_mapper.setLayout(self.tab_mapper.layout)
        self.dock.setWidget(self.tabs)
    

    def rb_policy_state(self,rb):
        if rb.isChecked():
            if rb.text() == 'Immediate Scheduling':
                self.immediate_cb.setEnabled(True)
                self.batch_cb.setEnabled(False)
            else:
                self.immediate_cb.setEnabled(False)
                self.batch_cb.setEnabled(True)
    
    def workload_data(self, enabled):
        self.tabs = QTabWidget()
        self.tab_workload = QWidget()

        self.tabs.addTab(self.tab_workload, "Workload")        
        self.tab_workload.layout = QVBoxLayout(self)

        self.workload_grid = QGridLayout(self)

        

        self.path_entry = QLineEdit(self)
        self.path_entry.setStyleSheet("QLineEdit"
                        "{"
                        "background : white;"
                        "}")
        self.path_entry.setText(self.workload_path)
        self.browse_btn = QPushButton('Load', self)
        self.browse_btn.clicked.connect(self.get_workload_file)


        self.workload_table = QTableWidget()        
        self.workload_table.setRowCount(0) 
        self.workload_table.setColumnCount(2) 

        self.workload_table.setHorizontalHeaderLabels(['Task Type', 'Arrival Time'])
        self.workload_table.horizontalHeader().setStretchLastSection(True)
        self.workload_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)        
        with open(self.workload_path,'r') as workload:
            workload_reader = csv.reader(workload)     
            next(workload_reader)        
            for idx, row in enumerate(workload_reader):                 
                self.workload_table.setRowCount(idx+1) 
                type_item = QTableWidgetItem(row[0])       
                arrival_item = QTableWidgetItem(str(row[1]))
                self.workload_table.setItem(idx, 0, type_item)
                self.workload_table.setItem(idx, 1, arrival_item )            
                type_item.setFlags(type_item.flags() ^ Qt.ItemIsEditable)
                arrival_item.setFlags(arrival_item.flags() ^ Qt.ItemIsEditable)
            

        self.workload_grid.addWidget(self.path_entry,0,0)        
        self.workload_grid.addWidget(self.browse_btn,0,1)   
        
        self.tab_workload.layout.addLayout(self.workload_grid) 
        self.tab_workload.layout.addWidget(self.workload_table)               
        self.tab_workload.layout.addStretch(1)
        self.tab_workload.setLayout(self.tab_workload.layout)
        self.dock.setWidget(self.tabs)
    
    def get_workload_file(self):     
        loaded_path  = QFileDialog.getOpenFileName(self, caption='Choose File',
                                                    directory=QDir.currentPath(),
                                                    filter='*.csv')
        if loaded_path[0]:
            self.workload_path = loaded_path[0]
        
        self.path_entry.setText(self.workload_path)
        with open(self.workload_path,'r') as workload:
            workload_reader = csv.reader(workload)     
            next(workload_reader)        
            for idx, row in enumerate(workload_reader):                                
                self.workload_table.setRowCount(idx+1)
                type_item = QTableWidgetItem(row[0])       
                arrival_item = QTableWidgetItem(str(row[1]))
                self.workload_table.setItem(idx, 0, type_item)
                self.workload_table.setItem(idx, 1, arrival_item)
                type_item.setFlags(type_item.flags() ^ Qt.ItemIsEditable)
                arrival_item.setFlags(arrival_item.flags() ^ Qt.ItemIsEditable)
            
    
    

        
         
            




    