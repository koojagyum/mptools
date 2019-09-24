from manager import WorkManager
from collector.collector import load_collector


def test_imresize():
    wmod = 'imresize'
    cmod = 'img'

    collector = load_collector(cmod)
    orders = collector.collect(dirpath='/home/koodev/Pictures')

    module_args = [
        '--outdir',
        '/home/koodev/mptools_test',
        '-W', '320',
        '-H', '320',
    ]

    wm = WorkManager(
        module_name=wmod,
        module_args=module_args,
        num_workers=3
    )
    report = wm.request(orders=orders)

    print(report)


def test_fail():
    wmod = 'imresize'
    cmod = 'img'

    collector = load_collector(cmod)
    orders = collector.collect(dirpath='/home/koodev')

    module_args = [
        '--outdir',
        '/home/koodev/mptools_fail',
        '-W', '320',
        '-H', '320',
    ]

    wm = WorkManager(
        module_name=wmod,
        module_args=module_args,
        num_workers=3
    )
    report = wm.request(orders=orders)

    print(report)


def test():
    wmod = 'dummy'
    cmod = 'img'

    collector = load_collector(cmod)
    orders = collector.collect(dirpath='/home/koodev/Pictures')

    wm = WorkManager(module_name=wmod, num_workers=4)
    report = wm.request(orders=orders)

    print(report)


if __name__ == '__main__':
    # test()
    test_imresize()
    # test_fail()
