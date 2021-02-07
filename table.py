import re

import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QComboBox, QLineEdit, QHBoxLayout
from PyQt5.QtWidgets import QWidget
from pandas.core.dtypes.common import is_string_dtype

from dataframe_model import DataFrameModel


class Table(QWidget):

    def __init__(self, data):
        super().__init__()

        self.data = data
        self.filtered_data = self.data.copy()
        self.table_view = QtWidgets.QTableView()
        self.table_view.setObjectName("tableView")
        self.grouping_option_selector = QComboBox()
        self.grouping_option_selector.addItems(["None"] + list(self.data.columns))
        self.filter_line = QLineEdit(self)
        self.header = self.table_view.horizontalHeader()
        self.group_by = "None"
        self.grouped_data = None
        self.sort_col_index = 0
        self.ascending = True

        self._set_layout()
        self._set_connections()
        self._group_data()
        self._render_table()

    def _set_layout(self):
        self.layout = QVBoxLayout()

        options_layout = QHBoxLayout()
        options_layout.addWidget(self.grouping_option_selector)
        options_layout.addWidget(self.filter_line)

        self.layout.addLayout(options_layout)
        self.layout.addWidget(self.table_view)
        self.setLayout(self.layout)

    def _set_connections(self):
        self.grouping_option_selector.currentIndexChanged.connect(self._grouping_option_changed)
        self.header.sectionClicked.connect(self._handle_header_clicked)
        self.filter_line.returnPressed.connect(self._handle_filtering_changed)

    def _grouping_option_changed(self):
        self.group_by = self.grouping_option_selector.currentText()
        self.sort_col_index = 0
        self._group_data()
        self._render_table()

    def _handle_filtering_changed(self):
        self.filtering_text = self.filter_line.text()
        mask = np.column_stack([self.data[col].str.contains(self.filtering_text, na=False,  flags=re.IGNORECASE)
                                for col in self.data.columns
                                if is_string_dtype(self.data[col])])
        self.filtered_data = self.data.loc[mask.any(axis=1)]
        self._group_data()
        self._render_table()

    def _handle_header_clicked(self, index):
        self.sort_col_index = index
        order = self.header.sortIndicatorOrder()
        if order == 0:
            self.ascending = True
        else:
            self.ascending = False
        self._render_table()

    def _group_data(self):
        if self.group_by == "None":
            self.grouped_data = self.filtered_data.copy()
        else:
            self.grouped_data = self.filtered_data.groupby(self.group_by, as_index=False).sum()

    def _render_table(self):
        if self.grouped_data is not None:
            table_data = self.grouped_data
            sort_col_name = table_data.columns[self.sort_col_index]
            table_data_sorted = table_data.sort_values(sort_col_name, ascending=self.ascending)
            model = DataFrameModel(table_data_sorted)
            self.table_view.setModel(model)
