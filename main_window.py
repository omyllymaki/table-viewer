from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from table_widget import Table
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self, data: pd.DataFrame):
        super().__init__(flags=Qt.Window)
        self.setWindowTitle('Table viewer')
        self.table = Table(data)
        self.setCentralWidget(self.table)
        self.showMaximized()
