import pandas as pd 
import time

def for1():
    try:
        for i in range(0,10):
            print("fortest1 current index: "+ str(i))
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("for1 interrupt.")
