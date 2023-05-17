import nidaqmx
import time
import pandas as pd

def acquisizioneNI(stop,stop1):
    print("NI Sim: activated")
    i = 0
    while stop.empty():
        acqui = pd.DataFrame(columns=['Time','Voltage'])
        acquirow = []
        if(stop1.empty()):
            while stop1.empty() and stop.empty():
                acquirow.append({'Time':round(time.time_ns()/1000),
                              'Voltage':10})
                time.sleep(0.001)

            print("NI Sim:stop acquirement, writting into csv...") 
            for new_row in acquirow:
                acqui = pd.concat([acqui, pd.DataFrame([new_row])], ignore_index=True)
            acqui.to_csv('./measure_NI'+str(i)+'.csv','\t',index=False)
            print('NI Sim:acquisizione'+str(i)+' completed.')

            #remove locking for motor
            stop1.get(1)
            i += 1
        time.sleep(0.5)



