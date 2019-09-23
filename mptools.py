from worker.manager import WorkManager
from collector.collector import load_collector


def test():
    wmod = 'dummy'
    cmod = 'img'

    collector = load_collector(cmod)
    orders = collector.collect(dirpath='/Users/koodev/Desktop')

    wm = WorkManager(module_name=wmod, num_workers=4)
    report = wm.request(orders=orders)

    print(report)


if __name__ == '__main__':
    test()
