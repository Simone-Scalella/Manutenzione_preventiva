import nidaqmx
import csv
import time

acqui = []
while True:
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        acqui.append([])
        acqui[-1].append([time.time_ns()/1000,task.read()])
        print(acqui[-1][0])



