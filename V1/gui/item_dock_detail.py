from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys



class ItemDockDetail(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_dock()
    

    def init_dock(self):   
        self.dock=QDockWidget('Dockable',self)
        self.dock.setFloating(False)        
        self.addDockWidget(Qt.RightDockWidgetArea,self.dock)
    
    def task_in_bq(self, task):
        title = QLabel("Task Information", self)
        self.dock.setTitleBarWidget(title)

        widget = QWidget(self)
        vlayout=QVBoxLayout()

        

        id_lbl = QLabel(f'ID: {task.id}')
        type_lbl = QLabel(f'Type: {task.type.name}')
        arr_lbl = QLabel(f'Arrival Time: {task.arrival_time}')
        start_lbl = QLabel(f'Start Time: {task.start_time}')
        compl_lbl = QLabel(f'Completion Time: {task.completion_time}')
        missed_lbl = QLabel(f'Completion Time: {task.missed_time}')

        ddl_lbl = QLabel(f'Deadline: {task.deadline}')
        dfr_lbl = QLabel(f'Deferred: {task.no_of_deferring}')
        
        eet_list = QListWidget()

        for machine, eet in task.estimated_time.items():
            eet_list.addItem(f'{machine.upper()}: {eet}')

        vlayout.addWidget(id_lbl)
        vlayout.addWidget(type_lbl)
        vlayout.addWidget(arr_lbl)
        vlayout.addWidget(start_lbl)
        vlayout.addWidget(compl_lbl)
        vlayout.addWidget(missed_lbl)
        vlayout.addWidget(ddl_lbl)
        vlayout.addWidget(dfr_lbl)

        vlayout.addWidget(eet_list)
        
        
        widget.setLayout(vlayout)

        self.dock.setWidget(widget)


    def machine_data(self, machine):
        title = QLabel("Machine Information", self)
        self.dock.setTitleBarWidget(title)

        widget = QWidget(self)
        vlayout=QVBoxLayout()

        

        id_lbl = QLabel(f'ID: {machine.id}')
        type_lbl = QLabel(f'Type: {machine.type.name}')
        arr_lbl = QLabel(f'Specs: {machine.specs}')
        
        
        eet_list = QListWidget()

        for title, value in machine.stats.items():
            eet_list.addItem(f'{title.upper()}: {value}')

        vlayout.addWidget(id_lbl)
        vlayout.addWidget(type_lbl)
        vlayout.addWidget(arr_lbl)        

        vlayout.addWidget(eet_list)
        
        
        widget.setLayout(vlayout)

        self.dock.setWidget(widget)
    
    def trash_data(self, cancelled_tasks):
        title = QLabel("Machine Information", self)
        self.dock.setTitleBarWidget(title)
        widget = QWidget(self)
        vlayout=QVBoxLayout()        
        task_list = QListWidget()
        for task in cancelled_tasks:
            task_list.addItem(f'{task.id}')        
        vlayout.addWidget(task_list)
        widget.setLayout(vlayout)
        self.dock.setWidget(widget)


        


        
        
 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ItemDockDetail()
    ex.show()
    sys.exit(app.exec_())
