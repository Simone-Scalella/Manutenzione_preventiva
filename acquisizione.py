import nidaqmx
import time
import pandas as pd

def acquisizioneNI(stop):
    acqui = pd.DataFrame(columns=['Time','Value'])
    acquirow = []
    print("NI: avviato")
    while stop.empty():
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
            '''new_row  = {'Time':round(time.time_ns()/1000),
                          'Value':task.read()}'''
            acquirow.append({'Time':round(time.time_ns()/1000),
                          'Value':task.read()})
    print("NI:stop acquisizione, salvataggio in csv")       
    for new_row in acquirow:
        acqui = pd.concat([acqui, pd.DataFrame([new_row])], ignore_index=True)
    acqui.to_csv('./measure_NI.csv','\t',index=False)
    print('NI:acquisizione completa..')



