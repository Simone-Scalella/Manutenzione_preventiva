import pandas as pd
import time
# Import mavutil
from pymavlink import mavutil

def controlMotor(master,stop,max=20,step=5,pauses=3):
    #dati da registrare:
    #potenza %
    #tempo unix timestamp
    inputVal = pd.DataFrame(columns=["time","pwm_percent"])
    #max = 20
    #step = 5
    rows = []
    print("accelerazione in corso...")
    for i in range(2,max,step):
        print("empowering motor: %s" % i)
        if not stop.empty():
            max = i
            break
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
        rows.append({"time":round(time.time_ns()/1000),"pwm_percent":i})
        time.sleep(pauses)
    print("motor test complete.. writting to csv.")
    print(rows)
    for row in rows:
        pd.concat([inputVal,pd.DataFrame([row])],ignore_index=True)
        print(row)
    inputVal.to_csv("./pwminput.csv",index=False)
    
    #Natural stop
    if stop.empty():
            stop.put(1)
    
    print("deccelerazione in corso...")
    for j in range(max-step,0,-5):
        print("deccelerating motor: %s" % j)
        master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_MOTOR_TEST,1,
        3, #motore 6
        mavutil.mavlink.MOTOR_TEST_THROTTLE_PERCENT,
        j, # pwm-to-output
        3, # timeout in seconds
        1, # number of motors to output
        0, # compass learning
        0
        )
        time.sleep(2)
    
    print("deccelerazione completa.")
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
    