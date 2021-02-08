from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QComboBox, QLineEdit, QHBoxLayout, QAbstractItemView
from PyQt5.QtWidgets import QWidget

from dataframe_model import DataFrameModel
from filtering import filter_by_query


class Table(QWidget):
    grouping_options = ["sum", "mean", "median", "count"]

    def __init__(self, data):
        super().__init__()

        self.data = data
        self.filtered_data = self.data.copy()
        self.table_view = QtWidgets.QTableView()
        self.table_view.setObjectName("tableView")
        self.grouping_option_selector = QComboBox()
        self.grouping_option_selector.addItems(self.grouping_options)
        self.filter_line = QLineEdit(self)
        self.header = self.table_view.horizontalHeader()
        self.group_by = None
        self.table_data = None
        self.sort_col_index = 0
        self.ascending = True
        self.grouping_function = self.grouping_options[0]

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
        self.filter_line.returnPressed.connect(self._handle_filtering_changed)

        self.header.sectionClicked.connect(self._handle_header_clicked)
        self.header.setContextMenuPolicy(Qt.CustomContextMenu)
        self.header.customContextMenuRequested.connect(self._handle_header_right_clicked)
        self.header.setSelectionMode(QAbstractItemView.SingleSelection)

    def _handle_header_right_clicked(self, position):
        index = self.header.logicalIndexAt(position)
        if self.group_by is None:
            self.group_by = self.table_data.columns[index]
        else:
            self.group_by = None
        self._group_data()
        self._render_table()

    def _grouping_option_changed(self):
        self.grouping_function = self.grouping_option_selector.currentText()
        self._group_data()
        self._render_table()

    def _handle_filtering_changed(self):
        self.query = self.filter_line.text()
        try:
            self.filtered_data = filter_by_query(self.data, self.query)
            self._set_filter_line_background_white()
        except Exception as e:
            print(e)
            self._set_filter_line_background_red()

        self._group_data()
        self._render_table()

    def _handle_header_clicked(self, index):
        self.sort_col_index = index
        order = self.header.sortIndicatorOrder()
        if order == 0:
            self.ascending = True
        else:
            self.ascending = False
        self._sort_table()
        self._render_table()

    def _group_data(self):
        if self.group_by is None:
            self.table_data = self.filtered_data.copy()
        else:
            self.table_data = self.filtered_data \
                .groupby(self.group_by, as_index=False) \
                .agg(self.grouping_function)

    def _sort_table(self):
        sort_col_name = self.table_data.columns[self.sort_col_index]
        self.table_data = self.table_data.sort_values(sort_col_name, ascending=self.ascending)

    def _render_table(self):
        if self.table_data is not None:
            model = DataFrameModel(self.table_data)
            self.table_view.setModel(model)

    def _set_filter_line_background_red(self):
        self.filter_line.setStyleSheet("QLineEdit"
                                       "{"
                                       "background : red;"
                                       "}")

    def _set_filter_line_background_white(self):
        self.filter_line.setStyleSheet("QLineEdit"
                                       "{"
                                       "background : white;"
                                       "}")
