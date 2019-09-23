import glob
import os


def get_files(dirpath, patterns, sort=True):
    files = []
    for p in patterns:
        files.extend(glob.glob(os.path.join(dirpath, p)))

    if sort:
        files = sorted(files)

    return files
