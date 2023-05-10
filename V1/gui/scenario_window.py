from PyQt5.QtCore import Qt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import utils.config as config


class ScenarioWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generate New Workload")
        self.layout = QGridLayout(self)


        #---------------Scenario---------------------------------------------
        self.add_scen_label = QLabel("Define Scenario")
        self.spacer = QLabel("")

        self.db_task_id_label = QLabel("Task ID")
        self.db_task_id = QLineEdit()

        self.db_no_tasks_label = QLabel("# of Tasks")
        self.db_no_tasks = QLineEdit()

        self.db_start_time_label = QLabel("Starting Time")
        self.db_start_time = QLineEdit()

        self.db_end_time_label = QLabel("Ending Time")
        self.db_end_time = QLineEdit()

        self.db_dist_label = QLabel("Distribution")
        self.db_dist = QComboBox()
        self.db_dist.addItem("1. Normal")
        self.db_dist.addItem("2. Uniform")
        self.db_dist.addItem("3. Exponential")
        self.db_dist.addItem("4. Spiky")

        self.db_add_scen = QPushButton("Add Scenario")
        self.db_reset = QPushButton("Reset Scenarios")

        self.layout.addWidget(self.add_scen_label,0,0)
        self.layout.addWidget(self.spacer,1,0)
        self.layout.addWidget(self.db_task_id_label,2,0)
        self.layout.addWidget(self.db_task_id,3,0)
        self.layout.addWidget(self.db_no_tasks_label,4,0)
        self.layout.addWidget(self.db_no_tasks,5,0)
        self.layout.addWidget(self.db_start_time_label,6,0)
        self.layout.addWidget(self.db_start_time,7,0)
        self.layout.addWidget(self.db_end_time_label,8,0)
        self.layout.addWidget(self.db_end_time,9,0)
        self.layout.addWidget(self.db_dist_label,10,0)
        self.layout.addWidget(self.db_dist,11,0)
        self.layout.addWidget(self.db_add_scen,12,0)
        self.layout.addWidget(self.db_reset,13,0)


        #-----------EET---------------------------------------(add option to add or remove machine here)
        self.eet_label = QLabel("EET Table")

        self.eet_table = QTableWidget()
        
        self.eet_table.setRowCount(len(config.task_types))
        self.eet_table.setColumnCount(len(config.machine_types))

        self.eet_machine_labels = [machine for machine in config.machine_type_names]
        self.eet_table.setHorizontalHeaderLabels(self.eet_machine_labels)

        self.eet_task_labels = [task for task in config.task_type_names]
        self.eet_table.setVerticalHeaderLabels(self.eet_task_labels)

        for i in range(self.eet_table.rowCount()):
            for j in range(self.eet_table.columnCount()):
                self.eet_table.setItem(i,j, QTableWidgetItem("0"))

        self.eet_table.setMaximumSize(self.getQTableWidgetSize())
        self.eet_table.setMinimumSize(self.getQTableWidgetSize())

        self.eet_submit = QPushButton("Submit EET and Scenarios")

        self.layout.addWidget(self.eet_label,0,1)
        self.layout.addWidget(self.eet_table,1,1)
        self.layout.addWidget(self.eet_submit,2,1)


        #-----Task Type deadline----------------------------------
        self.tt_deadline_label = QLabel("Task Type Deadlines")
        self.spacer2 = QLabel("")
        self.tt_combo = QComboBox()

        for i in range(len(config.task_type_names)):
            self.tt_combo.addItem(f'{config.task_type_names[i]}')

        self.tt_new_dl_label = QLabel("New Deadline")
        self.tt_deadline = QLineEdit()
        self.tt_dl_submit = QPushButton("Submit")

        self.layout.addWidget(self.tt_deadline_label, 0,2)
        self.layout.addWidget(self.spacer2,1,2)
        self.layout.addWidget(self.tt_combo,2,2)
        self.layout.addWidget(self.tt_new_dl_label,3,2)
        self.layout.addWidget(self.tt_deadline,4,2)
        self.layout.addWidget(self.tt_dl_submit,5,2)


        #-----------------Remove a machine--------------------------------------
        self.remove_machine_label = QLabel("Remove a machine type")
        self.spacer3 = QLabel("")
        self.remove_machine_combo = QComboBox()
        for i in range(len(config.machine_types)):
            self.remove_machine_combo.addItem(f'{config.machine_type_names[i]}')
        self.remove_machine_submit = QPushButton("Remove machine type")

        self.layout.addWidget(self.remove_machine_label,0,3)
        self.layout.addWidget(self.spacer3,1,3)
        self.layout.addWidget(self.remove_machine_combo,2,3)
        self.layout.addWidget(self.remove_machine_submit,3,3)

        #-----------Add a machine----------------------------------------------
        self.add_machine_label = QLabel("Add a machine type")
        self.spacer4 = QLabel("")
        self.add_machine_name_label = QLabel("Name")
        self.add_machine_name = QLineEdit()
        self.add_machine_power_label = QLabel("Power")
        self.add_machine_power = QLineEdit()
        self.add_machine_idle_label = QLabel("Idle")
        self.add_machine_idle = QLineEdit()
        self.add_machine_replicas_label = QLabel("# Replicas")
        self.add_machine_replicas = QLineEdit()
        self.add_machine_submit = QPushButton("Submit machine")

        self.layout.addWidget(self.add_machine_label,0,4)
        self.layout.addWidget(self.spacer4,1,4)
        self.layout.addWidget(self.add_machine_name_label,2,4)
        self.layout.addWidget(self.add_machine_name,3,4)
        self.layout.addWidget(self.add_machine_power_label,4,4)
        self.layout.addWidget(self.add_machine_power,5,4)
        self.layout.addWidget(self.add_machine_idle_label,6,4)
        self.layout.addWidget(self.add_machine_idle,7,4)
        self.layout.addWidget(self.add_machine_replicas_label,8,4)
        self.layout.addWidget(self.add_machine_replicas,9,4)
        self.layout.addWidget(self.add_machine_submit,10,4)


        self.setLayout(self.layout)


    def getQTableWidgetSize(self):
        w = self.eet_table.verticalHeader().width() + 4 
        for i in range(self.eet_table.columnCount()):
            w += self.eet_table.columnWidth(i)  
        h = self.eet_table.horizontalHeader().height() + 4
        for i in range(self.eet_table.rowCount()):
            h += self.eet_table.rowHeight(i)
        return QSize(w, h)