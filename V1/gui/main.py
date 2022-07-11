import  simUi
from simulator import Simulator

from PyQt5.QtWidgets import QApplication
import sys



def main():
    app = QApplication(sys.argv)   
    view = simUi.SimUi()
    view.show()
    app.exec()
    

main()


