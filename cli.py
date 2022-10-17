from cli_color_py import red, bright_yellow, yellow, green, bold, underline, blue
from database import SearchRushName, GetNotAchievedRush, GetAllRush
import inquirer
import sqlite3
import time


# def phone_validation(answers, current):
#     if not re.match('\+?\d[\d ]+\d', current):
#         raise errors.ValidationError('', reason='I don\'t like your phone number!')

#     return True

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
            c.execute("SELECT * FROM rush")
            rush_list = c.fetchall()
            rush_list = [ rush[1] for rush in rush_list ]
            if rush_list != []:
                questions = [
                    inquirer.List('rush_name_choosen', message="Please choose an existing rush to start : ",
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
        # rush_notachieved_list = GetNotAchievedRush(database_path)
        rush_notachieved_list = GetAllRush(database_path)
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
                        inquirer.Text('duration', message="Enter task duration (estimated with format '00:00:00') ", validate=null_validate)
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
        print(yellow("Describe the progress, blocking elements, \n achieved tasks, updated priorites \n , what is still to do ? "))
        question2 = [
                inquirer.Text('description', message="Report Description : ", validate=null_validate),
        ]
        meeting_description = inquirer.prompt(question2)['description']
        # add the new meeting report to the associated rush
        conn = sqlite3.connect(database_path)
        c = conn.cursor() 
        c.execute('INSERT INTO meeting (description, rush) VALUES (?,?);', (meeting_description, int(rush_data['id'])))
        conn.commit()
        conn.close()
    

def StartRushQuestion():
    questions = [
        inquirer.Confirm('start_rush', message="Start this rush right now ?", default=False),
    ]
    start_rush = inquirer.prompt(questions)['start_rush']
    return start_rush

def EditTaskStatusQuestion(rush_data, database_path):
    #@ TODO
    end_editing = False
    # while not end
    # 1 choose a task in task list or end

    # if end
    # show confirm with alert (tasks not completed will be left unachieved !)
    #end_editing = True

    # 2 edit final duration of the tasks (final_duration)
    pass

class MenuQuestion:

    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def DuringRushQuestion(self, rush_data, database_path, event):
        quit_by_countdown = True
        questions = [
            inquirer.List('during_rush', message=" What to do now ?",
                                        choices=['', 'Show all tasks','Edit task status', 'Write a meeting report', 'End this rush right now'])
        ]
        answers = inquirer.prompt(questions)
        if answers['during_rush'] == '' :
            # hacking for exiting input
            pass
        if answers['during_rush'] == 'Show all tasks' :
            conn = sqlite3.connect(database_path)
            c = conn.cursor()
            task_list = c.execute('SELECT * FROM task WHERE rush = ?', (rush_data['id'],)).fetchall()
            print(task_list)
            conn.close()
            print(green("== Tasks for this rush ( " + rush_data['name'] + " ) : "))
            for task in task_list:
                print(green("=  ✧ " + str(task[1]) + " : " + str(task[2])))

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
                
        
        elif answers['during_rush'] == 'Edit task status':
            EditTaskStatusQuestion(rush_data, database_path)
        
        return quit_by_countdown 

def EndRushQuestion(rush_data, database_path):
    questions = [
        inquirer.Confirm('end_rush', message="Does all tasks have been completed) ?", default=False),
    ]
    end_rush = inquirer.prompt(questions)['end_rush']
    
    if not end_rush:
        # Ask what tasks have been completed
        EditTaskStatusQuestion(rush_data, database_path)
        # @TODO End the rush right now
        # break to quite the while waiting thread loop ?
    else:
        # mean every task have been completed
        conn = sqlite3.connect(database_path)
        c = conn.cursor()
        # update task status to achieved
        c.execute('UPDATE task SET achieved=? WHERE rush=?;', (True, rush_data['id']))
        conn.commit()
        conn.close()