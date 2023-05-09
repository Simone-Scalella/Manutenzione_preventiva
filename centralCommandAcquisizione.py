import runMotor,acquisizioneDrone,time
import multiprocessing
from pymavlink import mavutil
from dronekit import connect
import dronekit_sitl
from threading import Thread 
from queue import Queue

#multiprocessing.set_start_method('spawn')
#context = get_context("spawn").Pool(2)

if __name__ == '__main__':
    
    host = 'udpin:localhost:14540'
    #host = 'COM3'
    # Connect to the Vehicle.
    #connection_string = 'COM3'

    #informazioni simulati
    print("Start simulator (SITL)")
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

    
    print("Connecting to vehicle on: %s" % (connection_string,))
    vehicle = connect(connection_string, wait_ready=True)
    #master = mavutil.mavlink_connection(host)
    print("vehicle connected and ready...")
    stop = Queue(1)
    try:
        workers = [runMotor.controlMotor,acquisizioneDrone.getFromDrone]
        p1 = Thread(target=workers[0],kwargs={"master":vehicle._master,"stop":stop},daemon=True)
        p2 = Thread(target=workers[1],kwargs={"vehicle":vehicle,"stop":stop},daemon=True)

        p1.start()
        p2.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop.put(1)
        p1.join()

    p2.join()
    #p1 = multiprocessing.Process(target=workers[0],kwargs={"master":vehicle._handler})
    #p2 = multiprocessing.Process(target=workers[1],kwargs={"vehicle":vehicle})
    #p1.start()
    #p2.start()

    #for bot in workers:
    #    p = multiprocessing.Process(target=bot,args=[master])
    #    p.start()
