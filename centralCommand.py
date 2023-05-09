import fortest,fortest2
import multiprocessing

from multiprocessing import get_context

#multiprocessing.set_start_method('spawn')
#context = get_context("spawn").Pool(2)

if __name__ == '__main__':
    workers = [fortest.for1,fortest2.for2]
    for bot in workers:
        p = multiprocessing.Process(target=bot)
        p.start()
