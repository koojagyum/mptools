import sys

from . import loader


enable_log = False

SUCCESS = 0
FAIL = 1
EXCEPTION = 2

retcode_table = {
    'SUCCESS': SUCCESS,
    'FAIL': FAIL,
    'EXCEPTION': EXCEPTION,
}


def get_retcode(output):
    i = output[0] - ord('0')
    return list(retcode_table.values())[i]


def verbose_retcode(c):
    return list(retcode_table.keys())[c]


def collect_args():
    import argparse

    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '--worker_name',
        choices=loader.module_table.keys(),
        default=list(loader.module_table.keys())[0],
        help='Set worker module\'s name.'
    )

    return parser.parse_known_args()[0]


def log(msg):
    global enable_log

    if enable_log:
        with open('./log.txt', 'a') as f:
            f.write(msg)


def loop(w):
    '''Receiving spot'''
    of = open(sys.stdout.fileno(), 'w')

    w.init()
    while True:
        for line in sys.stdin:
            res = False
            try:
                res = w.process(line)
                retcode = SUCCESS if (res == True) else FAIL
            except Exception as e:
                retcode = EXCEPTION

            of.write(str(retcode))
            of.write('\n')
            of.flush()

            # sys.stdout.write(str(retcode))
            # sys.stdout.write('\n')
            # sys.stdout.flush()

    of.close()


def main():
    args = collect_args()
    w = loader.load_worker_module(args.worker_name)
    print('worker_name:', args.worker_name)

    loop(w)


if __name__ == '__main__':
    main()
