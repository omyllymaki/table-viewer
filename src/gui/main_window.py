from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

import pandas as pd

from src.gui.table_widget import Table


class MainWindow(QMainWindow):
    def __init__(self, data: pd.DataFrame):
        super().__init__(flags=Qt.Window)
        self.setWindowTitle('Table viewer')
        self.table = Table(data)
        self.setCentralWidget(self.table)
        self.showMaximized()
