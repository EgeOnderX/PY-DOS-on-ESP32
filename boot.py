#Kernel
import machine, os, time

led = machine.Pin(2, machine.Pin.OUT)
required_files = ["espinit.py", "hal.py", "drivers.py", "edit.py", "startup.py" ]
missing_files = [f for f in required_files if f not in os.listdir()]
if missing_files:
    print("Error:", missing_files)
    for _ in range(2):
        led.value(1)
        time.sleep(0.3)
        led.value(0)
        time.sleep(0.3)
    while True:
        print("Kernel panic!")
        print("Error:", missing_files)
        time.sleep(1)
from hal import *
import espinit
ram = RAM()
disk = Disk()
espinit.start_terminal(ram, disk)