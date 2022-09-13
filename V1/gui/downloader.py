import os, urllib.request, datetime
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Downloader(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Save File'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.openFileNameDialog()
        self.openFileNamesDialog()
        self.saveFileDialog()

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

def download(df, type):
    PREFIX = "../../V1/output/data/default/FCFS/"
    FILE = df.to_csv(type + "_Report_" + datetime.now() + ".csv")
    try:
        if os.name == "nt":
            DL_DIR = f"{os.getenv('USERPROFILE')}\\Downloads"
        else:
            DL_DIR = f"{os.getenv('HOME')}/Downloads"

        if not os.path.exists(PREFIX + FILE):
            raise FileNotFoundError

        urllib.request.urlretrieve(PREFIX + FILE, DL_DIR + FILE)

    except Exception as e:
        print("ERROR:", e)

download("detailed-copy(1).csv")
print(os.path.exists("../../V1/"))