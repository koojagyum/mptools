from .util import get_files


def get_imgfiles(dirpath):
    return get_files(dirpath, ['*.png', '*.jpg', '*.jpeg'])


def collect(**kwargs):
    dirpath_key = 'dirpath'
    if dirpath_key in kwargs:
        dirpath = kwargs[dirpath_key]
        return get_imgfiles(dirpath)

    return None
