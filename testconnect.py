from pymavlink.dialects.v20 import common as mavlink2
from pymavlink import mavutil
import time


# Start a connection listening on a UDP port
the_connection = mavutil.mavlink_connection('COM3')

# Wait for the first heartbeat 
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))
the_connection.mav.request_data_stream_send(the_connection.target_system, the_connection.target_component,
                                        mavutil.mavlink.MAV_DATA_STREAM_ALL, 10, 1)
time.sleep(3)
try:
    while True:
        try: 
            values = the_connection.messages['ESC_STATUS']  # Note, you can access message fields as attributes!
            timestamp = the_connection.time_since('ESC_STATUS')
            print("servo values:"+ str(values) +" and timestamp: "+ str(timestamp))
        except:
            print('No ESC_STATUS message received')
        time.sleep(0.1)
except KeyboardInterrupt:
    print("terminated")