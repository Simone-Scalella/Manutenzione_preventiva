import time

def do_something():
    print('ok')
    time.sleep(3)

try:
    while True:
        do_something()
except KeyboardInterrupt:
    print('pippo')
    pass