from pymavlink import mavutil
import dronekit_sitl,time,sys
from dronekit import connect
# Start a connection listening on a UDP port

sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()
#vehicle = connect(connection_string, wait_ready=True)
#master = vehicle._handler.master
## Wait for the first heartbeat 
##   This sets the system and component ID of remote system for the link

master = mavutil.mavlink_connection(connection_string)
master.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (master.target_system, master.target_component))
def request_message_interval(message_id: int, frequency_hz: float):
    """
    Request MAVLink message in a desired frequency,
    documentation for SET_MESSAGE_INTERVAL:
        https://mavlink.io/en/messages/common.html#MAV_CMD_SET_MESSAGE_INTERVAL

    Args:
        message_id (int): MAVLink message ID
        frequency_hz (float): Desired frequency in Hz
    """
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
        message_id, # The MAVLink message ID
        1e6 / frequency_hz, # The interval between two messages in microseconds. Set to -1 to disable and 0 to request default rate.
        0, 0, 0, 0, # Unused parameters
        1, # Target address of message stream (if message has target address fields). 0: Flight-stack default (recommended), 1: address of requestor, 2: broadcast.
    )

time.sleep(3)
print("requesting parameter")
request_message_interval(291,10)
print("printing parameter..")
# Print old parameter value
#message = master.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
#print('name: %s\tvalue: %d' %
#      (message['param_id'].decode("utf-8"), message['param_value']))

# Get some information !
while True:
    try:
        print(master.recv_match().to_dict())
    except:
        #print("nothing received")
        pass
    time.sleep(0.1)
#while True:
#    msg = master.recv_match()
#    if not msg:
#        continue
#    if msg.get_type() == 'HEARTBEAT':
#        print("\n\n*****Got message: %s*****" % msg.get_type())
#        print("Message: %s" % msg)
#        print("\nAs dictionary: %s" % msg.to_dict())
#        # Armed = MAV_STATE_STANDBY (4), Disarmed = MAV_STATE_ACTIVE (3)
#        print("\nSystem status: %s" % msg.system_status)

'''while True:
    time.sleep(0.01)
    try:
        message = master.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
        print('name: %s\tvalue: %d' % (message['param_id'],
                                       message['param_value']))
    except Exception as error:
        print(error)
        sys.exit(0)'''