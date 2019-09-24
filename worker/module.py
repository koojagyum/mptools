from . import dummy
from . import imresize


module_table = {
    'dummy': dummy,
    'imresize': imresize,
}


def load_worker_module(name):
    if name not in module_table:
        return None

    return module_table[name]
