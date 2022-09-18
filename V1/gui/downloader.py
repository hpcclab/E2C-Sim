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
        self.saveFileDialog()

    def saveFileDialog(self):
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
            "QFileDialog.getSaveFileName()",
            DL_DIR,
            "CSV Files (*.csv)", 
            options=self.dialog
        )

        if path:
            self.download(path)

    def download(self, path):
        if not path.endswith(".csv"):
            path = path + ".csv"
        try:
            self.df.to_csv(path)

            print("Download succeeded")

        except Exception as e:
            print("ERROR:", e)