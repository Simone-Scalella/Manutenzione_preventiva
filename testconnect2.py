import dronekit_sitl,time
# Import DroneKit-Python
from dronekit import connect, VehicleMode, Command
from pymavlink import mavutil

sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()



# Connect to the Vehicle.
connection_string = 'COM6'
print("Start simulator (SITL)")
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, wait_ready=True)

# Get some vehicle attributes (state)
print ("Get some vehicle attribute values:")
print (" Battery: %s" % vehicle.battery)
print (" Last Heartbeat: %s" % vehicle.last_heartbeat)
print (" Is Armable?: %s" % vehicle.is_armable)
print (" System status: %s" % vehicle.system_status.state)
print (" Mode: %s" % vehicle.mode.name)    # settable

i = 0
while i <= 2:
    print(" yaw: ", vehicle._yaw)
    i += 1
    time.sleep(1)

### Test volo

vehicle.arm()

cmds = vehicle.commands
cmds.clear()
lat = 0
lon = 0
altitude = 0
cmd = Command(0,0,0, mavutil.mavlink.MAV_CMD_DO_MOTOR_TEST, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
    0, 0, 0, 0, 0, 0,
    lat, lon, altitude)
cmds.add(cmd)
cmds.upload()

print("\nPrint all parameters (iterate `vehicle.parameters`):")
for key in vehicle.parameters:
    print(" Key:%s Value:%s" % (key,vehicle.parameters[key]))


### fine test

time.sleep(10)

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
sitl.stop()
print("Completed")