from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import utils.config as config
from utils.task_type import UrgencyLevel
import sys
import random


class WorkloadGenerator(QMainWindow):
    def __init__(self):
        super().__init__()

        # set the title of self.main window
        self.setWindowTitle('Workload Generator')

        # set the size of window
        self.Width = 750
        self.height = int(1.200 * self.Width)
        self.resize(self.Width, self.height)

        # add all widgets
        self.task_types_btn = QPushButton('Task Types', self)
        self.machine_types_btn = QPushButton('Machine Types', self)
        self.scenario_btn = QPushButton('Scenario', self)
        self.workload_btn = QPushButton('Workload', self)
        self.eet_btn = QPushButton('EET', self)

        self.task_types_btn.setObjectName('left_button')
        self.machine_types_btn.setObjectName('left_button')
        self.scenario_btn.setObjectName('left_button')
        self.workload_btn.setObjectName('left_button')
        self.eet_btn.setObjectName('left_button')

        self.bg_color = "background-color:rgb(210,220,230)"

        self.workload_btn.setEnabled(False)
        self.workload_btn.setStyleSheet("QPushButton{color:rgb(100,100,100);}")

        self.task_types_btn.clicked.connect(self.set_tt_tab)
        self.machine_types_btn.clicked.connect(self.set_mt_tab)
        self.scenario_btn.clicked.connect(self.set_scen_tab)
        self.workload_btn.clicked.connect(self.set_wkld_tab)
        self.eet_btn.clicked.connect(self.set_eet_tab)

        # add tabs
        self.tab1 = self.tt_ui()
        self.tab2 = self.mt_ui()
        self.tab3 = self.scen_ui()
        self.tab4 = self.wkld_ui()
        self.tab5 = self.eet_ui()

        self.initUI()

    def initUI(self):
        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.task_types_btn)
        self.left_layout.addWidget(self.machine_types_btn)
        self.left_layout.addWidget(self.scenario_btn)
        self.left_layout.addWidget(self.workload_btn)
        self.left_layout.addWidget(self.eet_btn)
        self.left_layout.addStretch(5)
        self.left_layout.setSpacing(20)
        self.left_widget = QWidget()
        self.left_widget.setLayout(self.left_layout)
        self.left_widget.setStyleSheet('''
            QPushButton{
                border:none;
                color:rgb(0,0,0);
                font-size:15px;
                font-weight:400;
                text-align:left;
            }
            QPushButton#left_button:hover{
                font-weight:600;
                background:rgb(220,220,220);
                border-left:5px solid blue;
            }
            QWidget#self.left_widget{
                background:rgb(220,220,220);
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
            }
        ''')
    
        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')
        self.right_widget.addTab(self.tab5, '')

        self.right_widget.setCurrentIndex(0)
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; height: 0; margin: 0; padding: 0; border: none;}''')

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.left_widget)
        self.main_layout.addWidget(self.right_widget)
        self.main_layout.setStretch(0, 40)
        self.main_layout.setStretch(1, 200)
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.right_widget.setCurrentIndex(0)
        self.task_types_btn.setStyleSheet('''font-weight:600;background:rgb(220,220,220);''')

    # ----------------- 
    # buttons

    def set_tt_tab(self):
        self.right_widget.setCurrentIndex(0)
        self.clean()
        self.task_types_btn.setStyleSheet('''font-weight:600;background:rgb(220,220,220);''')

    def set_mt_tab(self):
        self.right_widget.setCurrentIndex(1)
        self.clean()
        self.machine_types_btn.setStyleSheet('''font-weight:600;background:rgb(220,220,220);''')

    def set_scen_tab(self):
        self.right_widget.setCurrentIndex(2)
        self.clean()
        self.scenario_btn.setStyleSheet('''font-weight:600;background:rgb(220,220,220);''')

    def set_wkld_tab(self):
        self.right_widget.setCurrentIndex(3)
        self.clean()
        self.workload_btn.setStyleSheet('''font-weight:600;background:rgb(220,220,220);''')

    def set_eet_tab(self):
        self.right_widget.setCurrentIndex(4)
        self.clean()
        self.eet_btn.setStyleSheet('''font-weight:600;background:rgb(220,220,220);''')

    # ----------------- 
    # functions

    def clean(self):
        self.task_types_btn.setStyleSheet('''''')
        self.machine_types_btn.setStyleSheet('''''')
        self.scenario_btn.setStyleSheet('''''')
        if self.wkld_table.rowCount() != 0:
            self.workload_btn.setStyleSheet('''''')
        else: self.workload_btn.setStyleSheet('''color:rgb(100,100,100)''')
        self.eet_btn.setStyleSheet('''''')


    def tt_ui(self):
        self.main_layout = QVBoxLayout()

        self.display_tt_lbl = QLabel("Existing Task Types")
        self.display_tt_lbl.setStyleSheet('font-weight: bold')
        self.display_tt_table = QTableWidget()
        self.display_tt_table.setColumnCount(6)
        self.display_tt_table.setRowCount(len(config.task_types))          #------------make sure to change this upon adding or removing tts
        self.display_tt_table.setHorizontalHeaderLabels(["Id","Name","Data Input","Mean Data Size (KB)","Urgency","Deadline"])
        default_data_inputs = ["png","mp3","jpg","csv","mp4"]
        default_data_sizes = ["10.0","5.5","7.0","2.8"]
        for i in range(len(config.task_types)):
            id = QTableWidgetItem(str(config.task_types[i].id))
            id.setFlags(id.flags() ^ Qt.ItemIsEditable)
            self.display_tt_table.setItem(i,0,id)
            self.display_tt_table.setItem(i,1,QTableWidgetItem(str(config.task_types[i].name)))
            self.display_tt_table.setItem(i,2,QTableWidgetItem(random.choice(default_data_inputs)))
            self.display_tt_table.setItem(i,3,QTableWidgetItem(random.choice(default_data_sizes)))
            if config.task_types[i].urgency == UrgencyLevel.BESTEFFORT:
                self.display_tt_table.setItem(i,4,QTableWidgetItem("BestEffort"))
            elif config.task_types[i].urgency == UrgencyLevel.URGENT:
                self.display_tt_table.setItem(i,4,QTableWidgetItem("Urgent"))
            self.display_tt_table.setItem(i,5,QTableWidgetItem(str(config.task_types[i].deadline)))
        self.display_tt_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.display_tt_table.verticalHeader().setVisible(False)

        header = self.display_tt_table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        self.display_tt_table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)

        self.tt_h_layout = QHBoxLayout()
        self.edit_tt_table = QPushButton("Edit Table Values")
        self.edit_tt_table.setStyleSheet(self.bg_color)
        self.edit_tt_submit = QPushButton("Submit Edit Changes")
        self.edit_tt_submit.setStyleSheet(self.bg_color)
        # self.tt_h_layout.addWidget(self.edit_tt_table)
        self.tt_h_layout.addWidget(self.edit_tt_submit)

        self.add_tt_lbl = QLabel("Add Task Type")
        self.add_tt_lbl.setStyleSheet("font-weight: bold")
        self.add_tt_name_lbl = QLabel("Task Type Name")
        self.add_tt_name = QLineEdit()
        self.add_tt_dt_lbl = QLabel("Data Input")
        self.add_tt_dt = QComboBox()
        self.add_tt_dt.addItems(default_data_inputs)
        self.add_new_di = QPushButton("Create New Data Input")
        self.add_new_di.setStyleSheet(self.bg_color)
        self.add_tt_ds_lbl = QLabel("Mean Data Size (KB)")
        self.add_tt_ds = QLineEdit()

        self.add_tt_ds.setValidator(QDoubleValidator(0.99, 99.99, 3))

        self.add_tt_urgency_lbl = QLabel("Urgency")
        self.add_tt_urgency = QComboBox()
        self.add_tt_urgency.addItem("BestEffort")
        self.add_tt_urgency.addItem("Urgent")
        self.add_tt_deadline_lbl = QLabel("Deadline")
        self.add_tt_deadline = QLineEdit()

        self.add_tt_deadline.setValidator(QDoubleValidator(0.99, 99.99, 3))

        self.add_tt_submit = QPushButton("Add")
        self.add_tt_submit.setStyleSheet(self.bg_color)

        self.di_h_layout = QHBoxLayout()
        self.di_h_layout.addWidget(self.add_tt_dt)
        self.di_h_layout.addWidget(self.add_new_di)

        self.remove_tt_lbl = QLabel("Remove Task Type")
        self.remove_tt_lbl.setStyleSheet("font-weight: bold")
        self.remove_tt_combo = QComboBox()
        for i in range(len(config.task_type_names)):
            self.remove_tt_combo.addItem(f'{config.task_type_names[i]}')
        self.remove_tt_submit = QPushButton("Remove")
        self.remove_tt_submit.setStyleSheet(self.bg_color)

        self.main_layout.addWidget(self.display_tt_lbl)
        self.main_layout.addWidget(self.display_tt_table)
        self.main_layout.addLayout(self.tt_h_layout)

        self.main_layout.addWidget(self.add_tt_lbl)
        self.main_layout.addWidget(self.add_tt_name_lbl)
        self.main_layout.addWidget(self.add_tt_name)
        self.main_layout.addWidget(self.add_tt_dt_lbl)
        self.main_layout.addLayout(self.di_h_layout)
        self.main_layout.addWidget(self.add_tt_ds_lbl)
        self.main_layout.addWidget(self.add_tt_ds)
        self.main_layout.addWidget(self.add_tt_urgency_lbl)
        self.main_layout.addWidget(self.add_tt_urgency)
        self.main_layout.addWidget(self.add_tt_deadline_lbl)
        self.main_layout.addWidget(self.add_tt_deadline)
        self.main_layout.addWidget(self.add_tt_submit)

        self.main_layout.addWidget(self.remove_tt_lbl)
        self.main_layout.addWidget(self.remove_tt_combo)
        self.main_layout.addWidget(self.remove_tt_submit)

        self.main = QWidget()
        self.main.setLayout(self.main_layout)
        return self.main

    def mt_ui(self):
        self.main_layout = QVBoxLayout()

        self.display_mt_lbl = QLabel("Existing Machine Types")     #------------make sure to change this upon adding or removing mts
        self.display_mt_lbl.setStyleSheet('font-weight: bold')
        self.display_mt_table = QTableWidget()
        self.display_mt_table.setColumnCount(4)
        self.display_mt_table.setRowCount(len(config.machine_types))          #------------make sure to change this upon adding or removing tts
        self.display_mt_table.setHorizontalHeaderLabels(["Name","Power","Idle Power","# Replicas"])
        for i in range(len(config.machine_types)):
            self.display_mt_table.setItem(i,0,QTableWidgetItem(str(config.machine_types[i].name)))
            self.display_mt_table.setItem(i,1,QTableWidgetItem(str(config.machine_types[i].power)))
            self.display_mt_table.setItem(i,2,QTableWidgetItem(str(config.machine_types[i].idle_power)))
            self.display_mt_table.setItem(i,3,QTableWidgetItem(str(config.machine_types[i].replicas)))
        self.display_mt_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        header = self.display_mt_table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        self.display_mt_table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)

        self.mt_h_layout = QHBoxLayout()
        self.edit_mt_table = QPushButton("Edit Table Values")
        self.edit_mt_table.setStyleSheet(self.bg_color)
        self.edit_mt_submit = QPushButton("Submit Edit Changes")
        self.edit_mt_submit.setStyleSheet(self.bg_color)
        # self.mt_h_layout.addWidget(self.edit_mt_table)
        self.mt_h_layout.addWidget(self.edit_mt_submit)

        self.add_mt_lbl = QLabel("Add Machine Type")
        self.add_mt_lbl.setStyleSheet("font-weight: bold")
        self.add_mt_name_lbl = QLabel("Machine Name")
        self.add_mt_name = QLineEdit()
        self.add_mt_power_lbl = QLabel("Power")
        self.add_mt_power = QLineEdit()

        self.add_mt_power.setValidator(QDoubleValidator(0.99, 99.99, 3))

        self.add_mt_idle_lbl = QLabel("Idle Power")
        self.add_mt_idle = QLineEdit()

        self.add_mt_idle.setValidator(QDoubleValidator(0.99, 99.99, 3))

        self.add_mt_replicas_lbl = QLabel("# Replicas")
        self.add_mt_replicas = QLineEdit()

        self.onlyInt = QIntValidator(0,999999)
        self.onlyIntNoZero = QIntValidator(1,999999)
        self.add_mt_replicas.setValidator(self.onlyInt)

        self.add_mt_submit = QPushButton("Add")
        self.add_mt_submit.setStyleSheet(self.bg_color)
        
        self.remove_mt_lbl = QLabel("Remove Machine Type")
        self.remove_mt_lbl.setStyleSheet("font-weight: bold")
        self.remove_mt_combo = QComboBox()
        for i in range(len(config.machine_types)):
            self.remove_mt_combo.addItem(f'{config.machine_type_names[i]}')
        self.remove_mt_submit = QPushButton("Remove")
        self.remove_mt_submit.setStyleSheet(self.bg_color)

        self.main_layout.addWidget(self.display_mt_lbl)
        self.main_layout.addWidget(self.display_mt_table)
        self.main_layout.addLayout(self.mt_h_layout)

        self.main_layout.addWidget(self.add_mt_lbl)
        self.main_layout.addWidget(self.add_mt_name_lbl)
        self.main_layout.addWidget(self.add_mt_name)
        self.main_layout.addWidget(self.add_mt_power_lbl)
        self.main_layout.addWidget(self.add_mt_power)
        self.main_layout.addWidget(self.add_mt_idle_lbl)
        self.main_layout.addWidget(self.add_mt_idle)
        self.main_layout.addWidget(self.add_mt_replicas_lbl)
        self.main_layout.addWidget(self.add_mt_replicas)
        self.main_layout.addWidget(self.add_mt_submit)
        
        self.main_layout.addWidget(self.remove_mt_lbl)
        self.main_layout.addWidget(self.remove_mt_combo)
        self.main_layout.addWidget(self.remove_mt_submit)
        
        self.main = QWidget()
        self.main.setLayout(self.main_layout)
        return self.main
        
    def scen_ui(self):              
        self.main_layout = QVBoxLayout()

        self.display_scen_lbl = QLabel("Current Scenario")
        self.display_scen_lbl.setStyleSheet('font-weight: bold')
        self.display_scen_table = QTableWidget()                    
        self.display_scen_table.setColumnCount(5)
        self.display_scen_table.setHorizontalHeaderLabels(["Task Type","# Tasks","Start Time",
                                                    "End Time","Distribution"])
        self.display_scen_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        header = self.display_scen_table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)

        self.scen_h_layout = QHBoxLayout()
        self.scen_h_layout2 = QHBoxLayout()

        self.add_scen_lbl = QLabel("Add Scenario")
        self.add_scen_lbl.setStyleSheet('font-weight: bold')
        self.add_scen_tt_lbl = QLabel("Task Type")
        self.add_scen_tt = QComboBox()
        for i in range(len(config.task_types)):
            self.add_scen_tt.addItem(f'{config.task_type_names[i]}')
        self.add_scen_num_tasks_lbl = QLabel("# Tasks")
        self.add_scen_num_tasks = QLineEdit()

        self.scen_h_layout.addWidget(self.add_scen_tt_lbl,2)
        self.scen_h_layout.addWidget(self.add_scen_num_tasks_lbl,1)
        self.scen_h_layout2.addWidget(self.add_scen_tt,2)
        self.scen_h_layout2.addWidget(self.add_scen_num_tasks,1)

        self.add_scen_num_tasks.setValidator(self.onlyIntNoZero)

        self.scen_h_layout3 = QHBoxLayout()
        self.scen_h_layout4 = QHBoxLayout()

        self.add_scen_start_time_lbl = QLabel("Start Time")
        self.add_scen_start_time = QLineEdit()

        self.add_scen_start_time.setValidator(QDoubleValidator(0.99, 99.99, 3))

        self.add_scen_end_time_lbl = QLabel("End Time")
        self.add_scen_end_time = QLineEdit()

        self.add_scen_end_time.setValidator(QDoubleValidator(0.99, 99.99, 3))

        self.add_scen_dist_lbl = QLabel("Distribution")
        self.add_scen_dist = QComboBox()
        self.add_scen_dist.addItem("Normal")
        self.add_scen_dist.addItem("Uniform")
        self.add_scen_dist.addItem("Exponential")
        self.add_scen_dist.addItem("Spiky")
        self.add_scen_submit = QPushButton("Add")
        self.add_scen_submit.setStyleSheet(self.bg_color)
        self.save_scen_lbl = QLabel("Save Scenario File")
        self.save_scen_lbl.setStyleSheet("font-weight: bold")
        self.save_scen = QPushButton("Save as csv")
        self.save_scen.setStyleSheet(self.bg_color)

        self.scen_h_layout3.addWidget(self.add_scen_start_time_lbl,1)
        self.scen_h_layout3.addWidget(self.add_scen_end_time_lbl,1)
        self.scen_h_layout3.addWidget(self.add_scen_dist_lbl,1)

        self.scen_h_layout4.addWidget(self.add_scen_start_time,1)
        self.scen_h_layout4.addWidget(self.add_scen_end_time,1)
        self.scen_h_layout4.addWidget(self.add_scen_dist,1)

        self.reset_scen_lbl = QLabel("Reset Scenario")
        self.reset_scen_lbl.setStyleSheet('font-weight: bold')
        self.reset_scen_btn = QPushButton("Reset Scenario")
        self.reset_scen_btn.setStyleSheet(self.bg_color)

        self.generate_wkld_lbl = QLabel("Generate Workload Using Current Scenario")
        self.generate_wkld_lbl.setStyleSheet('font-weight: bold')
        self.generate_wkld_submit = QPushButton("Generate Workload")
        self.generate_wkld_submit.setStyleSheet(self.bg_color)

        self.scen_h_layout5 = QHBoxLayout()
        self.scen_h_layout5.addWidget(self.reset_scen_btn)
        self.scen_h_layout5.addWidget(self.generate_wkld_submit)
        self.scen_h_layout5.addWidget(self.save_scen)

        spacer = QSpacerItem(20, 20)

        self.main_layout.addWidget(self.display_scen_lbl)
        self.main_layout.addWidget(self.display_scen_table)
        self.main_layout.addWidget(self.add_scen_lbl)
        self.main_layout.addLayout(self.scen_h_layout)
        self.main_layout.addLayout(self.scen_h_layout2)
        self.main_layout.addSpacerItem(spacer)
        # self.main_layout.addWidget(self.add_scen_tt_lbl)
        # self.main_layout.addWidget(self.add_scen_tt)
        # self.main_layout.addWidget(self.add_scen_num_tasks_lbl)
        # self.main_layout.addWidget(self.add_scen_num_tasks)
        # self.main_layout.addWidget(self.add_scen_start_time_lbl)
        # self.main_layout.addWidget(self.add_scen_start_time)
        # self.main_layout.addWidget(self.add_scen_end_time_lbl)
        # self.main_layout.addWidget(self.add_scen_end_time)
        # self.main_layout.addWidget(self.add_scen_dist_lbl)
        # self.main_layout.addWidget(self.add_scen_dist)
        self.main_layout.addLayout(self.scen_h_layout3)
        self.main_layout.addLayout(self.scen_h_layout4)
        self.main_layout.addSpacerItem(spacer)
        self.main_layout.addWidget(self.add_scen_submit)
        self.main_layout.addSpacerItem(spacer)
        self.main_layout.addLayout(self.scen_h_layout5)
        # self.main_layout.addWidget(self.reset_scen_lbl)
        # self.main_layout.addWidget(self.reset_scen_btn)
        # self.main_layout.addWidget(self.generate_wkld_lbl)
        # self.main_layout.addWidget(self.generate_wkld_submit)
        # self.main_layout.addWidget(self.save_scen_lbl)
        # self.main_layout.addWidget(self.save_scen)

        self.main = QWidget()
        self.main.setLayout(self.main_layout)
        return self.main

    def wkld_ui(self):
        self.main_layout = QVBoxLayout()

        self.wkld_lbl = QLabel("Workload")
        self.wkld_lbl.setStyleSheet('font-weight: bold')
        self.wkld_table = QTableWidget()
        self.wkld_table.setColumnCount(4)
        self.wkld_table.setHorizontalHeaderLabels(["Task Type","Data Size (KB)","Arrival Time","Deadline"])
        header = self.wkld_table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        self.wkld_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.save_wkld_lbl = QLabel("Save Workload File")
        self.save_wkld_lbl.setStyleSheet('font-weight: bold')
        self.save_wkld = QPushButton("Save as CSV File")
        self.save_wkld.setStyleSheet(self.bg_color)
                                                          #------------rows will only be set upon pressing submit for scenarios

        self.main_layout.addWidget(self.wkld_lbl)
        self.main_layout.addWidget(self.wkld_table)
        self.main_layout.addWidget(self.save_wkld_lbl)
        self.main_layout.addWidget(self.save_wkld)

        self.main = QWidget()
        self.main.setLayout(self.main_layout)
        return self.main
    
    def eet_ui(self):                                        #-----------make sure to remove or add rows/columns when adding/removing tts or mts
        self.main_layout = QVBoxLayout()

        self.eet_lbl = QLabel("Expected Execution Times")
        self.eet_lbl.setStyleSheet('font-weight: bold')
        self.eet_table = QTableWidget()
        self.eet_table.setColumnCount(len(config.machine_types))       
        self.eet_table.setRowCount(len(config.task_types))
        header = self.eet_table.horizontalHeader()
        for i in range(len(config.machine_types)):   
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        self.eet_table.setHorizontalHeaderLabels(config.machine_type_names)
        self.eet_table.setVerticalHeaderLabels(config.task_type_names)
        self.eet_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.eet_table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)

        for i in range(self.eet_table.rowCount()):
            for j in range(self.eet_table.columnCount()):
                self.eet_table.setItem(i,j, QTableWidgetItem("0"))

        self.eet_table.cellChanged.connect(self.validate_cell)

        self.horizontal_layout = QHBoxLayout()
        self.eet_table_edit = QPushButton("Edit EET")
        self.eet_table_edit.setStyleSheet(self.bg_color)
        self.eet_table_submit = QPushButton("Submit EET")
        self.eet_table_submit.setStyleSheet(self.bg_color)
        self.eet_table_reset = QPushButton("Reset")
        self.eet_table_reset.setStyleSheet(self.bg_color)
        # self.horizontal_layout.addWidget(self.eet_table_edit)
        self.horizontal_layout.addWidget(self.eet_table_submit)
        self.horizontal_layout.addWidget(self.eet_table_reset)

        self.save_eet_lbl = QLabel("Save EET File")
        self.save_eet_lbl.setStyleSheet('font-weight: bold')
        self.save_eet = QPushButton("Save as CSV File")
        self.save_eet.setStyleSheet(self.bg_color)

        self.close_window_lbl = QLabel("Close Workload Generator")
        self.close_window_lbl.setStyleSheet('font-weight: bold')
        self.close_window = QPushButton("Close")
        self.close_window.setStyleSheet(self.bg_color)
            
        self.main_layout.addWidget(self.eet_lbl)
        self.main_layout.addWidget(self.eet_table)
        self.main_layout.addLayout(self.horizontal_layout)
        self.main_layout.addWidget(self.save_eet_lbl)
        self.main_layout.addWidget(self.save_eet)
        self.main_layout.addWidget(self.close_window_lbl)
        self.main_layout.addWidget(self.close_window)

        self.main = QWidget()
        self.main.setLayout(self.main_layout)
        return self.main
    
    def validate_cell(self, row, column):
        item = self.eet_table.item(row, column)
        if item is None:
            return
        value = item.text()
        
        try:
            value = float(value)
            if value < 0 or round(value, 3) != value:
                raise ValueError()
        except ValueError:
            item.setText('0')
            QMessageBox.warning(self, 'Invalid Value', f'Please enter a non-negative number with up to 3 decimal places in cell ({row+1}, {column+1}).')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WorkloadGenerator()
    ex.show()
    sys.exit(app.exec_())