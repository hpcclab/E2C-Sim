import sys, time, csv
from wsgiref.util import is_hop_by_hop
from gui.reports import FullReport, MachineReport, TaskReport, SummaryReport
from gui.help import HelpMenu
from utils.db_workload import *
from utils.utilities import *
from utils.initTables import *
from utils.initTables import initTables
from utils.machine_type import MachineType
from utils.machine import Machine
from utils.task_type import TaskType, UrgencyLevel
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
from gui.workload_gen import WorkloadGenerator
import utils.config as config
from utils.task import Task
from utils.event_queue import EventQueue
from gui.gen_downloader import Downloader
import pandas as pd
import random
import sqlite3 as sq
import json

class SimUi(QMainWindow):

    def __init__(self,w,h,path_to_arrivals, path_to_etc, path_to_reports):
        super().__init__()
        self.path_to_arrivals = path_to_arrivals
        self.path_to_etc= path_to_etc
        self.path_to_reports = path_to_reports

        db_path = './utils/e2cDB.db'
        self.conn = sq.connect(db_path)
        self.cur = self.conn.cursor()

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
        self.db_scens = []
        self.db_scen = []

        self.etc_submitted = False

        menu = self.menuBar()
        self.report_menu = menu.addMenu("Reports")
        self.help_menu = menu.addMenu("Help")

        self.workload_gen_window = WorkloadGenerator()
        self.workload_gen_window.add_scen_submit.clicked.connect(self.add_scen)
        self.workload_gen_window.reset_scen_btn.clicked.connect(self.reset_scen)
        self.workload_gen_window.generate_wkld_submit.clicked.connect(self.generate_workload)
        self.workload_gen_window.eet_table_reset.clicked.connect(self.eet_table_reset)
        self.workload_gen_window.eet_table_submit.clicked.connect(self.set_etc_generator)
        self.workload_gen_window.add_tt_submit.clicked.connect(self.add_tt)
        self.workload_gen_window.remove_tt_submit.clicked.connect(self.remove_tt)
        self.workload_gen_window.add_mt_submit.clicked.connect(self.add_mt)
        self.workload_gen_window.remove_mt_submit.clicked.connect(self.remove_mt)
        self.workload_gen_window.edit_tt_submit.clicked.connect(self.edit_tt_submit)
        self.workload_gen_window.edit_mt_submit.clicked.connect(self.edit_mt_submit)
        self.workload_gen_window.save_eet.clicked.connect(self.save_eet_file)
        self.workload_gen_window.save_wkld.clicked.connect(self.save_wkld_file)
        self.workload_gen_window.save_scen.clicked.connect(self.save_scen_file)
        self.workload_gen_window.add_new_di.clicked.connect(self.add_di)
        self.workload_gen_window.close_window.clicked.connect(self.close_window)
        self.workload_gen_window.save_config.clicked.connect(self.save_config)

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

    def closeEvent(self, event):
        for window in QApplication.topLevelWidgets():
            window.close()

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

        self.gv.machine_colors = []

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
            pass

        # elif item.data(0) == 'machine_queues_frame':
        #     self.dock_right.set_mq()
        #     self.dock_right.mq_size.returnPressed.connect(self.set_mq_size)

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
                # self.dock_right.mq_size.returnPressed.connect(self.set_mq_size)
                self.dock_right.mq_size_gen.clicked.connect(self.set_mq_size)

        elif item.data(0) == 'workload':
            tt = config.task_type_names
            mt = config.machine_type_names
            self.etc_submitted = False
            self.dock_right.workload_data(0,tt, mt, config.task_types)
            self.dock_right.path_entry.textChanged.connect(self.set_arrival_path)
            self.dock_right.workload_generator.clicked.connect(self.workload_gen_show)
            self.dock_right.dock_wkl_submit.clicked.connect(self.dock_right_set_etc)


            try:
                self.simulator
                self.dock_right.etc_load.setEnabled(False)
                self.dock_right.etc_edit.setEnabled(False)
                self.dock_right.load_wl_btn.setEnabled(False)
                self.dock_right.etc_matrix.setEditTriggers(QAbstractItemView.NoEditTriggers)
            except:
                pass

        self.gv.scene.update()

    def workload_gen_show(self):
        self.workload_gen_window.show()


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


    def set_etc_generator(self):
        self.set_etc()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("EET has been successfully submitted.")
        msg.setWindowTitle("EET Submitted")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


    def dock_right_set_etc(self):
        self.workload_gen_window.eet_table.setRowCount(self.dock_right.etc_matrix.rowCount())
        self.workload_gen_window.eet_table.setColumnCount(self.dock_right.etc_matrix.columnCount())
        for i in range(self.dock_right.etc_matrix.rowCount()):
            for j in range(self.dock_right.etc_matrix.columnCount()):
                item = self.dock_right.etc_matrix.item(i, j)
                self.workload_gen_window.eet_table.setItem(i, j, item.clone())

        for i in range(self.dock_right.etc_matrix.columnCount()):
            header_item = self.dock_right.etc_matrix.horizontalHeaderItem(i)
            self.workload_gen_window.eet_table.setHorizontalHeaderItem(i, header_item.clone())

        for i in range(self.dock_right.etc_matrix.rowCount()):
            header_item = self.dock_right.etc_matrix.verticalHeaderItem(i)
            self.workload_gen_window.eet_table.setVerticalHeaderItem(i, header_item.clone())


        initTables(self.cur,self.conn)
        self.cur.execute("DELETE FROM workload;")
        self.arrivals = pd.DataFrame(columns=["task_type","arrival_time"])


        for row in range(self.dock_right.workload_table.rowCount()):
            self.arrivals.loc[len(self.arrivals.index)] =[(self.dock_right.workload_table.item(row,0).text()),
                                                          float(self.dock_right.workload_table.item(row,2).text())]

        self.arrivals.to_sql("workload",self.conn,if_exists="replace",index=False)
        self.conn.commit()

        self.rewrite_gen_window(self.arrivals)

        not_matched = self.set_etc()       #optionally, catch if tt/mts in eet dont match in config instead of auto changing them in set_etc
        if not_matched: return

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("EET and Workload have been successfully submitted.")
        msg.setWindowTitle("EET and Workload Submitted")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.workload_gen_window.workload_btn.setEnabled(True)
        self.workload_gen_window.workload_btn.setStyleSheet('''color:rgb(0,0,0)''')

    def set_arrival_path(self):
        print(f'wlPath: {self.dock_right.workload_path}')
        print(f'txt_entry: {self.dock_right.path_entry.text()}')
        self.path_to_arrivals = self.dock_right.path_entry.text()

    def close_window(self):
        if self.workload_gen_window.wkld_table.rowCount() == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Workload is empty. Are you sure you wish to close?")
            msg.setWindowTitle("Close Window")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            input = msg.exec_()

            if input == QMessageBox.Ok:
                self.workload_gen_window.close()

        else: self.workload_gen_window.close()

    def save_config(self):
        machine_table = self.workload_gen_window.display_mt_table
        task_table = self.workload_gen_window.display_tt_table
        # Retrieving table rows
        machines = []
        tasks = []
        for row in range(machine_table.rowCount()):
            current_row = []
            for column in range(machine_table.columnCount()):
                if column == 3:
                    item = int(machine_table.item(row, column).text())
                elif column in [1,2]:
                    item = float(machine_table.item(row, column).text())
                else:
                    item = machine_table.item(row, column).text()

                current_row.append(item if item else '')
            print(f'machine {row}: {current_row}')
            machines.append(current_row)

        for row in range(task_table.rowCount()):
            current_row = []
            for column in range(task_table.columnCount()):
                if column ==0:
                    item = int(task_table.item(row, column).text())
                elif column in [3,5]:
                    item = float(task_table.item(row, column).text())
                else:
                    item = task_table.item(row, column).text()
                current_row.append(item if item else '')
            print(f'task {row}: {current_row}')
            tasks.append(current_row)
        config_data = config.load_config()
        config_data['machines'] = []
        config_data['task_types'] = []

        for machine in machines:
            config_data['machines'].append({'name': machine[0],
                                            'power': machine[1],
                                            'idle_power': machine[2],
                                            'replicas': machine[3]})
        for task in tasks:
            config_data['task_types'].append({'id': task[0],
                                        'name': task[1],
                                        'urgency': task[4],
                                        'deadline': task[-1]})
        path  = QFileDialog.getSaveFileName(self, caption='Save Config File',
                                                    directory=QDir.currentPath(),
                                                    filter='*.json')
        if path[0]:
            with open(f'{path[0]}.json', 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=4)

    def set_mq_size(self):
        mq_size = float('inf')
        if self.dock_right.rb_batch.isChecked():
            mq_size = int(self.dock_right.mq_size.text())

        config.machine_queue_size = mq_size
        for machine in config.machines:
            machine.queue_size = config.machine_queue_size
            machine.recreate_queue()
        if mq_size >5 :
            mq_size = 5
        self.gv.machine_queues.max_qsize = mq_size
        # self.dock_right.mq_size.setReadOnly(True)
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


    def save_eet_file(self):
        eet_df = pd.DataFrame(columns=['task_type'])
        eet = self.workload_gen_window.eet_table
        data = []

        for col in range(eet.columnCount()):
            eet_df[f'{eet.horizontalHeaderItem(col).text()}'] = None

        for row in range(eet.rowCount()):
            data.append(eet.verticalHeaderItem(row).text())
            for col in range(eet.columnCount()):
                data.append(eet.item(row,col).text())
            eet_df.loc[len(eet_df)] = data
            data.clear()

        self.dialog = Downloader(eet_df, "EET")
        print(eet_df)

    def save_wkld_file(self):
        wkld_df = pd.DataFrame(columns=['task_type','data_size','arrival_time','deadline'])
        wkld = self.workload_gen_window.wkld_table
        data = []

        for row in range(wkld.rowCount()):
            for col in range(wkld.columnCount()):
                data.append(wkld.item(row,col).text())
            wkld_df.loc[len(wkld_df)] = data
            data.clear()

        self.dialog = Downloader(wkld_df, "Workload")
        print(wkld_df)

    def save_scen_file(self):
        scen_df = pd.DataFrame(columns=['task_type','num_of_tasks','start_time','end_time','distribution'])
        scen = self.workload_gen_window.display_scen_table
        data = []

        for row in range(scen.rowCount()):
            for col in range(scen.columnCount()):
                data.append(scen.item(row,col).text())
            scen_df.loc[len(scen_df)] = data
            data.clear()

        self.dialog = Downloader(scen_df, "Scenario")
        print(scen_df)

    def add_di(self):
        popup = QInputDialog(self, flags=Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        popup.setInputMode(QInputDialog.TextInput)
        popup.setWindowTitle('Add New Data Type')
        popup.setLabelText('Enter Data Type')
        ok = popup.exec_()

        if ok:
            self.workload_gen_window.add_tt_dt.addItem(popup.textValue())

    def edit_tt_submit(self):
        table = self.workload_gen_window.display_tt_table

        for row in range(table.rowCount()):
            id = int(table.item(row,0).text())
            name = table.item(row,1).text()
            data_input = table.item(row,2).text()
            data_size = float(table.item(row,3).text())
            urgency = table.item(row,4).text()
            deadline = float(table.item(row,5).text())

            for tt in config.task_types:
                if tt.id == id:
                    for item in range(self.workload_gen_window.remove_tt_combo.count()):
                        if tt.name == self.workload_gen_window.remove_tt_combo.itemText(item):
                            self.workload_gen_window.remove_tt_combo.setItemText(item,name)
                            self.workload_gen_window.add_scen_tt.setItemText(item,name)

                    for header in range(self.workload_gen_window.eet_table.rowCount()):
                        if tt.name == self.workload_gen_window.eet_table.verticalHeaderItem(header).text():
                            self.workload_gen_window.eet_table.setVerticalHeaderItem(header, QTableWidgetItem(name))

                    config.task_type_names[config.task_type_names.index(tt.name)] = name

                    tt.name = name
                    if urgency == "BestEffort":
                        tt.urgency = UrgencyLevel.BESTEFFORT
                    elif urgency == "Urgent":
                        tt.urgency = UrgencyLevel.URGENT
                    tt.deadline = deadline

        # self.workload_gen_window.display_tt_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Task Type table successfully updated.")
        msg.setWindowTitle("Task Types")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def edit_mt_submit(self):
        table = self.workload_gen_window.display_mt_table

        for row in range(table.rowCount()):
            name = table.item(row,0).text()
            power = float(table.item(row,1).text())
            idle = float(table.item(row,2).text())
            replicas = int(table.item(row,3).text())
            mt = config.machine_types

            for item in range(self.workload_gen_window.remove_mt_combo.count()):
                if mt[row].name == self.workload_gen_window.remove_mt_combo.itemText(item):
                    self.workload_gen_window.remove_mt_combo.setItemText(item,name)

            for header in range(self.workload_gen_window.eet_table.columnCount()):
                if mt[row].name == self.workload_gen_window.eet_table.horizontalHeaderItem(header).text():
                    self.workload_gen_window.eet_table.setHorizontalHeaderItem(header, QTableWidgetItem(name))

            config.machine_type_names[config.machine_type_names.index(mt[row].name)] = name

            mt[row].name = name
            mt[row].power = power
            mt[row].idle_power = idle
            mt[row].replicas = replicas

        # self.workload_gen_window.display_mt_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Machine Type table successfully updated.")
        msg.setWindowTitle("Machine Types")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def eet_table_reset(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Are you sure you want to reset EET?")
        msg.setWindowTitle("Confirm Reset EET")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        input = msg.exec_()

        if input == QMessageBox.Cancel:
            return
        # self.workload_gen_window.eet_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        for i in range(self.workload_gen_window.eet_table.rowCount()):
            for j in range(self.workload_gen_window.eet_table.columnCount()):
                self.workload_gen_window.eet_table.setItem(i,j, QTableWidgetItem("0"))


    def is_empty(self, val):
        if val.strip() == '':
            return True
        return False


    def add_tt(self):
        tt_name = self.workload_gen_window.add_tt_name.text()
        tt_dt = self.workload_gen_window.add_tt_dt.currentText()
        tt_ds = self.workload_gen_window.add_tt_ds.text()
        tt_urgency = self.workload_gen_window.add_tt_urgency.currentText()
        tt_deadline = self.workload_gen_window.add_tt_deadline.text()

        if (self.is_empty(tt_name) or self.is_empty(tt_dt) or self.is_empty(tt_ds)
            or self.is_empty(tt_urgency) or self.is_empty(tt_deadline)):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Please fill out all fields when adding a task type.")
                msg.setWindowTitle("Incomplete Task Type")
                msg.setStandardButtons(QMessageBox.Ok)
                input = msg.exec_()

                return


        tt_ds = float(tt_ds)
        tt_deadline = float(tt_deadline)

        tt_id = self.workload_gen_window.display_tt_table.rowCount() + 1

        # if tt_urgency == "BestEffort":
        #     urgency = UrgencyLevel.BESTEFFORT
        # elif tt_urgency == "Urgent":
        #     urgency = UrgencyLevel.URGENT

        # config.task_types.append(TaskType(tt_id,tt_name,urgency,tt_deadline))
        # config.task_type_names.append(tt_name)

        row_count = self.workload_gen_window.display_tt_table.rowCount()
        self.workload_gen_window.display_tt_table.insertRow(row_count)

        id = QTableWidgetItem(str(tt_id))
        id.setFlags(id.flags() ^ Qt.ItemIsEditable)
        self.workload_gen_window.display_tt_table.setItem(row_count,0,id)
        self.workload_gen_window.display_tt_table.setItem(row_count,1,QTableWidgetItem(tt_name))
        self.workload_gen_window.display_tt_table.setItem(row_count,2,QTableWidgetItem(tt_dt))
        self.workload_gen_window.display_tt_table.setItem(row_count,3,QTableWidgetItem(str(tt_ds)))
        self.workload_gen_window.display_tt_table.setItem(row_count,4,QTableWidgetItem(tt_urgency))
        self.workload_gen_window.display_tt_table.setItem(row_count,5,QTableWidgetItem(str(tt_deadline)))

        self.workload_gen_window.remove_tt_combo.addItem(tt_name)

        #add to eet
        row_count = self.workload_gen_window.eet_table.rowCount()
        self.workload_gen_window.eet_table.insertRow(row_count)
        self.workload_gen_window.eet_table.setVerticalHeaderItem(row_count,QTableWidgetItem(tt_name))
        for i in range(self.workload_gen_window.eet_table.columnCount()):
            self.workload_gen_window.eet_table.setItem(row_count,i,QTableWidgetItem("0"))

        #add to scen combobox
        self.workload_gen_window.add_scen_tt.addItem(tt_name)

    def remove_tt(self):
        if self.workload_gen_window.remove_tt_combo.count() == 0:
            return

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Are you sure you want to delete this task type?")
        msg.setWindowTitle("Confirm Remove Task Type")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        input = msg.exec_()

        if input == QMessageBox.Cancel:
            return

        tt_removed = self.workload_gen_window.remove_tt_combo.currentText()
        # for tt in config.task_types:
        #     if tt_removed == tt.name:
        #         for tt_id in config.task_types[config.task_types.index(tt):]:
        #             tt_id.id = tt_id.id - 1
        #         config.task_types.remove(tt)
        # for tt in config.task_type_names:
        #     if tt_removed == tt:
        #         config.task_type_names.remove(tt)

        for row in range(self.workload_gen_window.display_tt_table.rowCount()):
            if self.workload_gen_window.display_tt_table.item(row,1).text() == tt_removed:
                self.workload_gen_window.display_tt_table.removeRow(row)

                for row2 in range(self.workload_gen_window.display_tt_table.rowCount()):
                    self.workload_gen_window.display_tt_table.setItem(row2,0,QTableWidgetItem(str(config.task_types[row2].id)))

                self.workload_gen_window.eet_table.removeRow(row)
                self.workload_gen_window.remove_tt_combo.removeItem(row)
                self.workload_gen_window.add_scen_tt.removeItem(row)
                self.workload_gen_window.remove_tt_combo.setCurrentIndex(0)
                return

    def add_mt(self):
        mt_name = self.workload_gen_window.add_mt_name.text()
        mt_power = self.workload_gen_window.add_mt_power.text()
        mt_idle_power = self.workload_gen_window.add_mt_idle.text()
        mt_replicas = self.workload_gen_window.add_mt_replicas.text()

        if (self.is_empty(mt_name) or self.is_empty(mt_power)
            or self.is_empty(mt_idle_power) or self.is_empty(mt_replicas)):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Please fill out all fields when adding a machine type.")
                msg.setWindowTitle("Incomplete Machine Type")
                msg.setStandardButtons(QMessageBox.Ok)
                input = msg.exec_()

                return

        mt_id = (len(config.machine_types))

        # config.machine_types.append(MachineType(mt_id,mt_name,float(mt_power),
        #                             float(mt_idle_power),int(mt_replicas)))

        # config.machine_type_names.append(mt_name)

        # # config.no_of_machines = config.no_of_machines + int(mt_replicas)
        # config.no_of_machines = config.no_of_machines + 1

        # for r in range(int(mt_replicas)):
        #     config.machines.append(Machine(len(config.machines), r+1, config.machine_types[-1],
        #                                 {'power': float(mt_power), 'idle_power': float(mt_idle_power)}))

        # config.machines.append(Machine(len(config.machines), 1, config.machine_types[-1],
        #                                 {'power': float(mt_power), 'idle_power': float(mt_idle_power)}))

        # self.gv.machine_queues.m_queues[mt_id] = []
        # self.gv.machine_queues.m_runnings[mt_id] = []

        #----------visual tables----------------------
        row_count = self.workload_gen_window.display_mt_table.rowCount()
        self.workload_gen_window.display_mt_table.insertRow(row_count)

        self.workload_gen_window.display_mt_table.setItem(row_count,0,QTableWidgetItem(mt_name))
        self.workload_gen_window.display_mt_table.setItem(row_count,1,QTableWidgetItem(str(mt_power)))
        self.workload_gen_window.display_mt_table.setItem(row_count,2,QTableWidgetItem(str(mt_idle_power)))
        self.workload_gen_window.display_mt_table.setItem(row_count,3,QTableWidgetItem(str(mt_replicas)))

        self.workload_gen_window.remove_mt_combo.addItem(mt_name)

        #add to eet
        col_count = self.workload_gen_window.eet_table.columnCount()
        self.workload_gen_window.eet_table.insertColumn(col_count)
        self.workload_gen_window.eet_table.setHorizontalHeaderItem(col_count,QTableWidgetItem(mt_name))
        header = self.workload_gen_window.eet_table.horizontalHeader()
        header.setSectionResizeMode(self.workload_gen_window.eet_table.columnCount()-1, QHeaderView.Stretch)
        for i in range(self.workload_gen_window.eet_table.rowCount()):
            self.workload_gen_window.eet_table.setItem(i,col_count,QTableWidgetItem("0"))


    def remove_mt(self):
        if self.workload_gen_window.remove_mt_combo.count() == 0:
            return

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Are you sure you want to delete this machine type?")
        msg.setWindowTitle("Confirm Remove Machine Type")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        input = msg.exec_()

        if input == QMessageBox.Cancel:
            return

        mt_removed = self.workload_gen_window.remove_mt_combo.currentText()

        # for mt in config.machine_types:
        #     if mt_removed == mt.name:
        #         for mt_id in config.machine_types[config.machine_types.index(mt):]:
        #             mt_id.id = mt_id.id - 1
        #         # config.no_of_machines = config.no_of_machines - 1
        #         config.machine_types.remove(mt)

        # config.no_of_machines = config.no_of_machines - 1

        # for mt in config.machine_type_names:
        #     if mt_removed == mt:
        #         config.machine_type_names.remove(mt)

        # for m in config.machines:
        #     if mt_removed == m.type.name:
        #         for m_id in config.machines[config.machines.index(m):]:
        #             m_id.id = m_id.id - 1
        #         config.machines.remove(m)

        for row in range(self.workload_gen_window.display_mt_table.rowCount()):
            if self.workload_gen_window.display_mt_table.item(row,0).text() == mt_removed:
                self.workload_gen_window.display_mt_table.removeRow(row)
                self.workload_gen_window.remove_mt_combo.removeItem(row)
                self.workload_gen_window.remove_mt_combo.setCurrentIndex(0)

                for col in range(self.workload_gen_window.eet_table.columnCount()):
                    if self.workload_gen_window.eet_table.horizontalHeaderItem(col).text() == mt_removed:
                        self.workload_gen_window.eet_table.removeColumn(col)
                        return

    def add_scen(self):

        scen_tt = self.workload_gen_window.add_scen_tt.currentText()
        scen_num_tasks = self.workload_gen_window.add_scen_num_tasks.text()
        scen_start = self.workload_gen_window.add_scen_start_time.text()
        scen_end = self.workload_gen_window.add_scen_end_time.text()
        scen_dist = self.workload_gen_window.add_scen_dist.currentText()

        if (self.is_empty(scen_tt) or self.is_empty(scen_num_tasks)
            or self.is_empty(scen_start) or self.is_empty(scen_end) or self.is_empty(scen_dist)):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Please fill out all fields when adding a scenario subset.")
                msg.setWindowTitle("Incomplete Scenario")
                msg.setStandardButtons(QMessageBox.Ok)
                input = msg.exec_()

                return

        self.db_scen = [str(self.workload_gen_window.add_scen_tt.currentText()),
                        int(self.workload_gen_window.add_scen_num_tasks.text()),
                        float(self.workload_gen_window.add_scen_start_time.text()),
                        float(self.workload_gen_window.add_scen_end_time.text()),
                        (self.workload_gen_window.add_scen_dist.currentText())]

        row_count = self.workload_gen_window.display_scen_table.rowCount()
        self.workload_gen_window.display_scen_table.insertRow(row_count)

        self.workload_gen_window.display_scen_table.setItem(row_count,0,QTableWidgetItem(self.db_scen[0]))
        self.workload_gen_window.display_scen_table.setItem(row_count,1,QTableWidgetItem(str(self.db_scen[1])))
        self.workload_gen_window.display_scen_table.setItem(row_count,2,QTableWidgetItem(str(self.db_scen[2])))
        self.workload_gen_window.display_scen_table.setItem(row_count,3,QTableWidgetItem(str(self.db_scen[3])))
        self.workload_gen_window.display_scen_table.setItem(row_count,4,
                                            QTableWidgetItem(self.workload_gen_window.add_scen_dist.currentText()))

        self.db_scens.append(self.db_scen)

    def reset_scen(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Are you sure you want to reset scenario")
        msg.setWindowTitle("Confirm Reset Scenario")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        input = msg.exec_()

        if input == QMessageBox.Cancel:
            return

        self.workload_gen_window.add_scen_tt.setCurrentIndex(0)
        self.workload_gen_window.add_scen_num_tasks.clear()
        self.workload_gen_window.add_scen_start_time.clear()
        self.workload_gen_window.add_scen_end_time.clear()
        self.workload_gen_window.add_scen_dist.setCurrentIndex(0)

        self.workload_gen_window.display_scen_table.setRowCount(0)

        self.db_scens.clear()

    def clear_scen_reset(self):
        self.simulator.reset()

    def set_etc(self):
        etc_matrix = self.workload_gen_window.eet_table
        not_matched_tt = self.check_etc_format()

        if not_matched_tt:
            return not_matched_tt
        mt_etc = []
        for clmn_idx in range(etc_matrix.columnCount()):
                mt_etc.append(etc_matrix.horizontalHeaderItem(clmn_idx).text())
        if len(mt_etc) != len(config.machine_type_names):
            print(mt_etc, config.machine_type_names)
            self.err_msg("Machine Types", f'Profiling table has {len(mt_etc)} while {len(config.machine_type_names)} machine types are defined in config.json')
            return

        self.dock_right.path_to_etc = './task_machine_performance/gui_generated/etc.csv'
        with open(self.dock_right.path_to_etc,'w',newline='') as etc_file:
            etc_writer = csv.writer(etc_file)
            machine_types = []
            for clmn_idx in range(etc_matrix.columnCount()):
                machine_types.append(etc_matrix.horizontalHeaderItem(clmn_idx).text())
            machine_types = ['idx'] + machine_types
            etc_writer.writerow(machine_types)
            task_types= []
            for row_count in range(etc_matrix.rowCount()):
                row = [etc_matrix.item(row_count, column_count).text() for column_count in range(etc_matrix.columnCount())]
                task_type_name = etc_matrix.verticalHeaderItem(row_count).text()
                task_types.append(task_type_name)
                row = [task_type_name] + row
                etc_writer.writerow(row)
        # print("----------------")
        for idx, mt in enumerate(config.machine_types):
            mt.name = machine_types[idx+1]
        for idx, tt in enumerate(config.task_types):
            # print(idx)
            # print(tt)
            tt.name = task_types[idx]

        for machine in config.machines:
                machine.reset_tt_stats()
        self.path_to_etc = f'./task_machine_performance/gui_generated/etc.csv'

        self.gv.machine_queues.machine_colors = self.is_heterogeneous()

        self.dock_right.etc_editable = False
        self.etc_submitted = True

        self.dock_right.get_eet_input()

    def generate_workload(self):
        #make sure scenario isnt empty
        if self.workload_gen_window.display_scen_table.rowCount() <= 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Error: Scenario is empty.")
            msg.setWindowTitle("Workload Generate Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return


        # initTables(self.cur,self.conn)
        # self.cur.execute("DELETE FROM workload;")
        self.arrivals = pd.DataFrame(columns=["task_type","arrival_time"])
        self.arrival_times = []

        for i in (self.db_scens):
            self.db_task_id = i[0]
            self.db_no_tasks = i[1]
            self.db_start_time = i[2]
            self.db_end_time = i[3]
            self.db_dist = 0
            if i[4] == "Normal":
                self.db_dist = 1
            elif i[4] == "Uniform":
                self.db_dist = 2
            elif i[4] == "Exponential":
                self.db_dist = 3
            elif i[4] == "Spiky":
                self.db_dist = 4

            self.arrival_times = fetchArrivals(self.db_start_time, self.db_end_time, self.db_no_tasks, self.db_dist, self.cur)

            for j in range(self.db_no_tasks):
                self.arrivals.loc[len(self.arrivals.index)] = [(self.db_task_id), self.arrival_times[j]]

        # self.arrivals.sort_values("arrival_time",inplace=True)
        # self.arrivals.reset_index(drop=True,inplace=True)
        # self.arrivals.to_sql("workload",self.conn,if_exists="replace",index=False)
        # self.conn.commit()

        # workload = pd.read_sql_query("SELECT * FROM workload", self.conn)
        # self.dock_right.rewrite_from_db(self.arrivals)
        self.rewrite_gen_window(self.arrivals)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("The workload has been successfully generated.")
        msg.setWindowTitle("Workload Generated")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

        self.workload_gen_window.workload_btn.setEnabled(True)
        self.workload_gen_window.workload_btn.setStyleSheet('''color:rgb(0,0,0)''')

    def check_etc_format(self):
        task_types_etc = []

        workload = pd.read_sql_query("SELECT * FROM workload", self.conn)

        try:
            etc_matrix = self.workload_gen_window.eet_table
            for row_count in range(etc_matrix.rowCount()):
                task_type_name = etc_matrix.verticalHeaderItem(row_count).text()
                task_types_etc.append(task_type_name)
                workload = workload.replace(to_replace=f'T{row_count+1}', value = task_type_name)
        except:
            etc_file = pd.read_csv(self.path_to_etc)
            for row_count, row in etc_file.iterrows():
                task_type_name = row[0]
                task_types_etc.append(task_type_name)
                workload = workload.replace(to_replace=f'T{row_count+1}', value = task_type_name)
        task_types_etc_matrix = task_types_etc.copy()
        task_types_wl = workload['task_type'].unique()

        not_matched_tt = [tt for tt in task_types_wl if tt not in task_types_etc]
        # print("----1-----")
        # print([tt for tt in task_types_wl])
        # print("----2-----")
        # print(task_types_etc)
        if not_matched_tt:
            self.cur.execute(f'DELETE FROM workload WHERE task_type = "{not_matched_tt[0]}";')
            self.arrivals.drop(self.arrivals.loc[self.arrivals['task_type']==not_matched_tt[0]].index, inplace=True)
            for i in self.db_scens:
                if i[0] == not_matched_tt[0]:
                    self.db_scens.remove(i)

            err_txt = f"Task type {not_matched_tt} in workload are not found in ETC"
            self.err_msg('Format Error', err_txt)
            return not_matched_tt

        return not_matched_tt

    def rewrite_gen_window(self, arrivals):
        for idx, row in arrivals.iterrows():
            self.workload_gen_window.wkld_table.setRowCount(idx+1)
            type_item = QTableWidgetItem(row["task_type"])
            arrival_item = QTableWidgetItem(str(row["arrival_time"]))
            self.workload_gen_window.wkld_table.setItem(idx, 0, type_item)
            self.workload_gen_window.wkld_table.setItem(idx, 2, arrival_item)

        for tt in range(self.workload_gen_window.display_tt_table.rowCount()):
            if self.workload_gen_window.display_tt_table.item(tt,1).text() in set(arrivals['task_type']):
                count = arrivals['task_type'].value_counts()[f'{self.workload_gen_window.display_tt_table.item(tt,1).text()}']
                data_size = float(self.workload_gen_window.display_tt_table.item(tt,3).text())
                stdv = data_size / 6
                dist = get_data_sizes(data_size,stdv,count)

                i = 0
                for wkl_row in range(self.workload_gen_window.wkld_table.rowCount()):

                    if self.workload_gen_window.wkld_table.item(wkl_row,0).text() == self.workload_gen_window.display_tt_table.item(tt,1).text():
                        self.workload_gen_window.wkld_table.setItem(wkl_row,1,QTableWidgetItem(str(round(dist[i],3))))
                        self.dock_right.workload_table.setItem(wkl_row,1,QTableWidgetItem(str(round(dist[i],3))))

                        #for deadline
                        arr_time = float(self.workload_gen_window.wkld_table.item(wkl_row,2).text())
                        deadline = float(self.workload_gen_window.display_tt_table.item(tt,5).text())
                        real_dl = round((deadline + arr_time),3)
                        self.workload_gen_window.wkld_table.setItem(wkl_row,3,QTableWidgetItem(str(real_dl)))
                        self.dock_right.workload_table.setItem(wkl_row,3,QTableWidgetItem(str(real_dl)))

                        i = i + 1

            else:
                i = 0
                for wkl_row in range(self.workload_gen_window.wkld_table.rowCount()):
                    self.workload_gen_window.wkld_table.setItem(wkl_row,1,QTableWidgetItem(str(5.0)))

                    #for deadline
                    arr_time = float(self.workload_gen_window.wkld_table.item(wkl_row,2).text())
                    deadline = 50.0
                    real_dl = round((deadline + arr_time),3)
                    self.workload_gen_window.wkld_table.setItem(wkl_row,3,QTableWidgetItem(str(real_dl)))

                    i = i + 1



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
        config.scheduling_method = self.policy

    def is_heterogeneous(self):
        colors = []
        m_col = []
        hets = []
        etc_file = pd.read_csv(self.path_to_etc)
        etc_file = etc_file.iloc[:,1:]

        for i in range(len(etc_file.columns)):
            colors.extend([[82,126,191]]) #homogeneous colors

        #make nested list of each machine column (the EETs of each task)
        for i in range(len(etc_file.columns)):
            temp = []
            for j in range(len(etc_file)):
                temp.append(etc_file.at[j,etc_file.columns[i]])
            m_col.append(temp)

        #passes if is heterogeneous
        if m_col.count(m_col[0]) != len(m_col):
            for i in range(len(m_col)):
                for j in range(i + 1, len(m_col)):
                    if(m_col[i] == m_col[j]):
                        hets.append([i,j])

            for i in range(len(m_col)):
                colors[i] = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
            for i in range(len(hets)):
                colors[hets[i][0]] = colors[hets[i][1]]

        return colors




    def setup_config(self, simulator):
        if self.configs['scheduler'] == 'default':
            self.policy = 'FCFS'
        else:
            self.policy = self.configs['scheduler']
        simulator.set_scheduling_method(self.policy)


    def simulate_start(self):
        not_matched_tt = self.check_etc_format()
        if not_matched_tt:
            return
        if not self.etc_submitted:
            if (self.workload_gen_window.wkld_table.rowCount() == 0):
                self.err_msg('EET Submision', 'Must generate a workload and submit EET in the workload generator.')
            else:
                self.err_msg('EET Submision', 'Must submit EET in the workload generator.')
            return
        if self.workload_gen_window.wkld_table.rowCount() == 0:
            self.err_msg('EET Submision', 'Must generate a workload in the workload generator.')
            return

        self.thread = QThread(parent=self)
        self.simulator =  Simulator(self.path_to_arrivals,self.path_to_etc, self.path_to_reports,  seed=123)

        self.setup_config(self.simulator)
        self.simulator.moveToThread(self.thread)
        self.thread.started.connect(self.clear_scen_reset)
        self.thread.started.connect(self.simulator.run)
        self.thread.finished.connect(self.thread.deleteLater)
        self.simulator.simulation_done.connect(self.simulation_done)
        self.simulator.simulation_done.connect(self.simulator.deleteLater)


        self.simulator.event_signal.connect(self.msg_handler)
        self.simulator.scheduler.decision.connect(self.msg_handler)
        #self.simulator.scheduler.decision.connect(self.msg_handler)
        self.simulator.simulation_done.connect(self.thread.quit)
        self.simulator.simulation_done.connect(lambda: self.buttons['reset'].setEnabled(True))
        self.simulator.simulation_done.connect(lambda: self.buttons['simulate'].setEnabled(False))
        self.simulator.simulation_done.connect(lambda: self.buttons['speed'].setEnabled(False))
        self.simulator.simulation_done.connect(lambda: self.buttons['simulate'].setIcon(QIcon(f'./gui/icons/simulate.png')))


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
            self.simulator.simulation_done.connect(lambda: self.dock_right.etc_edit.setEnabled(True))
            self.simulator.simulation_done.connect(lambda: self.dock_right.etc_load.setEnabled(True))
            self.simulator.simulation_done.connect(lambda: self.dock_right.load_wl_btn.setEnabled(True))
        except:
            pass

        try:
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
            self.buttons['reset'].setEnabled(False)
            self.simulator.pause = False
        else:
            self.buttons['simulate'].setIcon(QIcon(f'./gui/icons/simulate.png'))
            self.buttons['increment'].setEnabled(True)
            self.buttons['reset'].setEnabled(True)
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
        self.workload_gen_window.workload_btn.setEnabled(False)
        self.workload_gen_window.workload_btn.setStyleSheet("QPushButton{color:rgb(100,100,100);}")
        self.workload_gen_window.wkld_table.setRowCount(0)
        self.progress=0
        self.p_count = 0
        self.pbar.setFormat(f'{self.p_count}/0 tasks ({self.progress}%)')
        self.pbar.setValue(self.progress)
        self.gv.batch_queue.reset()
        self.gv.machine_queues.reset()
        self.buttons['simulate'].setEnabled(True)
        self.buttons['speed'].setEnabled(False)
        config.event_queue = EventQueue()
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
        self.gv.batch_queue.outer_frame()
        self.gv.batch_queue.inner_frame()
        self.gv.mapper_ui.mapper()
        self.gv.mapper_ui.trash()
        self.gv.workload_ui.draw_frame()
        self.gv.connect_workload(QPen(Qt.red, 4), Qt.red)
        self.gv.connecting_lines()
        self.gv.machine_queues.outer_frame()
        self.gv.machine_queues.draw_queues()
        self.gv.machine_queues.fill_queues()
        self.gv.machine_queues.runnings(config.machines)
        self.gv.machine_queues.trash()

        try:
            self.dock_right.etc_load.setEnabled(True)
            self.dock_right.etc_edit.setEnabled(True)
            self.dock_right.load_wl_btn.setEnabled(True)
            self.dock_right.etc_matrix.setEditTriggers(QAbstractItemView.NoEditTriggers)
        except:
            pass

        self.update()







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
            #print(f'RUNNING@ {m_id}:\n{[t.id for t in self.gv.machine_queues.m_runnings[m_id]]}')

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
            #print(f'RUNNING@ {m_id}:{self.gv.machine_queues.m_runnings[m_id][0].id}\n{task.id}')
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

        # print(self.gv.machine_colors)

        self.gv.batch_queue.draw_tasks(selected_task)
        self.gv.machine_queues.outer_frame()
        self.gv.machine_queues.draw_queues()
        self.gv.machine_queues.fill_queues()
        self.gv.machine_queues.runnings(config.machines)
        self.gv.machine_queues.trash()
        self.update()

    def simulation_done(self):
        self.simulate_pause = True




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
