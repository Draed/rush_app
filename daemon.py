from cli_color_py import red, bright_yellow, yellow, green, bold, underline, blue
# from report import generate_sales_data, plot
from cli import ProjectMeetingQuestion
from utils import notify
import time
import shutil
import threading
from datetime import datetime as dt

class Daemon:

    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, rush_data, event):
        duration = int(rush_data['initial_duration'].strip(" hours"))
        # duration = rush_data['duration'] = "3 hours"
        # duration = 1
        duration_in_sec = int(duration * 60 * 60)
        initial_duration = duration_in_sec
        
        rush_type = rush_data['type']
        # 1/4 project time
        project_quarter_duration = int(duration_in_sec/4)

        # start coutdown
        while duration_in_sec and (not event.is_set()):
            # show available time
            # minn, secc = divmod(duration_in_sec, 60)
            # timeformat = '{:02d}:{:02d}'.format(minn, secc)

            # if modulo 3600 (every hour)
            if duration_in_sec % 3600 == 0 and duration_in_sec < initial_duration-60:
                # is odd
                if duration_in_sec % 1 == 0:
                    notify("[Rush notification] - Pause", "Make a quick pause (1 to 5 min) hydrate yourself")
                # is even
                else:
                    notify("[Rush notification] - Pause", "Make a quick pause (3 to 5 min) to do some stretching and physical exercises")

            # if modulo 1/4 of total time :
            if duration_in_sec % project_quarter_duration == 0 and duration_in_sec < initial_duration-60 and rush_type != "Learning":
                notify("[Rush notification] - Meeting", "Time to do a rush meeting ! ")
                # ProjectMeetingQuestion()
        
            time.sleep(1)
            duration_in_sec -= 1
        else:
            if not event.is_set():
                # when timing coutdown over
                print("\n")
                print(bold(red("Coutdown is over !")).center(shutil.get_terminal_size().columns))
                notify("[Rush notification] - Rush end", "Coutdown is over !")
                # notify main thread that countdown is over
                event.set()
                print(yellow("Press enter to continue").center(shutil.get_terminal_size().columns))
                
    


