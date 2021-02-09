import glob
import os


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