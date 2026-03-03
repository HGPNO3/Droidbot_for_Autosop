#!/usr/bin/env python
"""
Collect multiple states from Chrome to build a state transition graph
"""
import sys
import time
import json
import os
from droidbot.device import Device

serial = "1121625397000081"
output_dir = "./output_chrome_utg_50"

try:
    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    states_dir = os.path.join(output_dir, "states")
    if not os.path.exists(states_dir):
        os.makedirs(states_dir)
    
    device = Device(device_serial=serial, output_dir=output_dir, enable_accessibility_hard=True)
    print("Device created")
    device.set_up()
    print("Device set up")
    device.connect()
    print("Device connected")
    
    # Start Chrome
    try:
        device.start_app('com.android.chrome')
        print('Started com.android.chrome')
    except Exception as e:
        print('Failed to start app:', e)
    
    time.sleep(2)
    
    # Collect 50 states with random interactions
    states_data = {
        "states": [],
        "transitions": []
    }
    
    previous_state = None
    
    for i in range(50):
        print(f"\n[{i+1}/50] Collecting state...")
        state = device.get_current_state()
        
        if state:
            state.save2dir(states_dir)
            
            state_info = {
                "step": i + 1,
                "timestamp": state.tag,
                "activity": state.foreground_activity,
                "view_count": len(state.views),
                "state_str": state.state_str
            }
            states_data["states"].append(state_info)
            
            # Record transition if we have a previous state
            if previous_state and previous_state.state_str != state.state_str:
                states_data["transitions"].append({
                    "from": previous_state.state_str,
                    "to": state.state_str,
                    "from_activity": previous_state.foreground_activity,
                    "to_activity": state.foreground_activity
                })
            
            previous_state = state
            print(f"State {i+1}: {state.foreground_activity} ({len(state.views)} views)")
        else:
            print(f"Failed to get state {i+1}")
        
        # Perform random action
        if i < 49:  # Don't perform action after last iteration
            try:
                # Random tap on screen
                import random
                x = random.randint(100, device.get_width() - 100)
                y = random.randint(300, device.get_height() - 100)
                device.view_touch(x, y)
                print(f"Tapped at ({x}, {y})")
            except Exception as e:
                print(f"Failed to perform action: {e}")
            
            time.sleep(1)
    
    # Save state transitions data
    utg_data_path = os.path.join(output_dir, "utg_data.json")
    with open(utg_data_path, "w") as f:
        json.dump(states_data, f, indent=2)
    
    print(f"\n✅ Collected {len(states_data['states'])} states with {len(states_data['transitions'])} transitions")
    print(f"Output directory: {output_dir}")
    
    device.disconnect()
    
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
    sys.exit(1)
