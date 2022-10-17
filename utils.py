import datetime
import subprocess
import json
import re
import time

def parse_time(s):
    hour, minute, second = s.split(':')
    try:
        hour = int(hour)
        minute = int(minute)
        second = int(second)
    except ValueError:
        return "ValueError"
    
    return datetime.timedelta(hours=hour, minutes=minute, seconds=second)

def notify(title, text):
    ## for mac os
    # source : https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/reference/ASLR_cmds.html#//apple_ref/doc/uid/TP40000983-CH216-SW224
    script = 'display notification "{}" with title "{}" sound name "Ping"'.format(text, title)
    subprocess.call(['osascript', '-e', script], text = True)
    ## for ubuntu
    #notify-send "title" "message"
    ## for windows
    #New-BurntToastNotification -Text "title", 'message'

def dialogWithButton(title, text):
    ## for mac os
    script = 'display dialog "{}" with title "{}" buttons {"Yes", "No"} default button "No" giving up after 180 with icon note'.format(text, title)
    result = subprocess.check_output(['osascript', '-e', script], text = True)
    #print(result.decode("utf-8"))

