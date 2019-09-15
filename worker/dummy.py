import random

from time import sleep


_message = None


def _half_raise():
    if random.random() < 0.5:
        raise Exception


def _quarter_raise():
    if random.random() < 0.25:
        raise Exception


def collect_args():
    import argparse

    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '--message', '-m',
        type=str,
        default=None
    )

    return parser.parse_known_args()


def init():
    global _message

    args, un = collect_args()
    _message = args.message


def process(arg):
    global _message

    sleep(3)
    _quarter_raise()

    return random.random() < 0.5


def main():
    pass


if __name__ == '__main__':
    main()
