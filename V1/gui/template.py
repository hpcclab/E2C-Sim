import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

class MainWindow(qtw.QWidget):
    
    def __init__(self): 
        
        super().__init__()
        self.setWindowTitle('E2C SIM')

        self.setLayout(qtw.QVBoxLayout())

        my_label = qtw.QLabel("Pick a machine type from the list:")
        my_label.setFont(qtg.QFont('Helvetica', 18))

        self.layout().addWidget(my_label)

        # my_entry = qtw.QLineEdit()
        # my_entry.setObjectName('name_field')
        # my_entry.setText("Placeholder")
        # self.layout().addWidget(my_entry)
        my_combo = qtw.QComboBox(self)
        my_combo.addItem('CPU')
        my_combo.addItem('GPU')
        my_combo.addItem('FPGA')

        self.layout().addWidget(my_combo)

        my_button = qtw.QPushButton("Press Me!",
        clicked = lambda:press_it())
        self.layout().addWidget(my_button)

        def press_it():            
            # my_label.setText(f'Hello {my_entry.text()}')
            # my_entry.setText('')
            my_label.setText(f'You picked {my_combo.currentText()}')
    
        self.show()

    
        


app = qtw.QApplication([])
mw = MainWindow()

app.exec_()