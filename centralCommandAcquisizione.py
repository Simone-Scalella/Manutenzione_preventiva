import runMotor,Telemetry,acquisizione
import time
from threading import Thread 
from queue import Queue
from pymavlink import mavutil


if __name__ == '__main__':
    #Connect to the Vehicle.
    connection_string = 'COM3'

    #stop queue for communication between threads
    stop = Queue(1)
    try:
        
        print("Connecting to vehicle on: %s" % (connection_string,))
        #vehicle = connect(connection_string, wait_ready=True)
        master = mavutil.mavlink_connection(connection_string)
        master.wait_heartbeat()

        #Send a request to get the Telemetry

        #ESC telemetry
        master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,1,
        11030, #Message ID
        100, #interval in us
        1, # response target
        0,0,0,0)
        
        #SYS status(Battery)
        master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,1,
        1, #Message ID:SYS_STATUS
        100, #interval in us
        1, # response target
        0,0,0,0)

        print("vehicle connected and ready...")
        threads = []
        workers = [runMotor.controlMotor,acquisizione.acquisizioneNI,Telemetry.getDrone]
        #0 thread motor control
        #1 thread of National Instrument
        #2 thread acquiring data

        threads.append(Thread(target=workers[0],kwargs={"master":master,"stop":stop,"max":20,"step":5,"pauses":3},daemon=True))
        threads.append(Thread(target=workers[1],kwargs={"stop":stop},daemon=True))
        threads.append(Thread(target=workers[2],kwargs={"master":master,"stop":stop},daemon=True))
        

        for t in threads:
            t.start()
        
        while stop.empty():
            time.sleep(1)
        
    except KeyboardInterrupt:
        stop.put(1)
    
    # wait for the decceleration of the drone 
    print("wait for decceleration..")
    threads[0].join()
    # Close vehicle object before exiting script
    print("operation complete.")
