from cli import DefineRushQuestion, StartRushQuestion, MainRushQuestion, MenuQuestion, EndRushQuestion
from cli_color_py import red, bright_yellow, yellow, green, bold, underline, blue
from daemon import Daemon
from report import create_html_report, convert_html_to_pdf
from database import databaseInit, databaseImport
from utils import update_repo_rush

from datetime import datetime as dt
import shutil
import json
import threading
import time, datetime
import sqlite3

# Print welcome
print("\n")
print(underline(blue("[ --- Rush App --- ]")).center(shutil.get_terminal_size().columns))
print("\n")
print(blue("Welcome to Rush app, a tool to start an IT challenge limited in time.").center(shutil.get_terminal_size().columns))
print(blue("You can set the parameters in the file 'rush_settings.json' ").center(shutil.get_terminal_size().columns))
print("\n")

# load setting data
print(blue("loading data from setting file ... ").center(shutil.get_terminal_size().columns))
time.sleep(0.5)
f = open('ressources/rush_settings.json')
settings = json.load(f)
database_path = settings['database_path']
f.close()

# init database
print(blue("Database initialization ... ").center(shutil.get_terminal_size().columns))
time.sleep(0.3)
databaseInit(database_path)
databaseImport(database_path, settings['rush_list_data_path'])

# # show settings : 
# print("===================================================  ".center(shutil.get_terminal_size().columns))
# print(("        == A pause will be programmed every : " + bold(pause_every) + "   ==  ").center(shutil.get_terminal_size().columns))
# print(("        == These pause will last : " + bold(pause_duration)  + "              ==  ").center(shutil.get_terminal_size().columns))
# print("===================================================  ".center(shutil.get_terminal_size().columns))
# print("\n")
rush_data = None
start_bool = False

while rush_data == None or start_bool == False:
    rush_data = MainRushQuestion(database_path)
    start_bool = StartRushQuestion()

else:
    # change rush_data from tuple to dict : 
    start_dateTime = dt.now()
    rush_data = {"id" : rush_data[0], "name" : rush_data[1], "description" : rush_data[2], "type" : rush_data[3], "tag" : rush_data[4], "initial_duration" : rush_data[5], "level" : rush_data[6], "start_time" : start_dateTime, "achieved" : rush_data[10]}

    # create a new thread Event
    event = threading.Event()

    # Thread 1 is the countdown (Daemon)
    print(blue("Rush Started at :  " + str(start_dateTime)).center(shutil.get_terminal_size().columns))
    RushDaemon = Daemon()
    background_daemon = threading.Thread(target=RushDaemon.run, args=(rush_data, event))
    background_daemon.start()
    print(bold(green("Daemon Started")).center(shutil.get_terminal_size().columns))
    print("\n")

    # While waiting for the thread 1 to set event, ask question
    menuQuestion = MenuQuestion()

    while not event.is_set():
        during_question_thread = threading.Thread(target=menuQuestion.DuringRushQuestion, args=(rush_data, database_path, event))
        during_question_thread.start()
        during_question_thread.join()

    ## When rush is over
    ## Mean Countdown from Daemon is over OR End rush was choosen during question
    end_dateTime = dt.now()
    real_duration = end_dateTime - rush_data["start_time"]
    rush_data.update({"end_time" : end_dateTime})
    rush_data.update({"real_duration" : real_duration})
    rush_data.update({"achieved" : True})

    # Rush end question (will push data task to database)
    new_rush_data = EndRushQuestion(rush_data, database_path)
    markdown_path = new_rush_data['markdown_path']

    # update rush's info
    conn = sqlite3.connect(database_path)
    c = conn.cursor()        
    c.execute('UPDATE rush SET start_time=?, end_time=?, real_duration=?, achieved=?  WHERE id=?;', (str(rush_data['start_time']), str(rush_data['end_time']), str(rush_data['real_duration']), rush_data['achieved'],  rush_data['id']))
    conn.commit()
    conn.close()

    print("\n")
    print(blue("Generating report ...").center(shutil.get_terminal_size().columns))
    report_path = create_html_report(rush_data, settings)
    pdf_report_path = convert_html_to_pdf(rush_data, report_path)
    print(bold(green("Rush report generated ! File is avalaible under 'reports' folder ").center(shutil.get_terminal_size().columns)))
    print("\n")

    # generate report for all previous rushes
    # @TODO
    print(blue("Gloabl report initialization ... ").center(shutil.get_terminal_size().columns))
    print(bold(green("Global report generated ! File is avalaible under 'reports' folder ").center(shutil.get_terminal_size().columns)))
    print("\n")

    # push last data to project repo
    update_repo_rush(settings, rush_data, pdf_report_path, markdown_path)
    print(blue("Pushing reports to portofolio ... ").center(shutil.get_terminal_size().columns))
    print(bold(green("Portofolio content updated !").center(shutil.get_terminal_size().columns)))
    print("\n")
