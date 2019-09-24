import sys

from . import debug
from . import module
from .constant import *


def collect_args():
    import argparse

    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '--module_name',
        choices=module.module_table.keys(),
        help='Set worker module\'s name.'
    )

    return parser.parse_known_args()[0]


def loop(w):
    '''Receiving spot'''
    of = open(sys.stdout.fileno(), 'w')

    w.init()
    while True:
        for line in sys.stdin:
            res = False
            try:
                res = w.process(line.strip())
                retcode = SUCCESS if (res == True) else FAIL
            except Exception as e:
                retcode = EXCEPTION

            of.write(str(retcode))
            of.write('\n')
            of.flush()

    of.close()


def main():
    args = collect_args()
    w = module.load_worker_module(args.module_name)
    debug.log('module_name: {}'.format(args.module_name))

    loop(w)


if __name__ == '__main__':
    main()
