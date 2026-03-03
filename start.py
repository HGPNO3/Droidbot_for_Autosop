import sys
import os
import argparse
from droidbot import droidbot as droidbot_module
from droidbot import input_manager
print("DroidBot imported from:", droidbot_module.__file__)
from droidbot.device import Device
import inspect
print("Device init signature:", inspect.signature(Device.__init__))

def parse_args():
    parser = argparse.ArgumentParser(description="Start DroidBot to test an Android app.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-d", action="store", dest="device_serial", required=False,
                        help="The serial number of target device (use `adb devices` to find your device serial).\n"
                             "DroidBot will select the first available device if not specified.")
    parser.add_argument("-a", action="store", dest="apk_path", required=True,
                        help="The file path to target APK")
    parser.add_argument("-o", action="store", dest="output_dir",
                        help="The directory that stores the test output")
    # parser.add_argument("-env", action="store", dest="env_policy",
    #                     help="The environment policy to use during testing. \n"
    #                          "Supported policies:\n"
    #                          "  none\tNo environment will be set. Default.\n")
    parser.add_argument("-policy", action="store", dest="input_policy", default=input_manager.DEFAULT_POLICY,
                        help='The policy to use for test input generation. \n'
                             'Supported policies:\n'
                             '  %s\n'
                             '  %s\n'
                             '  %s\n'
                             '  %s\n'
                             '  %s\n'
                             'Default: %s' % (input_manager.POLICY_NONE,
                                              input_manager.POLICY_MONKEY,
                                              input_manager.POLICY_NAIVE_DFS,
                                              input_manager.POLICY_NAIVE_BFS,
                                              input_manager.POLICY_GREEDY_DFS,
                                              input_manager.DEFAULT_POLICY))
    parser.add_argument("-distributed", action="store", dest="distributed", choices=["master", "worker"],
                        help="Start DroidBot in distributed mode.")
    parser.add_argument("-master", action="store", dest="master",
                        help="DroidBotMaster's RPC address")
    parser.add_argument("-q", action="store", dest="quiet", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="The log level")
    parser.add_argument("-t", action="store", dest="timeout", default=input_manager.DEFAULT_TIMEOUT,
                        help="Timeout in seconds, Default: %d" % input_manager.DEFAULT_TIMEOUT)
    parser.add_argument("-debug", action="store_true", dest="debug_mode",
                        help="Run in debug mode (dump protocol messages).")
    parser.add_argument("-keep_app", action="store_true", dest="keep_app",
                        help="Keep the app on the device after testing.")
    parser.add_argument("-keep_env", action="store_true", dest="keep_env",
                        help="Keep the test environment (no reset) after testing.")
    parser.add_argument("-cv", action="store_true", dest="cv_mode",
                        help="Use OpenCV (instead of UIAutomator) to identify UI components. CV must be installed.")
    parser.add_argument("-u", action="store", dest="humanoid",
                        help="Use humanoid for input generation.")
    parser.add_argument("-ignore_ad", action="store_true", dest="ignore_ad",
                        help="Ignore Ad views.")
    parser.add_argument("-grant_perm", action="store_true", dest="grant_perm",
                        help="Grant all permissions at startup.")
    parser.add_argument("-is_emulator", action="store_true", dest="is_emulator",
                        help="Declare the target device to be an emulator, which would be treated specially by DroidBot.")
    parser.add_argument("-accessibility_auto", action="store_true", dest="enable_accessibility_hard",
                        help="Enable accessibility service automatically even though it might require device restart\n"
                             "(can be useful for Android 7+).")
    parser.add_argument("-humanoid", action="store", dest="humanoid",
                        help="Connect to a Humanoid service (addr:port) for more human-like behaviors.")
    parser.add_argument("-ignore_views_text", action="store_true", dest="ignore_views_text",
                        help="Ignore views' text when identifying the state.")
    parser.add_argument("-replay_output", action="store", dest="replay_output",
                        help="The droidbot output directory being replayed.")
    parser.add_argument("-count", action="store", dest="count", default=input_manager.DEFAULT_EVENT_COUNT, type=int,
                        help="Number of events to generate in total. Default: %d" % input_manager.DEFAULT_EVENT_COUNT)
    parser.add_argument("-interval", action="store", dest="interval", default=input_manager.DEFAULT_EVENT_INTERVAL, type=int,
                        help="Interval in seconds between each two events. Default: %d" % input_manager.DEFAULT_EVENT_INTERVAL)
    return parser.parse_args()


def main():
    """
    the main function
    it starts a droidbot according to the arguments given in cmd line
    """
    opts = parse_args()
    import logging
    if opts.quiet:
        logging.basicConfig(level=opts.quiet.upper())
    
    if opts.distributed:
        print("Starting DroidBot in distributed mode")
        if opts.distributed == "master":
            start_mode = "master"
        else:
            start_mode = "worker"
    else:
        start_mode = "normal"

    if start_mode == "master":
        droidbot_master = droidbot_module.DroidBotMaster(
            app_path=opts.apk_path,
            is_emulator=opts.is_emulator,
            output_dir=opts.output_dir,
            # env_policy=opts.env_policy,
            policy_name=opts.input_policy,
            # random_input=opts.random_input,
            # script_path=opts.script_path,
            event_count=opts.count,
            event_interval=opts.interval,
            timeout=opts.timeout,
            keep_app=opts.keep_app,
            keep_env=opts.keep_env,
            cv_mode=opts.cv_mode,
            debug_mode=opts.debug_mode,
            # profiling_method=opts.profiling_method,
            grant_perm=opts.grant_perm,
            enable_accessibility_hard=opts.enable_accessibility_hard,
            master_address=opts.master,
            humanoid=opts.humanoid,
            ignore_ad=opts.ignore_ad,
            ignore_views_text=opts.ignore_views_text,
            replay_output=opts.replay_output)
        droidbot_master.start()
    elif start_mode == "worker":
        droidbot_worker = droidbot.DroidBotWorker(
            device_serial=opts.device_serial,
            is_emulator=opts.is_emulator,
            output_dir=opts.output_dir,
            # env_policy=opts.env_policy,
            policy_name=opts.input_policy,
            random_input=opts.random_input,
            script_path=opts.script_path,
            event_count=opts.count,
            event_interval=opts.interval,
            timeout=opts.timeout,
            keep_app=opts.keep_app,
            keep_env=opts.keep_env,
            cv_mode=opts.cv_mode,
            debug_mode=opts.debug_mode,
            profiling_method=opts.profiling_method,
            grant_perm=opts.grant_perm,
            enable_accessibility_hard=opts.enable_accessibility_hard,
            master_address=opts.master,
            humanoid=opts.humanoid,
            ignore_ad=opts.ignore_ad,
            ignore_views_text=opts.ignore_views_text,
            replay_output=opts.replay_output)
        droidbot.start()
    else:
        droidbot = droidbot_module.DroidBot(
            app_path=opts.apk_path,
            device_serial=opts.device_serial,
            is_emulator=opts.is_emulator,
            output_dir=opts.output_dir,
            # env_policy=opts.env_policy,
            policy_name=opts.input_policy,
            # random_input=opts.random_input,
            # script_path=opts.script_path,
            event_count=opts.count,
            event_interval=opts.interval,
            timeout=opts.timeout,
            keep_app=opts.keep_app,
            keep_env=opts.keep_env,
            cv_mode=opts.cv_mode,
            debug_mode=opts.debug_mode,
            # profiling_method=opts.profiling_method,
            grant_perm=opts.grant_perm,
            enable_accessibility_hard=opts.enable_accessibility_hard,
            humanoid=opts.humanoid,
            ignore_ad=opts.ignore_ad,
            ignore_views_text=opts.ignore_views_text,
            replay_output=opts.replay_output)
        droidbot.start()


if __name__ == "__main__":
    main()
