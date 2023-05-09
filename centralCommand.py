import fortest,fortest2
import multiprocessing
from pymavlink import mavutil
from multiprocessing import get_context

#multiprocessing.set_start_method('spawn')
#context = get_context("spawn").Pool(2)

if __name__ == '__main__':
    
    host = 'udpin:localhost:14540'
    #host = 'COM3'
    master = mavutil.mavlink_connection(host)
    workers = [fortest.for1,fortest2.for2]
    for bot in workers:
        p = multiprocessing.Process(target=bot,args=[master])
        p.start()
