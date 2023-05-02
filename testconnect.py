from pymavlink.dialects.v20 import common as mavlink2
from pymavlink import mavutil

# Start a connection listening on a UDP port
the_connection = mavutil.mavlink_connection('COM6')

# Wait for the first heartbeat 
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

try: 
    altitude = the_connection.messages['GPS_RAW_INT'].alt  # Note, you can access message fields as attributes!
    timestamp = the_connection.time_since('GPS_RAW_INT')
    print(timestamp)
except:
    print('No GPS_RAW_INT message received')