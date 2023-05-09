from pymavlink import mavutil

# Start a connection listening on a UDP port
host = 'udpin:localhost:14540'
#host = 'COM3'
master = mavutil.mavlink_connection(host)

# Wait for the first heartbeat 
#   This sets the system and component ID of remote system for the link
master.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (master.target_system, master.target_component))

def requestparameter(master,param):
    # param =b'
    # Request parameter
    master.mav.param_request_read_send(
        master.target_system, master.target_component,
        param,
        -1
    )

    # Print old parameter value
    message = master.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
    print('name: %s\tvalue: %d' %
          (message['param_id'].decode("utf-8"), message['param_value']))