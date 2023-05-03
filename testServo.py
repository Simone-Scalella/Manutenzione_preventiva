"""
Example of how to directly control a Pixhawk servo output with pymavlink.
"""

import time
# Import mavutil
from pymavlink import mavutil
# Create the connection
master = mavutil.mavlink_connection('COM3')
#master.reboot_autopilot()
# Wait a heartbeat before sending commands
master.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (master.target_system, master.target_component))

#dati da registrare:
#potenza %
#tempo unix timestamp
for i in range(2,100,10):
    print(i)
    master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_DO_MOTOR_TEST,1,
    1,
    mavutil.mavlink.MOTOR_TEST_THROTTLE_PERCENT,
    i, # pwm-to-output
    6, # timeout in seconds
    1, # number of motors to output
    0, # compass learning
    0
    )
    time.sleep(5)
