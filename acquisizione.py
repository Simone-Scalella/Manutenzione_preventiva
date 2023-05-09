import nidaqmx
import csv
import time
import keyboard
import csv
import pandas as pd

acqui = pd.DataFrame(columns=['Time','Value'])
acquirow = []
try:
    while True:
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
            '''new_row  = {'Time':round(time.time_ns()/1000),
                          'Value':task.read()}'''
            acquirow.append({'Time':round(time.time_ns()/1000),
                          'Value':task.read()})
            
            
except KeyboardInterrupt:
    for new_row in acquirow:
        acqui = pd.concat([acqui, pd.DataFrame([new_row])], ignore_index=True)
    acqui.to_csv('./measure_internation_instrument.csv','\t',index=False)
    print('acquisizione completa..')



