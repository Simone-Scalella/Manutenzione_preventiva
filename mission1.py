import dronekit_sitl,time
# Import DroneKit-Python
from dronekit import connect, VehicleMode

sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()


# Connect to the Vehicle.
connection_string = 'COM6'
print("Start simulator (SITL)")
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, wait_ready=True)


print("Starting mission")
# Set mode to AUTO to start mission
vehicle.mode = VehicleMode("AUTO")

while True:
    nextwaypoint=vehicle.commands.next
    print('Distance to waypoint')

    if nextwaypoint==3: #Skip to next waypoint
        print('Skipping to Waypoint 5 when reach waypoint 3')
        vehicle.commands.next=5
        vehicle.commands.upload()
    if nextwaypoint==5: #Dummy waypoint - as soon as we reach waypoint 4 this is true and we exit.
        print ("Exit 'standard' mission when start heading to final waypoint (5)")
        break
    time.sleep(1)