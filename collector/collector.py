from . import img_collector
from . import json_collector


collector_table = {
    'img': img_collector,
    'json': json_collector,
}


def load_collector(name):
    if name not in collector_table:
        return None

    return collector_table[name]
