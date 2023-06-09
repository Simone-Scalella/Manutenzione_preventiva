import TelemetryDischarge as Telemetry,NIDischarge as NI,NIDischargeSimulation as NiSim
import time
from threading import Thread 
from queue import Queue
from pymavlink import mavutil
import pandas as pd



def controlMotorMax(stop,stop1,max=100,step=10):
    #dati da registrare:
    #potenza %
    #tempo unix timestamp
    #if it exceeds max, run the motor with max    
    #Stop
    

    while stop.empty():
        fase = 1
        print("Motor: Empowering motor: %s" % max)
        master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_MOTOR_TEST,1,
        3,
        mavutil.mavlink.MOTOR_TEST_THROTTLE_PERCENT,
        max, # pwm-to-output
        15, # timeout in seconds
        1, # number of motors to output
        0, # compass learning
        0
        )
        time.sleep(5)

        print("Motor: decelerating motor...")
        for j in range(max-step,0,-step):
            print("Motor: decelerating motor: %s" % j)
            master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_MOTOR_TEST,1,
        3, #motore 6
        mavutil.mavlink.MOTOR_TEST_THROTTLE_PERCENT,
        j, # pwm-to-output
        4, # timeout in seconds
        1, # number of motors to output
        0, # compass learning
        0
        )
            time.sleep(3)
        
        #pause waiting for IO
        time.sleep(5)
        print("Motor: wait IO writting on disk")
        #wait lock for threads
        stop1.put(1)
        stop1.put(1)
        #wait for threads
        
        while (not stop1.empty()) and (stop.empty()):
            time.sleep(0.1)

        print("Motor: all check done, next interation start..")

        
        
    print("Motor: motor control done.")

if __name__ == '__main__':
    #Connect to the Vehicle.
    connection_string = 'COM6'

       
    #simulation
    #import dronekit_sitl
    #sitl = dronekit_sitl.start_default()
    #connection_string = sitl.connection_string()

    #stop queue for communication between threads
    stop = Queue(1)


    #wait for IO writting.
    stop1 = Queue(2)
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
        10, #interval in us
        1, # response target
        0,0,0,0)
        
        #SYS status(Battery)
        master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,1,
        1, #Message ID:SYS_STATUS
        10, #interval in us
        1, # response target
        0,0,0,0)

        print("Main: vehicle connected and ready...")
        threads = []
        workers = [controlMotorMax,NI.acquisizioneNI,Telemetry.getDrone]

        #used for testing fake NI acquisition
        #workers = [controlMotorMax,NiSim.acquisizioneNI,Telemetry.getDrone]
        
        #0 thread motor control
        #1 thread of National Instrument
        #2 thread acquiring data

        threads.append(Thread(target=workers[0],kwargs={"stop":stop,"max":100,"step":10,'stop1':stop1},daemon=True))
        threads.append(Thread(target=workers[1],kwargs={"stop":stop,'stop1':stop1},daemon=True))
        threads.append(Thread(target=workers[2],kwargs={"master":master,"stop":stop,'stop1':stop1},daemon=True))
        

        for t in threads:
            t.start()
        
        while stop.empty():
            time.sleep(1)
        
    except KeyboardInterrupt:
        stop.put(1)
    
    # wait for the decceleration of the drone 
    print("Main: wait for decceleration..")
    threads[0].join()
    print("Main: wait for National Instrument..")
    threads[1].join()
    print("Main: wait for mavlink telemetry..")
    threads[2].join()
    # Close vehicle object before exiting script
    print("Main: data acquisition complete.")
