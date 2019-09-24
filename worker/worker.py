from subprocess import Popen, PIPE

from . import constant
from .nbstreamreader import NonBlockingStreamReader as NBSR


class Worker:
    '''
    Delegate some job to a child process. It is not thread safe.
    '''

    def __init__(self, module_name=None, module_args=None):
        self._module_name = module_name
        self._module_args = module_args

        self._orders_processed = []
        self._orders_failed = []
        self._orders_exception = []

        self._p = None
        self._of = None
        self._reader = None
        self._cmd = None
        self._order = None
        self._orders = {
            'processed': [],
            'failed': [],
            'exception': []
        }

        self._setup_cmd()
        self._setup_p()

    def _setup_cmd(self):
        self._cmd = [
            'python',
            '-m',
            'worker.wrapper',
            '--module_name={}'.format(self.module_name),
        ]
        if self._module_args:
            self._cmd += self._module_args

    def _setup_p(self):
        self._p = Popen(
            self.cmd,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            shell=False
        )
        self._reader = NBSR(self._p.stdout)
        self._of = open(self._p.stdin.fileno(), 'w')

    def _cleanup_p(self):
        if self._of is not None:
            self._of.close()
            self._of = None
        if self._p is not None:
            self._p.terminate()
            self._p = None

    def check_alive(self):
        '''
        Test if the chile process is alive

        :returns: boolean if the process is alive
        :rtype: bool
        '''
        if self._p is None or self._of is None:
            return False

        if self._p.poll() is not None:
            self._cleanup_p()
            return False

        return True

    def request(self, order):
        '''
        Request an order

        :returns: boolean if it is able to retreive an order
        :rtype: bool
        '''
        if not self.idle:
            return False

        self._order = order
        self._of.write(self._order)
        self._of.write('\n')
        self._of.flush()

        return True

    def poll(self):
        '''
        Check if there's processed result and if there is, store to
        orders dic

        :returns: boolean if there's processed result
        :rtype: bool
        '''
        if self._order is None:
            return False

        # if not self.check_alive():
        #     return False

        o = self._reader.readline()
        if not o:
            return False

        retcode = constant.get_retcode(o)
        if retcode == constant.PROCESSED:
            self.orders['processed'].append(self._order)
        elif retcode == constant.FAILED:
            self.orders['failed'].append(self._order)
        elif retcode == constant.EXCEPTION:
            self.orders['exception'].append(self._order)

        self._order = None

        return True

    def __del__(self):
        self._cleanup_p()

    @property
    def idle(self):
        '''
        Check if it is able to retreive an order

        :returns: boolean if it is able to retreive an order
        :rtype: bool
        '''
        if self._order is not None:
            return False

        return self.check_alive()

    @property
    def module_name(self):
        return self._module_name

    @property
    def module_args(self):
        return self._module_args

    @property
    def cmd(self):
        return self._cmd

    @property
    def order(self):
        return self._order

    @property
    def orders(self):
        '''
        Dictionary which consists of 3 key-value pairs
        '''
        return self._orders


def test():
    '''
    test function of worker is mini version of workmanager
    '''

    w = Worker(module_name='dummy', module_args=None)
    orders = ['order1', 'order2', 'order3']

    # version 1
    o = None
    while True:
        if w.poll() or w.idle:
            if orders:
                if o is None:
                    o = orders.pop()
                print('Request order:', o)
                if w.request(o):
                    o = None
            else:
                break

    # version 2: Hard and dirty code
    # o = orders.pop()
    # while orders or not w.idle:
    #     w.poll()
    #     if o and w.request(o):
    #         print('Request order:', o)
    #         o = orders.pop() if orders else None

    print(w.orders)


if __name__ == '__main__':
    test()
