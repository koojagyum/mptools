from . import dummy


module_table = {
    'dummy': dummy,
}


def load_worker_module(name):
    if name not in module_table:
        return None

    return module_table[name]
