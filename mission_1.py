import dronekit_sitl,time
# Import DroneKit-Python
from dronekit import connect, VehicleMode, Command
from pymavlink import mavutil

sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()



# Connect to the Vehicle.
connection_string = 'COM6'
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, wait_ready=True)

#vehicle.wait_ready('parameters')
print("\nPrint all parameters (iterate `vehicle.parameters`):")
for key in vehicle.parameters:
    print(" Key:%s Value:%s" % (key, vehicle.parameters[key]))

#vehicle.armed = True
#vehicle.groundspeed = 0.5

time.sleep(3)

vehicle.close()