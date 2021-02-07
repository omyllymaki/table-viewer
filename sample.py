import glob
import os

import pandas as pd
import argparse
import sys

from PyQt5.QtWidgets import QApplication

from main_window import MainWindow
from parsing import init_parser, get_file_paths

parser = init_parser()

args = parser.parse_args()
file_paths = get_file_paths(args.path, args.extension, args.recursive)

df_list = []
for path in file_paths:
    df = pd.read_csv(path,
                     sep=args.separator,
                     header=args.header_row,
                     decimal=args.decimal,
                     parse_dates=["Kirjauspäivä", "Arvopäivä", "Maksupäivä"],
                     infer_datetime_format=True)
    df_list.append(df)
data = pd.concat(df_list)

print(data.shape)

app = QApplication(sys.argv)
mw = MainWindow(data)
mw.show()
app.exec()
