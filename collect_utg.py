#!/usr/bin/env python
"""
Collect complete UTG with 50 events for Chrome
"""
import sys
import time
from droidbot import droidbot as droidbot_module

serial = "1121625397000081"
output_dir = "./output_chrome_50events"

try:
    droidbot = droidbot_module.DroidBot(
        app_path="./chrome_base.apk",
        device_serial=serial,
        output_dir=output_dir,
        event_count=50,
        timeout=300,  # 5 minutes timeout
        keep_app=True,
        keep_env=True,
        grant_perm=True,
        enable_accessibility_hard=True
    )
    print("DroidBot instance created successfully")
    droidbot.start()
    print("DroidBot test completed with 50 events")
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
    sys.exit(1)
