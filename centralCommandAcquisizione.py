import runMotor,acquisizioneDrone,acquisizione,testconnect3Thread
import time
from dronekit import connect
import dronekit_sitl
from threading import Thread 
from queue import Queue

if __name__ == '__main__':

    #Connect to the Vehicle.
    connection_string = 'COM3'

    #stop queue for communication between threads
    stop = Queue(1)
    try:
        
        print("Connecting to vehicle on: %s" % (connection_string,))
        vehicle = connect(connection_string, wait_ready=True)
        print("vehicle connected and ready...")
        threads = []
        workers = [runMotor.controlMotor,acquisizioneDrone.getFromDrone,acquisizione.acquisizioneNI,testconnect3Thread.getAllMsg]
        #0 thread motor control
        #1 thread acquiring data
        #2 thread of National Instrument
        #3 thread of esc telemetry, note: telemetry works only when the drone is armed

        threads.append(Thread(target=workers[0],kwargs={"master":vehicle._master,"stop":stop},daemon=True))
        threads.append(Thread(target=workers[1],kwargs={"vehicle":vehicle,"stop":stop},daemon=True))
        threads.append(Thread(target=workers[2],kwargs={"stop":stop},daemon=True))
        threads.append(Thread(target=workers[3],kwargs={"master":vehicle._master,"stop":stop},daemon=True))
        

        for t in threads:
            t.start()
        
        while stop.empty():
            time.sleep(1)
        
    except KeyboardInterrupt:
        stop.put(1)
    
    # wait for the decceleration of the drone 
    threads[0].join()
    # Close vehicle object before exiting script
    vehicle.close()
