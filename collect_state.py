import time
import sys
from droidbot.device import Device

serial = "1121625397000081"
output_dir = "./output_chrome"

try:
    device = Device(device_serial=serial, output_dir=output_dir, enable_accessibility_hard=True)
    print("Device created")
    device.set_up()
    print("Device set up")
    device.connect()
    print("Device connected")
    # start chrome
    try:
        device.start_app('com.android.chrome')
        print('Started com.android.chrome')
    except Exception as e:
        print('Failed to start app:', e)
    time.sleep(2)
    state = device.get_current_state()
    if state:
        state.save2dir(output_dir)
        print('State saved to:', output_dir)
        print(state.to_json())
    else:
        print('Failed to get state')
    device.disconnect()
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
