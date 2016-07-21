import fcntl
import sys
import os
import logging
import time


def run():
    time.sleep(20)

if __name__ == '__main__':
    pid_file = '/tmp/%s.pid' % os.path.basename(__file__)
    with open(pid_file, 'w') as fp:
        try:
            fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
            run()
        except IOError as e:
            if e.errno == 11:
                # another instance is running
                logging.warning('Failed to obtain lock')
                sys.exit(0)
            else:
                raise
