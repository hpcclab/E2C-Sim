import os, urllib.request, datetime
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from pandas import DataFrame


class Downloader(QMainWindow):

    def __init__(self, df: DataFrame, type: str):
        # Initialize self
        super().__init__()
        self.setWindowTitle("Save File")
        self.setStyleSheet(f"background-color: rgb(217,217,217);")
        self.df = df
        self.type = type

        # Go live
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.resize(640, 480)
        if self.type == "EET":
            self.saveFileDialogEET()
        elif self.type == "Workload":
            self.saveFileDialogWKL()
        elif self.type == "Scenario":
            self.saveFileDialogSCEN()

    def saveFileDialogEET(self):
        # Get user's Downloads dir
        if os.name == "nt":
            DL_DIR = f"{os.getenv('USERPROFILE')}\\Downloads"            
        else:
            DL_DIR = f"{os.getenv('HOME')}/Downloads"

        # Initialize dialog
        self.dialog = QFileDialog.Options()
        self.dialog |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save EET File as CSV",
            DL_DIR,
            "CSV Files (*.csv.eet)", 
            options=self.dialog
        )

        if path:
            self.downloadEET(path)

    def downloadEET(self, path):
        if not path.endswith(".csv.eet"):
            path = path + ".csv.eet"
        try:
            self.df.to_csv(path, index = False)

            print("Download succeeded")

        except Exception as e:
            print("ERROR:", e)

    def saveFileDialogWKL(self):
        # Get user's Downloads dir
        if os.name == "nt":
            DL_DIR = f"{os.getenv('USERPROFILE')}\\Downloads"            
        else:
            DL_DIR = f"{os.getenv('HOME')}/Downloads"

        # Initialize dialog
        self.dialog = QFileDialog.Options()
        self.dialog |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Workload File as CSV",
            DL_DIR,
            "CSV Files (*.csv.wkl)", 
            options=self.dialog
        )

        if path:
            self.downloadWKL(path)

    def downloadWKL(self, path):
        if not path.endswith(".csv.wkl"):
            path = path + ".csv.wkl"
        try:
            self.df.to_csv(path, index = False)

            print("Download succeeded")

        except Exception as e:
            print("ERROR:", e)

    def saveFileDialogSCEN(self):
        # Get user's Downloads dir
        if os.name == "nt":
            DL_DIR = f"{os.getenv('USERPROFILE')}\\Downloads"            
        else:
            DL_DIR = f"{os.getenv('HOME')}/Downloads"

        # Initialize dialog
        self.dialog = QFileDialog.Options()
        self.dialog |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Scenario File as CSV",
            DL_DIR,
            "CSV Files (*.csv.scen)", 
            options=self.dialog
        )

        if path:
            self.downloadSCEN(path)

    def downloadSCEN(self, path):
        if not path.endswith(".csv.scen"):
            path = path + ".csv.scen"
        try:
            self.df.to_csv(path, index = False)

            print("Download succeeded")

        except Exception as e:
            print("ERROR:", e)