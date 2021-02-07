import argparse
import glob
import os


def init_parser():
    parser = argparse.ArgumentParser(description='Read in a file or set of files, and return the result.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--path', default=None, nargs='+', help='File paths or folder of files. File dialog is openened if None (default value).')
    parser.add_argument('-e', '--extension', default=None, help='File extension to filter by. By defauilt None which means no filtering by extension.')
    parser.add_argument('-r', '--recursive', action='store_true', default=False, help='Make recursive search through sub folders.')
    parser.add_argument('-s', '--separator', default=None, help="Delimiter to use. If none, it is detected automatically.")
    parser.add_argument('-d', '--decimal', default=".", help="Decimal to use.")
    parser.add_argument('-hr', '--header', type=int, default=0, help="Row number(s) to use as the column names.")
    parser.add_argument('-dt', '--datetime', default=None, nargs='+', help='Datetime column names.')
    return parser


def get_file_paths(paths, extension=None, recursive_search=False):
    full_paths = [os.path.join(os.getcwd(), path) for path in paths]

    file_paths = set()
    for path in full_paths:
        if os.path.isfile(path):
            file_extension = os.path.splitext(path)[-1]
            if (extension is None) or (file_extension == extension):
                file_paths.add(path)
        else:
            if recursive_search:
                full_paths += glob.glob(path + '/*')

    return file_paths
