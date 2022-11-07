import datetime
import subprocess
import json
import re
import time
import shutil
import os

def parse_time(s):
    hour, minute, second = s.split(':')
    try:
        hour = int(hour)
        minute = int(minute)
        second = int(float(second))
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

def update_repo_rush(settings, rush_data, pdf_report_path):
    """update rush data on my git repo """

    # /Users/dreadper/Git/2_Public_work/Draed
    rush_repo_path = settings['rush_repo_path']
    report_name = os.path.basename(os.path.normpath(pdf_report_path))

    # adding the pdf to report
    shutil.copyfile(pdf_report_path, rush_repo_path+"/0_reports/"+report_name)

    # add/append a new line to the rush summary file :
    # | :one: | [Project Name](https://Draed.github.io)| <br> Project Description <br><br> | Start Time | End Time | Duration |
    line = "| " +str(rush_data['id'])+ " | ["+str(rush_data['name'])+ "](/0_reports/"+report_name +") | <br> "+str(rush_data['description'])+" <br><br> | "+str(rush_data['start_time'])+" | "+str(rush_data['end_time'])+" | "+str(rush_data['real_duration'])+" | \n"

    f=open(rush_repo_path+"/readme.md", "a")
    f.write(line)
    f.close()