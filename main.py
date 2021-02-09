import sys
import tkinter.filedialog
from tkinter import filedialog

from PyQt5.QtWidgets import QApplication

from src.data_loading import load_data
from src.gui.main_window import MainWindow
from src.parsing import init_parser
from src.utils import get_file_paths

parser = init_parser()

args = parser.parse_args()

if args.path is None:
    root = tkinter.Tk()
    file_paths = filedialog.askopenfilenames(parent=root, title='Choose files for viewing')
    root.destroy()
else:
    file_paths = get_file_paths(args.path, args.extension, args.recursive)

data = load_data(file_paths, args)

app = QApplication(sys.argv)
mw = MainWindow(data)
mw.show()
app.exec()
