# -*- coding: utf-8 -*-

import sys
import time

def processbar():

    for num in range(1000):
        nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        sys.stdout.write('\r%s progress (% 10d)' % (nowtime, num))
        sys.stdout.flush()
        time.sleep(1)

if __name__ == '__main__':
    processbar()
