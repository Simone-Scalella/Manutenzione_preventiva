import pandas as pd 
import time

def for2():
    try:
        for i in range(0,10):
            print("fortest2 current index: "+ str(i))
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("for2 interrupt.")