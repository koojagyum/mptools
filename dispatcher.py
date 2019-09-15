import os
import traceback

from subprocess import Popen, PIPE

from nbstreamreader import NonBlockingStreamReader as NBSR
from worker import wrapper
from worker.wrapper import get_retcode
from worker.wrapper import verbose_retcode


def collect_args():
    import argparse

    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '--jobs', '-j',
        default=1,
        help='Set number of worker modules.'
    )

    return parser.parse_known_args()


def test():
    args, unknown_args = collect_args()
    print('j:', args.jobs)

    try:
        cmd = [
            'python',
            '-m',
            'worker.wrapper',
            '--worker_name={}'.format('dummy'),
        ]
        cmd += unknown_args

        p = Popen(
            cmd,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            shell=False
        )
        nbsr = NBSR(p.stdout)
        of = open(p.stdin.fileno(), 'w')

        a = of.write('COMMAND1\n')
        of.flush()

        cnt = 0
        while True:
            output = nbsr.readline(1)

            if not output:
                continue

            print('[{}] output:'.format(cnt), output)
            retcode = get_retcode(output)
            # print('[{}] Output retcode: {} ({})'.format(
            #     cnt, retcode, verbose_retcode(retcode)
            # ))

            if retcode is wrapper.SUCCESS:
                cnt += 1
                of.write('{}\n'.format(cnt))
            else:
                of.write('{}\n'.format(cnt))

            of.flush()

        of.close()

    except Exception as e:
        p.terminate()
        print(e)
        traceback.print_exc()
        of.close()


def main():
    pass


if __name__ == '__main__':
    # main()
    test()

