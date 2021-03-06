# -*- coding: utf-8 -*-

from multiprocessing.pool import Pool
from time import sleep
# from random import randint

ADD_FAST = 0
ADD_SLOW = 1

class BlockedPool(Pool):
    def __init__(self, processes, lowsize, batchsize):
        super(BlockedPool, self).__init__(processes)
        self.lowsize = lowsize
        self.fastsize = batchsize
        self.fastcnt = 0
        self.addmod = ADD_FAST
 
    def apply_block_async(self, func, args=(), kwds={}, callback=None,
            error_callback=None):

        if self.addmod == ADD_FAST:
            self.fastcnt = self.fastcnt + 1
            if self.fastcnt > self.fastsize:
                self.addmod = ADD_SLOW
                self.fastcnt = 0
        else:
            if self._taskqueue.qsize() < self.lowsize:
                self.addmod = ADD_FAST
            else:
#                 sleep(randint(1, 5))
                sleep(2)
                
        return self.apply_async(func, args, kwds, callback, error_callback)

def call_main():

    pool = BlockedPool(10, 5000, 1000)

    num = 0
    for input in range(1000):

        pool.apply_block_async(lambda x:print(x), (input, ))

        if num % 10 == 0:
            nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            sys.stdout.write('\rprogress: %s, (% 10d)%s' % (nowtime, num, phone_num))
            sys.stdout.flush()

        num = num + 1

    pool.close()
    pool.join()

if __name__ == "__main__":
    call_main()
