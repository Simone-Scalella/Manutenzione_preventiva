import time,pandas as pd
def getFromDrone(vehicle,stop):
        acqui = pd.DataFrame(columns=['time','voltage','current','level'])
        acquirow = []
        while stop.empty():
            print (" Battery: %s" % vehicle.battery)
            acquirow.append({"time":round(time.time_ns()/1000),"voltage":vehicle.battery.voltage,"current":vehicle.battery.current,"level":vehicle.battery.level})
            time.sleep(0.001)
        print("measurement stopped, writing on csv file..")
        for new_row in acquirow:
            acqui = pd.concat([acqui, pd.DataFrame([new_row])], ignore_index=True)
            acqui.to_csv("./droneOutput.csv",index=False)
        print("acquisizione completa")