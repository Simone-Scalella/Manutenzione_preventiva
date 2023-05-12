import time,pandas as pd
def getFromDrone(master,stop):
    acquiredRPM = []
    acquiredBatt = []
    print("waiting for rpm data..")
    def acquireRPM(message):
        acquiredRPM.append({"time":round(time.time_ns()/1000),"rpm":message['rpm'][3]})
        print("rpm motor 4: %s" % message['rpm'][3])

    def acquireBatt(message):
        acquiredBatt.append({"time":round(time.time_ns()/1000),"volts":message['voltage_battery']/1000})
        print("get battery with volts: %s" % message['voltage_battery']/1000)
    
    msgCase = {
                'ESC_TELEMETRY_1_TO_4':acquireRPM,
                'SYS_STATUS':acquireBatt
            }
    while stop.empty():
        try:
            #ESC_TELEMETRY manda informazioni solo quando il motore e' armato.
            #print(master.recv_match().to_dict())
            
            message = master.recv_match()
            if (message is not None):
                message = message.to_dict()
                msgCase[message['mavpackettype']](message)
        except Exception as e:
            print(e)
            pass
        time.sleep(0.001)
    
    DFacquiredRPM = pd.DataFrame(columns=['time','rpm'])
    for new_row in acquiredRPM:
        DFacquiredRPM = pd.concat([DFacquiredRPM, pd.DataFrame([new_row])], ignore_index=True)
    DFacquiredRPM.to_csv('./measure_RPM.csv','\t',index=False)

    acquiredBatt = pd.DataFrame(columns=['time','volts'])
    for new_row in acquiredBatt:
        acquiredBatt = pd.concat([acquiredBatt, pd.DataFrame([new_row])], ignore_index=True)
    acquiredBatt.to_csv('/droneOutput.csv',index=False)
    print('RPM:acquisizione completa..')
        


    