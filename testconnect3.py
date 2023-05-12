from pymavlink.dialects.v20 import common as mavlink2
from pymavlink import mavutil
from pymavlink import dialects
import time
import dronekit_sitl
from pymavlink.dialects.v10 import ardupilotmega as mavlink1

# Start a connection listening on a UDP port
#the_connection = mavutil.mavlink_connection('COM3')
#sitl = dronekit_sitl.start_default()
#connection_string = sitl.connection_string()
#vehicle = connect(connection_string, wait_ready=True)
#master = vehicle._handler.master

## Wait for the first heartbeat 
##   This sets the system and component ID of remote system for the link
connection_string = 'COM3'
master = mavutil.mavlink_connection(connection_string)
master.wait_heartbeat()
#master.mav.param_request_list_send(
#    master.target_system, master.target_component
#)
# Wait for the first heartbeat 
#   This sets the system and component ID of remote system for the link
#the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (master.target_system, master.target_component))

'''master.mav.request_data_stream_send(master.target_system, master.target_component,
                                        mavlink2.ESC_TELEMETRY_1_TO_4, 1, 1)'''

#x = master.mav.command_long_send(
#        master.target_system,
#        master.target_component,
#        mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,1,
#        11030,
#        0,
#        0,
#        0,
#        0,
#        0,
#        2
#        )
#print(x)
'''while True:
    try:
        message = master.recv_match().to_dict()
        if(message['mavpackettype'] == 'ESC_TELEMETRY_1_TO_4'):
            print(message)
        #print(master.messages)
    except:
        #print("nothing received")
        pass
    time.sleep(0.001)'''

while True:
    try:
        message = master.recv_match(type='ESC_TELEMETRY_1_TO_4').to_dict()
        #if(message['mavpackettype'] == 'ESC_TELEMETRY_1_TO_4'):
        print("rpm %s" % message['rpm'][3])
        #print(master.messages)
    except:
        #print("nothing received")
        pass
    #time.sleep(0.001)


'''while True:
    time.sleep(0.01)
    try:
        message = master.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
        print('name: %s\tvalue: %d' % (message['param_id'],
                                       message['param_value']))
    except Exception as error:
        print(error)
        break'''


'''try:
    while True:
        try: 
            print(master.messages)
            print(master.messages['MAV'])
            print(master.messages['HOME'])
            print(master.messages['HEARTBEAT'])
            values = master.messages['ESC_STATUS']  # Note, you can access message fields as attributes!
            timestamp = master.time_since('ESC_STATUS')
            print("servo values:"+ str(values) +" and timestamp: "+ str(timestamp))
        except:
            print('No ESC_STATUS message received')
        time.sleep(0.1)
except KeyboardInterrupt:
    print("terminated")'''

'''try:
    while True:
        try: 
            message = master.recv_match(type='ESC_TELEMETRY_1_TO_4', blocking=False).to_dict()
        except:
            pass
            #print('No ESC_TELEMETRY_1_TO_4 message received')
        time.sleep(0.01)
except KeyboardInterrupt:
    print("terminated")'''