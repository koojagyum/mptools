from .util import get_files


def collect(**kwargs):
    dirpath_key = 'dirpath'
    if dirpath_key in kwargs:
        dirpath = kwargs[dirpath_key]
        return get_files(dirpath, ['*.json'])

    return None
