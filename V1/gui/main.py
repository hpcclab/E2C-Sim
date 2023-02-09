import  gui.simUi as simUi_A
from simulator import Simulator

from PyQt5.QtWidgets import QApplication
import sys



def main():
    app = QApplication(sys.argv)   
    view = simUi_A.SimUi()
    view.show()
    app.exec()
    

main()


