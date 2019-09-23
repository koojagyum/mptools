from time import sleep
from tqdm import tqdm

from .worker import Worker


class WorkManager:

    def __init__(self, module_name=None, module_args=None, num_workers=1):
        self._module_name = module_name
        self._module_args = module_args
        self._num_workers = num_workers
        self._time_elapsed = 0.0

    def _setup_workers(self, num_workers):
        workers = []
        for i in range(0, self.num_workers):
            workers.append(
                Worker(
                    module_name=self.module_name,
                    module_args=self.module_args
                )
            )

        return workers

    def request(self, orders, timeout=0.0, check_interval=0.5):
        workers = self._setup_workers(self.num_workers)

        o = None
        run = True
        while run:
            for w in workers:
                if w.poll() or w.idle:
                    if orders:
                        if o is None:
                            o = orders.pop()
                        print('Request order:', o)
                        if w.request(o):
                            o = None

            # Escape condition
            if not orders:
                run = False
                for w in workers:
                    if not w.idle:
                        run = True
                        break

            if check_interval > 0:
                sleep(check_interval)

        # print report
        for w in workers:
            print(w.orders)


    @property
    def module_name(self):
        return self._module_name

    @property
    def module_args(self):
        return self._module_args

    @property
    def num_workers(self):
        return self._num_workers


def test():
    wm = WorkManager(module_name='dummy', num_workers=4)
    wm.request(
        orders=[
            'hana',
            'dule',
            'set',
            'net',
            'dasut',
            'yeosut',
            'illgope',
            'yeodurb',
            'ahope',
            'yeol',
            'yeolhana',
        ]
    )


if __name__ == '__main__':
    test()
