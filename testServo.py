"""
Example of how to directly control a Pixhawk servo output with pymavlink.
"""

import time
# Import mavutil
from pymavlink import mavutil
# Create the connection
master = mavutil.mavlink_connection('COM3',baud=9600)
#master.reboot_autopilot()
# Wait a heartbeat before sending commands
master.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (master.target_system, master.target_component))

print(mavutil.mavlink.MAV_CMD_DO_MOTOR_TEST)

master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_DO_MOTOR_TEST,int(0),
    int(1),
    int(50), 
    int(2), 
    int(0), 
    int(0), 
    int(0),
    int(0)
    )
