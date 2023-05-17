import time,pandas as pd
def getDrone(master,stop,stop1):
    print("waiting for rpm data..")
    def acquireRPM(message):
        acquiredRPM.append({"time":round(time.time_ns()/1000),"rpm":message['rpm'][3]})
        #print("rpm motor 4: %s" % message['rpm'][3])

    def acquireBatt(message):
        acquiredBatt.append({"time":round(time.time_ns()/1000),"volts":float(message['voltage_battery']/1000)})
        #print("get battery with volts: %s" % float(message['voltage_battery']/1000))
    
    msgCase = {
                'ESC_TELEMETRY_1_TO_4':acquireRPM,
                'SYS_STATUS':acquireBatt
            }
    
    i = 0
    while stop.empty():
        acquiredRPM = []
        acquiredBatt = []
        DFacquiredRPM = pd.DataFrame(columns=['time','rpm'])
        DFacquiredBatt = pd.DataFrame(columns=['time','volts'])
        
        if stop1.empty():
            while stop1.empty() and stop.empty():
                try:
                #ESC_TELEMETRY manda informazioni solo quando il motore e' armato. 
                    message = master.recv_match()
                    if (message is not None):
                        message = message.to_dict()
                        msgCase[message['mavpackettype']](message)
                except Exception as e:
                    pass
                time.sleep(0.00001)
            
            print("run complete writting to the csv..")
            print(acquiredRPM[-1])
            print(acquiredBatt[-1])
            
            for new_row in acquiredRPM:
                DFacquiredRPM = pd.concat([DFacquiredRPM, pd.DataFrame([new_row])], ignore_index=True)
            DFacquiredRPM.to_csv('./measure_RPM'+str(i)+'.csv','\t',index=False)

            
            for new_row in acquiredBatt:
                DFacquiredBatt = pd.concat([DFacquiredBatt, pd.DataFrame([new_row])], ignore_index=True)
            DFacquiredBatt.to_csv('./measure_Volts'+str(i)+'.csv','\t',index=False)

            #battery low: shutdown
            if(acquiredBatt[-1]['volts'] <= 15.2):
                stop.put()
            #removing the locking
            stop1.put()    
        time.sleep(0.5)

    print('RPM:acquisizione completa..')
        


    