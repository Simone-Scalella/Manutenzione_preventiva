import nidaqmx
import time
import pandas as pd

def acquisizioneNI(stop,stop1):
    acqui = pd.DataFrame(columns=['Time','Voltage'])
    acquirow = []
    print("NI: avviato")
    i = 0
    while stop.empty():
        
        if(stop1.empty()):
            while stop1.empty() and stop.empty():
                with nidaqmx.Task() as task:
                    task.ai_channels.add_ai_voltage_chan("Dev1/ai1")
                    acquirow.append({'Time':round(time.time_ns()/1000),
                              'Voltage':task.read()})
            print("NI:stop acquisizione, salvataggio in csv") 
              
            for new_row in acquirow:
                acqui = pd.concat([acqui, pd.DataFrame([new_row])], ignore_index=True)
            acqui.to_csv('./measure_NI'+str(i)+'.csv','\t',index=False)
            print('NI:acquisizione'+str(i)+' completa..')

            #remove locking for motor
            stop1.get()
            i += 1
        time.sleep(0.5)



