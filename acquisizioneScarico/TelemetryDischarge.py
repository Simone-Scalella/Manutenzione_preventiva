import time,pandas as pd
def getDrone(master,stop,stop1):
    print("Telemetry: activated.")
    def acquireRPM(message):
        acquiredRPM.append({"time":round(time.time_ns()/1000),"rpm":message['rpm'][3]})

    def acquireBatt(message):
        acquiredBatt.append({"time":round(time.time_ns()/1000),"volts":float(message['voltage_battery']/1000)})
    
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
                #time.sleep(0.00001)
            
            print("Telemetry: Writting to the csv..")
            
            if len(acquiredRPM)>0:

                print(acquiredRPM[-1])
            else:
                print("Telemetry: No RPM data acquired.")

            if len(acquiredRPM)>0:
                print(acquiredBatt[-1])
            else:
                print("Telemetry: No Battery data acquired.")
            
            
            for new_row in acquiredRPM:
                DFacquiredRPM = pd.concat([DFacquiredRPM, pd.DataFrame([new_row])], ignore_index=True)
            DFacquiredRPM.to_csv('./measure_RPM'+str(i)+'.csv','\t',index=False)
            print("Telemetry: written to: measure_RPM"+str(i)+'.csv')
            
            for new_row in acquiredBatt:
                DFacquiredBatt = pd.concat([DFacquiredBatt, pd.DataFrame([new_row])], ignore_index=True)
            DFacquiredBatt.to_csv('./measure_Volts'+str(i)+'.csv','\t',index=False)
            print("Telemetry: written to: measure_Volts"+str(i)+'.csv')
            
            i += 1
            ##battery low: shutdown
            if(len(acquiredBatt)):
                print("Battery voltage: "+ str(acquiredBatt[-1]['volts']))
            
            if(acquiredBatt[-1]['volts'] <= 15.2):
                print("Telemetry: battery too low, proceeds to shut down motors..")
                stop.put(1)
            #removing the locking
            stop1.get(1)    
        time.sleep(0.5)

    print('Telemetry: acquisizione completa..')
        


    