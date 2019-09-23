import sys

from . import loader
from .constant import *


enable_log = False


def collect_args():
    import argparse

    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '--module_name',
        choices=loader.module_table.keys(),
        # default=list(loader.module_table.keys())[0],
        help='Set worker module\'s name.'
    )

    return parser.parse_known_args()[0]


def log(msg):
    global enable_log

    if enable_log:
        with open('./log.txt', 'a') as f:
            f.write(msg)
            f.write('\n')


def loop(w):
    '''Receiving spot'''
    of = open(sys.stdout.fileno(), 'w')

    w.init()
    while True:
        # todo,checkme: waiting method instead of infinite loop?
        for line in sys.stdin:
            res = False
            try:
                res = w.process(line)
                retcode = SUCCESS if (res == True) else FAIL
            except Exception as e:
                retcode = EXCEPTION

            of.write(str(retcode))
            # of.write(', outputof {}'.format(line[:-1]))
            of.write('\n')
            of.flush()

    of.close()


def main():
    args = collect_args()
    w = loader.load_worker_module(args.module_name)
    print('module_name:', args.module_name)
    log('module_name: {}'.format(args.module_name))

    loop(w)


if __name__ == '__main__':
    main()
