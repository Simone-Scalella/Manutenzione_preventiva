"""
Example of how to directly control a Pixhawk servo output with pymavlink.
"""

import time
# Import mavutil
from pymavlink import mavutil
# Create the connection
master = mavutil.mavlink_connection('COM6')
#master.reboot_autopilot()
# Wait a heartbeat before sending commands
master.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (master.target_system, master.target_component))

#dati da registrare:
#potenza %
#tempo unix timestamp
max = 30
print("accelerazione in corso...")
for i in range(2,max,2):
    print(i)
    master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_DO_MOTOR_TEST,1,
    3,
    mavutil.mavlink.MOTOR_TEST_THROTTLE_PERCENT,
    i, # pwm-to-output
    6, # timeout in seconds
    1, # number of motors to output
    0, # compass learning
    0
    )
    time.sleep(3)

print("deccelerazione in corso...")
for j in range(max,0,-10):
    print(j)
    master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_DO_MOTOR_TEST,1,
    3, #motore 6
    mavutil.mavlink.MOTOR_TEST_THROTTLE_PERCENT,
    j, # pwm-to-output
    5, # timeout in seconds
    1, # number of motors to output
    0, # compass learning
    0
    )
    time.sleep(3)

'''time.sleep(3)

master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_DO_MOTOR_TEST,1,
    6,
    mavutil.mavlink.MOTOR_TEST_THROTTLE_PERCENT,
    5, # pwm-to-output
    6, # timeout in seconds
    1, # number of motors to output
    0, # compass learning
    0
    )'''
