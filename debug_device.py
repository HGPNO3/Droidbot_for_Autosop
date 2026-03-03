import sys
import os
sys.path.append(os.getcwd())
try:
    from droidbot.device import Device
    import inspect
    print("Device imported")
    print(inspect.signature(Device.__init__))
except Exception as e:
    print(e)
