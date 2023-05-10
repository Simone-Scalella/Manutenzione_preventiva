import runMotor,acquisizioneDrone,acquisizione,time
from dronekit import connect
import dronekit_sitl
from threading import Thread 
from queue import Queue

if __name__ == '__main__':

    #informazioni simulati
    #Connect to the Vehicle.
    connection_string = 'COM3'
    #print("Start simulator (SITL)")
    #sitl = dronekit_sitl.start_default()
    #connection_string = sitl.connection_string()
    stop = Queue(1)
    try:
        
        print("Connecting to vehicle on: %s" % (connection_string,))
        vehicle = connect(connection_string, wait_ready=True)
        vehicle
        #master = mavutil.mavlink_connection(host)
        print("vehicle connected and ready...")
        workers = [runMotor.controlMotor,acquisizioneDrone.getFromDrone,acquisizione.acquisizioneNI]
        #p1 e' il thread di azionamento
        #p2 e' il thread di acquisizione Drone.
        #p3 e' il thread di NI

        p1 = Thread(target=workers[0],kwargs={"master":vehicle._master,"stop":stop},daemon=True)
        p2 = Thread(target=workers[1],kwargs={"vehicle":vehicle,"stop":stop},daemon=True)
        p3 = Thread(target=workers[2],kwargs={"stop":stop},daemon=True)

        p1.start()
        p2.start()
        p3.start()

        while stop.empty():
            time.sleep(1)
        #p2.join()
        # Close vehicle object before exiting script
        print("motore accelerazione completa..")
        time.sleep(3)
        p1.join()
        vehicle.close()
    except KeyboardInterrupt:
        stop.put(1)

        p1.join()
        #p2.join()
        # Close vehicle object before exiting script
        time.sleep(3)
        vehicle.close()

