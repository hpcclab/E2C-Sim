import pandas as pd
import os, glob, pathlib
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import utils.config as config

from gui.downloader import Downloader

def fetchReport(path_to_reports):
    files = []
    for i, file in enumerate(os.listdir(path_to_reports)):
        if file.startswith('detailed'):
            files.append(path_to_reports + file)
    file = max(files, key=os.path.getctime)
    return file

# ========================================================================= FULL REPORT
class FullReport(QMainWindow):

    def __init__(self, path_to_reports, method):
        #Initialize window
        super().__init__()
        self.setWindowTitle("Full Simulation Report")
        self.setStyleSheet(f"background-color: rgb(217,217,217);")

        # Fetch CSV file
        df = pd.read_csv(fetchReport(path_to_reports + "/" + method + "/"))

        # Reorder columns
        df = df.reindex(columns=[
            'id',
            'type',
            'urgency',
            'status',
            'assigned_machine',
            'arrival_time',
            'start_time',
            'completion_time',
            'missed_time',
            'execution_time',
            'energy_usage',
            'deadline',
            'extended_deadline'
        ])

        # Initialize save action
        save_report = QAction("&Save", self)
        save_report.setToolTip("Save report to CSV file")
        save_report.setIcon(QIcon("./gui/icons/save.png"))
        save_report.triggered.connect(lambda: self.full_report_save(df))
        tb = self.addToolBar("farat")
        tb.addAction(save_report)

        # Initialize widget
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(df.shape[0])
        self.tableWidget.setColumnCount(df.shape[1])
        self.tableWidget.verticalHeader().setVisible(False)

        # Set column headers
        self.tableWidget.setHorizontalHeaderLabels(df.columns)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setStyleSheet("""
            alternate-background-color: lightgray;
            background-color: white;
            selection-background-color:lightblue;
            ;
        """)

        # Format floating points to 3 decimal places
        for col in list(df.select_dtypes(include=['float64']).columns):
            df.loc[:, col] = df[col].map('{:.3f}'.format)

        df = df.replace(to_replace="inf",
           value="N/A")
        # Populate cells with values from CSV
        for r in range(df.shape[0]):
            for c in range(df.shape[1]):
                if not str(df.values[r][c]).isdigit():
                    self.tableWidget.setItem(r, c, QTableWidgetItem(str(df.values[r][c])))
                else:
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, df.values[r][c])
                    self.tableWidget.setItem(r, c, item)

        # Enable sorting
        self.tableWidget.setSortingEnabled(True)


        # Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #A label that indicates the scheduling policy
        scheduling_lbl = QLabel(f'Scheduling Method: {method}')

        # Go live
        self.report_layout = QVBoxLayout(self)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.report_layout)

        self.report_layout.addWidget(scheduling_lbl)
        self.report_layout.addWidget(self.tableWidget)
        self.resize(1200, 800)
        self.show()

    def full_report_save(self, df):
        self.dialog= Downloader(df, "Full")

# ========================================================================= TASK REPORT
class TaskReport(QMainWindow):

    def __init__(self, path_to_reports, method):
        #Initialize window
        super().__init__()
        self.setWindowTitle("Task-based Simulation Report")
        self.setStyleSheet(f"background-color: rgb(217,217,217);")

        # Fetch CSV file
        df = pd.read_csv(fetchReport(path_to_reports + "/" + method + "/"), usecols=[
            'id',
            'type',
            'status',
            'assigned_machine',
            'arrival_time',
            'start_time',
            'completion_time',
            'missed_time'])


        # Initialize save action
        save_report = QAction("&Save", self)
        save_report.setIcon(QIcon("./gui/icons/save.png"))
        save_report.setToolTip("Save report to CSV file")
        save_report.triggered.connect(lambda: self.task_report_save(df))

        # Initialize widget
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(df.shape[0])
        self.tableWidget.setColumnCount(df.shape[1])
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Set column headers
        self.tableWidget.setHorizontalHeaderLabels(df.columns)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setStyleSheet("""
            alternate-background-color: lightgray;
            background-color: white;
            selection-background-color:lightblue;
        """)

        # Format floating points to 3 decimal places
        for col in list(df.select_dtypes(include=['float64']).columns):
            df.loc[:, col] = df[col].map('{:.3f}'.format)

        df = df.replace(to_replace="inf",
           value="N/A")

        # Populate cells with values from CSV
        for r in range(df.shape[0]):
            for c in range(df.shape[1]):
                if not str(df.values[r][c]).isdigit():
                    self.tableWidget.setItem(r, c, QTableWidgetItem(str(df.values[r][c])))
                else:
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, df.values[r][c])
                    self.tableWidget.setItem(r, c, item)

        # Enable sorting
        self.tableWidget.setSortingEnabled(True)

        # Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Add search bar
        self.query = QLineEdit()
        self.query.setPlaceholderText("Search id")
        self.query.textChanged.connect(self.search)
        tb = self.addToolBar("farat")
        tb.addAction(save_report)
        tb.addWidget(self.query)

        #A label that indicates the scheduling policy
        scheduling_lbl = QLabel(f'Scheduling Method: {method}')

        # Go live
        self.report_layout = QVBoxLayout(self)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.report_layout)

        self.report_layout.addWidget(scheduling_lbl)
        self.report_layout.addWidget(self.tableWidget)
        self.resize(1200, 800)
        self.show()

        # # Build layout & Go live
        # self.layout = QVBoxLayout(self)
        # self.setCentralWidget(self.tableWidget)
        # self.setLayout(self.layout)
        # self.resize(1200, 800)
        # self.show()


    def search(self, id):

        # Clear selection
        self.tableWidget.setCurrentItem(None)

        if not id: return

        matches = self.tableWidget.findItems(id, Qt.MatchContains)
        if matches:
            item = matches[0]
            self.tableWidget.setCurrentItem(item)

    def task_report_save(self, df):
        self.dialog= Downloader(df, "Task")

# ========================================================================= MACHINE REPORT
class MachineReport(QMainWindow):

    def __init__(self, path_to_reports, method):

        #Initialize window
        super().__init__()
        self.setWindowTitle("Machine-based Simulation Report")
        self.setStyleSheet(f"background-color: rgb(217,217,217);")

        # Fetch CSV file
        df = pd.read_csv(fetchReport(path_to_reports + "/" + method + "/"))
        #df = MachineReport.makeReport(df).sort_index(ascending=True)
        df = MachineReport.makeReport(df)
        print(f'Machine Report: @{path_to_reports}/{method}/')
        print(df)

        # Initialize save action
        save_report = QAction("&Save", self)
        save_report.setToolTip("Save report to CSV file")
        save_report.setIcon(QIcon("./gui/icons/save.png"))
        save_report.triggered.connect(lambda: self.mach_report_save(df))
        tb = self.addToolBar("farat")
        tb.addAction(save_report)

        # Initialize widget
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(df.shape[0])
        self.tableWidget.setColumnCount(df.shape[1])
        self.tableWidget.verticalHeader().setVisible(False)

        # Set column headers
        self.tableWidget.setHorizontalHeaderLabels(df.columns)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setStyleSheet("""
            alternate-background-color: lightgray;
            background-color: white;
            selection-background-color:lightblue;
        """)

        # Populate cells with values from CSV
        for r in range(df.shape[0]):
            for c in range(df.shape[1]):
                if not str(df.values[r][c]).isdigit():
                    self.tableWidget.setItem(r, c, QTableWidgetItem(str(df.values[r][c])))
                else:
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, df.values[r][c])
                    self.tableWidget.setItem(r, c, item)

        # Enable sorting
        self.tableWidget.setSortingEnabled(True)


        # Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #A label that indicates the scheduling policy
        scheduling_lbl = QLabel(f'Scheduling Method: {method}')

        # Go live
        self.report_layout = QVBoxLayout(self)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.report_layout)

        self.report_layout.addWidget(scheduling_lbl)
        self.report_layout.addWidget(self.tableWidget)
        self.resize(600, 200)
        self.show()

        # # Go live
        # self.layout = QVBoxLayout(self)
        # self.setCentralWidget(self.tableWidget)
        # self.setLayout(self.layout)
        # self.resize(600, 200)
        # self.show()

    def makeReport(df):
        df_machine = pd.DataFrame(
            index=set(df["assigned_machine"]),
            columns=['machine', 'tasks_assigned', 'tasks_completed', 'tasks_missed',
                     'throughput', 'utilization']
        )

        df_machine.sort_index(ascending=True).fillna(0)

        assigned_t, complete_t, missed_t = 0, 0, 0
        throughputs_t, utilizations_t = [], []

        for machine in df_machine.index:
            df_machine.at[machine, 'machine'] = machine

            assigned, complete, missed = 0, 0, 0

            subset = df.loc[df['assigned_machine'].isin([machine])]

            for i in subset.index:
                assigned_t += 1
                assigned += 1
                if(subset.at[i, 'status'] == 'COMPLETED'):
                    complete_t += 1
                    complete += 1
                elif(subset.at[i, 'status'] == 'MISSED'):
                    missed_t += 1
                    missed += 1

            df_machine.at[machine, 'tasks_assigned'] = assigned
            df_machine.at[machine, 'tasks_completed'] = complete
            df_machine.at[machine, 'tasks_missed'] = missed

        for m in config.machines:
            utilization = round(100*m.busy_time / config.time.gct(),2)
            throughput = round((m.stats['completed_tasks'] + m.stats['xcompleted_tasks']) / config.time.gct(),2)
            utilizations_t.append(utilization)
            throughputs_t.append(throughput)
            df_machine.at[f'{m.type.name}-{m.replica_id}', 'throughput'] = throughput
            df_machine.at[f'{m.type.name}-{m.replica_id}', 'utilization'] = utilization

        df_machine.loc['total'] = {
            'machine': 'total',
            'tasks_assigned': assigned_t,
            'tasks_completed': complete_t,
            'tasks_missed': missed_t,
            'throughput': round(sum(throughputs_t), 2),
            'utilization': round(sum(utilizations_t)/ len(utilizations_t),2)
        }


        return df_machine

    def mach_report_save(self, df):
        print(df)
        self.dialog= Downloader(df, "Machine")


# ========================================================================= Summary REPORT
class SummaryReport(QMainWindow):

    def __init__(self, path_to_reports, method):

        #Initialize window
        super().__init__()
        self.setWindowTitle("Summarized Simulation Report")
        self.setStyleSheet(f"background-color: rgb(217,217,217);")

        # Fetch CSV file
        df = pd.read_csv(path_to_reports + "/" + method + "/results-summary.csv")
        for col in list(df.select_dtypes(include=['float64']).columns):
            df.loc[:, col] = df[col].map('{:.3f}'.format)
        print('Summary Report:')
        print(df)

        # Initialize save action
        save_report = QAction("&Save", self)
        save_report.setToolTip("Save report to CSV file")
        save_report.setIcon(QIcon("./gui/icons/save.png"))
        save_report.triggered.connect(lambda: self.summary_report_save(df))
        tb = self.addToolBar("farat")
        tb.addAction(save_report)

        # Initialize widget
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(df.shape[0])
        self.tableWidget.setColumnCount(df.shape[1])
        self.tableWidget.verticalHeader().setVisible(False)

        # Set column headers
        self.tableWidget.setHorizontalHeaderLabels(df.columns)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setStyleSheet("""
            alternate-background-color: lightgray;
            background-color: white;
            selection-background-color:lightblue;
        """)

        # Populate cells with values from CSV
        for r in range(df.shape[0]):
            for c in range(df.shape[1]):
                if not str(df.values[r][c]).isdigit():
                    self.tableWidget.setItem(r, c, QTableWidgetItem(str(df.values[r][c])))
                else:
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, df.values[r][c])
                    self.tableWidget.setItem(r, c, item)

        # Enable sorting
        self.tableWidget.setSortingEnabled(True)


        # Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)



        #A label that indicates the scheduling policy
        scheduling_lbl = QLabel(f'Scheduling Method: {method}')

         # Go live
        self.report_layout = QVBoxLayout(self)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.report_layout)

        self.report_layout.addWidget(scheduling_lbl)
        self.report_layout.addWidget(self.tableWidget)
        self.resize(600, 200)
        self.show()

        # Go live
        # self.layout = QVBoxLayout(self)
        # self.setCentralWidget(self.tableWidget)
        # self.setLayout(self.layout)
        # self.resize(600, 200)
        # self.show()





    def summary_report_save(self, df):
        self.dialog= Downloader(df, "Summary")