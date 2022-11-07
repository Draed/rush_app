from cli_color_py import red, bright_yellow, yellow, green, bold, underline, blue
from database import SearchRushName, GetNotAchievedRush, GetAllRush
from datetime import datetime as dt
from datetime import timedelta
from utils import parse_time
import inquirer
import sqlite3
import time


# def phone_validation(answers, current):
#     if not re.match('\+?\d[\d ]+\d', current):
#         raise errors.ValidationError('', reason='I don\'t like your phone number!')

#     return True

def duration_validate(answers, current):
    # pattern = re.compile(r"[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]{1,3})?", re.IGNORECASE)
    if not re.match('[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]{1,3})?', current):
        raise errors.ValidationError('', reason='Please enter correct format (00:00:00)')
    return True

def null_validate(answers, current):
    if not current:
        raise errors.ValidationError('', reason=" Please enter a value")
    return True

def MainRushQuestion(database_path):
    questions = [
        inquirer.List('main', message="What would you like to do ? ",
                              choices=['Create a new rush', 'Show all not achieved rush', 'Start an existing rush', 'exit'])
    ]
    answer = inquirer.prompt(questions)['main']
    
    if answer == "Start an existing rush" : 
        try:
            conn = sqlite3.connect(database_path)
            c = conn.cursor()
            # c.execute("SELECT * FROM rush")
            c.execute("SELECT * FROM rush WHERE achieved = ?", (False,))
            rush_list = c.fetchall()
            rush_list = [ rush[1] for rush in rush_list ]
            if rush_list != []:
                questions = [
                    inquirer.List('rush_name_choosen', message="Please choose an existing rush to start ",
                                        choices=rush_list)
                ]
                answer = inquirer.prompt(questions)['rush_name_choosen']
                # get data from the choosen rush
                rush_data = c.execute('SELECT * FROM rush WHERE name = ?', (answer,)).fetchone()
            else:
                print(yellow("No rush in database, please create one"))
                rush_data = DefineRushQuestion(database_path)
        except:
            print("Database Sqlite3.db not formed.")
            rush_data = None
        finally:
            if conn:
                conn.close()
            return rush_data

    elif answer == "Create a new rush" :
        # Create rush data
        rush_data = DefineRushQuestion(database_path)
        return rush_data
    elif answer == "Show all not achieved rush":
        rush_notachieved_list = GetNotAchievedRush(database_path)
        # rush_notachieved_list = GetAllRush(database_path)
        if rush_notachieved_list:
            print(green("== Rush not achieved : "))
            for rush_element in rush_notachieved_list:
                print(green("=  ✧ " + str(rush_element[0])))
            
            print("\n")
            time.sleep(0.5)
            MainRushQuestion(database_path)
        else:
            print(blue("No rush with status 'not achieved' in database"))
            print("\n")
            MainRushQuestion(database_path)

    else:
        exit()

def DefineRushQuestion(database_path):
    rush_creation_error = True
    task_list = []
    add_task = True
    conn = sqlite3.connect(database_path)
    c = conn.cursor() 
    while rush_creation_error:
        question1 = [
            inquirer.Text('name', message="Enter rush name", validate=null_validate)
        ]
        answers1 = inquirer.prompt(question1)
        rush_name = SearchRushName(database_path, answers1['name'])
 
        if rush_name:
            print(red("A rush with this name already exist in database : " + rush_name[0] ))
        else:    
            question2 = [
                inquirer.Text('description', message="Enter rush description", validate=null_validate),
                inquirer.List('type', message="Choose the rush type", 
                                        choices=['POC', 'Learning', 'Challenge']),
                inquirer.Text('tag', message="Enter rush tag", validate=null_validate),
                inquirer.List('duration', message="Duration of this rush",
                                    choices=['3 hours', '6 hours', '12 hours', '24 hours']),
                inquirer.List('level', message="Choose the rush difficulty", 
                                    choices=['Easy', 'Medium', 'Hard'])
            ]
            answers2 = inquirer.prompt(question2)
            
            while add_task:
                question3 = [
                    inquirer.Confirm('add_task', message="Adding a task ?", default=False)
                ]
                add_task = inquirer.prompt(question3)['add_task']

                if add_task:
                    question_task = [
                        inquirer.Text('name', message="Enter task name", validate=null_validate),
                        inquirer.Text('description', message="Enter task description", validate=null_validate),
                        inquirer.Text('duration', message="Enter task duration (estimated with format '00:00:00') ", validate=duration_validate)
                    ]
                    answer_task = inquirer.prompt(question_task)
                    task_list.append(answer_task)


            # adding rush to database
            c.execute('''
                INSERT INTO rush (name, description, type, tag, level, initial_duration)
                VALUES(?,?,?,?,?,?);
            ''', (answers1['name'],answers2['description'],answers2['type'],answers2['tag'],answers2['level'],answers2['duration']))
            
            rush_id = c.execute('SELECT id FROM rush WHERE name = ?', (answers1['name'],)).fetchone()[0]
            # adding task to database
            for task in task_list:
                c.execute('INSERT INTO task (name, description, duration, achieved, rush) VALUES (?,?,?,?,?);', (task['name'],task['description'], task['duration'], False, int(rush_id)))
            conn.commit()
            conn.close()
            rush_creation_error = False

            print(green("The rush  " + answers1['name'] + " has successfully been created ! You can now choose it within the option 'Start an existing rush' " ))
            print("\n")

def ProjectMeetingQuestion(rush_data, database_path):
    questions = [
        inquirer.Confirm('show_meeting_question', message="Would you like to add a meeting report ?", default=False),
    ]
    show_meeting_question = inquirer.prompt(questions)['show_meeting_question']

    if show_meeting_question:
        start_meeting_dateTime = str(dt.now())
        # start_meeting_dateTime_str = start_meeting_dateTime.strftime('%H:%M:%S')
        print(yellow("Describe the progress, blocking elements, achieved tasks, updated priorites, what is still to do ? "))
        question2 = [
                inquirer.Text('description', message="Report Description ", validate=null_validate),
        ]
        meeting_description = inquirer.prompt(question2)['description']

        late_question = [
            inquirer.Confirm('late_question1', message="Are you late in your project estimation ?", default=False),
        ]
        late_response1 = inquirer.prompt(late_question)['late_question1']

        if late_response1:
            catchup_lost_time_question = [
                inquirer.Confirm('late_question2', message="Is it possible to make up for lost time ?", default=False),
            ]
            catchup_lost_time = inquirer.prompt(catchup_lost_time_question)['late_question2']

            if catchup_lost_time:
                catchup_lost_time_description_question = [
                        inquirer.Text('late_question3', message="Describe how to catch up time ? "),
                ]
                catchup_lost_time_description = inquirer.prompt(catchup_lost_time_description_question)['late_question3']
            else:
                catchup_lost_time_description = ""
        else:
            catchup_lost_time = ""
            catchup_lost_time_description = ""
        
        # add the new meeting report to the associated rush
        conn = sqlite3.connect(database_path)
        c = conn.cursor() 
        c.execute('INSERT INTO meeting (time, late, catchup_lost_time, catchup_lost_time_description, description, rush) VALUES (?,?,?,?,?,?);', (start_meeting_dateTime, late_response1, catchup_lost_time, catchup_lost_time_description,  meeting_description, int(rush_data['id'])))
        conn.commit()
        conn.close()
    

def StartRushQuestion():
    questions = [
        inquirer.Confirm('start_rush', message="Start this rush right now ?", default=False),
    ]
    start_rush = inquirer.prompt(questions)['start_rush']
    return start_rush

def EditTaskStatusQuestion(rush_data, database_path):
    # getting tasks from database :
    conn = sqlite3.connect(database_path)
    c = conn.cursor() 
    c.execute("SELECT * FROM task WHERE rush=?", (rush_data['id'],))
    task_list = c.fetchall()
    final_task_list = []
    task_name_list = [ task[1] for task in task_list ]

    end_editing = False
    while not end_editing:
        question1 = [
            inquirer.List('end_choice', message="Edition menu ", 
                                    choices=['Edit a task data', 'Stop with task editing']),
        ]
        answer1 = inquirer.prompt(question1)['end_choice']

        if answer1  == "Stop with task editing" :
            print(yellow("Beware, tasks with uncompleted data will be left unachieved !"))
            end_editing = True
        
        # Choose a task to edit
        else:
            question2 = [
                inquirer.List('task_edition_choice', message="Choose A task to edit ", 
                                    choices=task_name_list),
            ]
            task_name = inquirer.prompt(question2)['task_edition_choice']
            task_list_index = int(task_name_list.index(task_name))
            
            # show previous data for the task
            print(yellow(str(task_name) + " current status : " + str(task_list[task_list_index][5])))
            question3 = [
                inquirer.Confirm('achieved', message="Does the task have been completed ?", default=True)
            ]
            achieved = inquirer.prompt(question3)['achieved']

            if achieved:
                # show previous data for the task
                print(yellow(str(task_name) + " current estimated duration : " + str(task_list[task_list_index][3]) + " and current final duration " + str(task_list[task_list_index][4])))
                question4 = [ 
                    inquirer.Text('final_duration', message="Enter the task final duration (with format '00:00:00') ", validate=duration_validate),
                    
                ]
                final_duration = inquirer.prompt(question4)['final_duration']
            else:
                final_duration = "00:00:00"

            c.execute('UPDATE task SET final_duration=?, achieved=? WHERE name=?;', (final_duration, achieved, task_name))

    conn.commit()
    conn.close()   



class MenuQuestion:

    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def DuringRushQuestion(self, rush_data, database_path, event):
        quit_by_countdown = True
        if rush_data['type'] == "Learning":
            choice_list = ['', 'Show all tasks', 'Edit task status', 'Show me current data of this rush', 'Make a pause', 'End this rush right now']
        else:
            choice_list = ['', 'Show all tasks', 'Edit task status', 'Show me current data of this rush', 'Make a pause', 'Write a meeting report', 'End this rush right now']

        questions = [
            inquirer.List('during_rush', message=" What to do now ?",
                                        choices=choice_list)
        ]
        answers = inquirer.prompt(questions)
        if answers['during_rush'] == '' :
            # hacking for exiting input
            pass
        if answers['during_rush'] == 'Show all tasks' :
            conn = sqlite3.connect(database_path)
            c = conn.cursor()
            task_list = c.execute('SELECT * FROM task WHERE rush = ?', (rush_data['id'],)).fetchall()
            conn.close()
            print(green("== Tasks for this rush ( " + rush_data['name'] + " ) : "))
            for task in task_list:
                print(green("=  ✧ " + str(task[1]) + " : " + str(task[2])))

        if answers['during_rush'] == 'Show me current data of this rush' : 
            conn = sqlite3.connect(database_path)
            c = conn.cursor()
            task_list = c.execute('SELECT * FROM task WHERE rush = ?', (rush_data['id'],)).fetchall()
            last_pause = c.execute('SELECT * FROM pause WHERE rush = ? ORDER BY start_time DESC LIMIT 1', (rush_data['id'],)).fetchone()
            
            # apply filter on task list to get achieved one and not achieved :
            achieved_task = len(list(filter(lambda task: task[5] == 1, task_list)))
            unachieved_task = len(list(filter(lambda task: task[5] == 0, task_list)))
            initial_duration = int(rush_data['initial_duration'].strip(" hours"))
            estimated_end_time = rush_data['start_time'] + timedelta(hours = initial_duration)
            time_available = estimated_end_time - dt.now()
            print(green("== Data for this rush ( " + rush_data['name'] + " ) : "))
            print(green("=  ✧ Rush started at : " + str(rush_data['start_time']) ))
            print(green("=  ✧ Rush ending estimated at : " + str(estimated_end_time) ))
            print(green("=  ✧ time available before rush end : " + str(time_available) ))
            print(green("=  ✧ Tasks achieved : " + str(achieved_task)+ "/" + str(unachieved_task) ))
            if last_pause:
                print(green("=  ✧ Last pause was at : " + str(last_pause[2]) + " for the reason : " + str(last_pause[1]) ))

        if answers['during_rush'] == 'End this rush right now' :
            question_confirm = [
                inquirer.Confirm('achieved', message="Are you sure to end this rush, now ?", default=False),
            ]
            answer_achieved = inquirer.prompt(question_confirm)['achieved']
            if answer_achieved :
                event.set()
                quit_by_countdown = False
        
        elif answers['during_rush'] == 'Write a meeting report':
            ProjectMeetingQuestion(rush_data, database_path)
        
        elif answers['during_rush'] == 'Make a pause':
            PauseQuestion(rush_data,database_path)
        
        elif answers['during_rush'] == 'Edit task status':
            EditTaskStatusQuestion(rush_data, database_path)
        
        return quit_by_countdown 

def PauseQuestion(rush_data,database_path):
    questions = [
        inquirer.List('pause_reason_question', message="Why are you doing a pause ?",
                                    choices=['Drinking','Stretching', 'Physical exercises','Not productive anymore', 'Too tired', 'Other reason']),
        inquirer.List('pause_initial_question', message="When do you start the pause ?",
                                    choices=['Now','Enter the time'])
    ]
    answer = inquirer.prompt(questions)
    answer1 = answer['pause_initial_question']
    pause_reason = answer['pause_reason_question'] 

    if answer1 == 'Now':
        start_pause_dateTime = dt.now()
        # start_pause_dateTime_str = start_pause_dateTime.strftime('%H:%M:%S')
        
    else:
        question2 = [
            inquirer.Text('start_pause_dateTime', message="Enter the pause start time (format 00:00:00)", validate=duration_validate)
        ]
        start_pause_dateTime_str = inquirer.prompt(question2)['start_pause_dateTime']
        start_pause_dateTime = parse_time(start_pause_dateTime_str)
        start_pause_dateTime = dt(dt.now().year, dt.now().month, dt.now().day, start_pause_dateTime.seconds // 3600, start_pause_dateTime.seconds // 60 % 60, microsecond=10 )


    question3 = [
        inquirer.List('pause_end_question', message="When do you end the pause ?",
                                    choices=['Now','Enter the time'])
    ]
    answer3 = inquirer.prompt(question3)['pause_end_question']

    if answer3 == 'Now':
        end_pause_dateTime = dt.now()
        # end_pause_dateTime_str = end_pause_dateTime.strftime('%H:%M:%S')
        
    else:
        question4 = [
            inquirer.Text('end_pause_final_dateTime', message="Enter the pause end time (format 00:00:00)", validate=duration_validate)
        ]
        end_pause_dateTime_str = inquirer.prompt(question4)['end_pause_final_dateTime']
        end_pause_dateTime = parse_time(end_pause_dateTime_str)
        end_pause_dateTime = dt(dt.now().year, dt.now().month, dt.now().day, end_pause_dateTime.seconds // 3600, end_pause_dateTime.seconds // 60 % 60, microsecond=10)


    pause_duration = end_pause_dateTime - start_pause_dateTime 
    # pushing pause data to database
    conn = sqlite3.connect(database_path)
    c = conn.cursor() 
    c.execute('INSERT INTO pause (reason, start_time, end_time, duration, rush) VALUES (?,?,?,?,?);', (pause_reason ,start_pause_dateTime ,end_pause_dateTime ,str(pause_duration), int(rush_data['id'])))
    conn.commit()
    conn.close()


def EndRushQuestion(rush_data, database_path):
    questions = [
        inquirer.Confirm('end_rush', message="Does all tasks have been completed ?", default=False),
    ]
    end_rush = inquirer.prompt(questions)['end_rush']
    
    if not end_rush:
        # Ask what tasks have been completed
        EditTaskStatusQuestion(rush_data, database_path)
        # change rush status to achieved 
        rush_data.update({"achieved" : True})
    else:
        # mean every task have been completed
        conn = sqlite3.connect(database_path)
        c = conn.cursor()
        # get all unachieved tasks of this rush from db 
        c.execute("SELECT * from task WHERE rush=? AND achieved=? ;", (str(rush_data['id']), False))
        task_list = c.fetchall()
        # for all unachieved tasks change them as done with original estimated duration
        for task in task_list:
            # update task status to achieved
            c.execute('UPDATE task SET achieved=?, final_duration=? WHERE id=?;', (True, task[3], task[0]))
        conn.commit()
        conn.close()

    path_questions = [
        inquirer.Confirm('path_question1', message="Have you a folder in rush repo to refer ?", default=False),
    ]
    path_answer1 = inquirer.prompt(path_questions)['path_question1']

    if path_answer1:
        path_questions2 = [
        inquirer.Path('path_question2', message="Please, enter the path to the markdown file (ex: 6_Virtualization/docker/docker_lab2/docker_lab_2.md)", path_type=inquirer.Path.FILE,),
    ]
    path_answer2 = inquirer.prompt(path_questions2)['path_question2']
    rush_data.update({"markdown_path" : path_answer2})


    aar_questions = [
        inquirer.Confirm('aar_question1', message="Would you like to write an AAR ?", default=False),
    ]
    aar_answer1 = inquirer.prompt(aar_questions)['aar_question1']

    if aar_answer1:
        aar_questions_next = [
            inquirer.Editor('aar_question2', message="How was this session, efficient , productive, what was the blocking element ?", validate=null_validate)
        ]
        aar_description = inquirer.prompt(aar_questions_next)['aar_question2']
    
        # pushing pause data to database
        conn = sqlite3.connect(database_path)
        c = conn.cursor() 
        c.execute('INSERT INTO aar (description, rush) VALUES (?,?);', (aar_description, int(rush_data['id'])))
        conn.commit()
        conn.close()


    return rush_data