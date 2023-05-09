import pandas as pd 
import time

inputVal = pd.DataFrame(columns=["time","pwm_percent"])
for i in range(100,0,-10):
    inputVal = inputVal.append({"time":round(time.time_ns()/1000),"pwm_percent":i},ignore_index=True)

print(inputVal)
inputVal.to_csv("./testcsv.csv",index=False)