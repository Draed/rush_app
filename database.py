import sqlite3
import json

def databaseInit(database_path):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    # rush
    c.execute("""CREATE TABLE IF NOT EXISTS rush 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL,
                description TEXT,
                type TEXT,
                tag TEXT,
                initial_duration TEXT,
                level TEXT,
                start_time TEXT,
                end_time TEXT,
                real_duration TEXT,
                achieved BOOLEAN DEFAULT False NOT NULL,
                markdown_path TEXT
                );
            """)
    # task
    c.execute("""CREATE TABLE IF NOT EXISTS task 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT,
                description TEXT,
                start_time TEXT,
                end_time TEXT,
                duration TEXT,
                final_duration TEXT,
                achieved BOOLEAN,
                rush INTEGER,
                FOREIGN KEY (rush) REFERENCES rush(id)
                );
            """)
    # meeting
    c.execute("""CREATE TABLE IF NOT EXISTS meeting 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                description TEXT,
                time TEXT,
                late BOOLEAN,
                catchup_lost_time BOOLEAN,
                catchup_lost_time_description TEXT,
                rush INTEGER,
                FOREIGN KEY (rush) REFERENCES rush(id)
                );
            """)
    # pause
    c.execute("""CREATE TABLE IF NOT EXISTS pause 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                reason TEXT,
                start_time TEXT,
                end_time TEXT,
                duration TEXT,
                rush INTEGER,
                FOREIGN KEY (rush) REFERENCES rush(id)
                );
            """)
    # aar
    c.execute("""CREATE TABLE IF NOT EXISTS aar 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                description TEXT,
                rush INTEGER,
                FOREIGN KEY (rush) REFERENCES rush(id)
                );
            """)
    conn.close()

def databaseImport(database_path, json_path):
    f = open(json_path)
    rush_list_to_import = json.load(f)
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    for rush in rush_list_to_import:
        rush_id = c.execute('SELECT id FROM rush WHERE name = ?', (rush['name'],)).fetchone()
        # if rush did not already exist, add it
        if not rush_id:
            # add rush
            c.execute('''
                    INSERT INTO rush (name, description, type, tag, initial_duration, level)
                    VALUES(?,?,?,?,?,?);
                ''', (rush['name'],rush['description'],rush['type'],rush['tag'],rush['initial_duration'],rush['level']))
            rush_id = c.execute('SELECT id FROM rush WHERE name = ?', (rush['name'],)).fetchone()[0]
            # add tasks
            for task in rush['task_list']:
                c.execute('INSERT INTO task (name, description, duration, achieved, rush) VALUES (?,?,?,?,?);', (task['name'],task['description'], task['duration'], False, int(rush_id)))

    conn.commit()
    conn.close()
    # clear json file
    with open(json_path, "w") as outfile:
        outfile.write("[]")

def SearchRushName(database_path, name):
    # search if rush name already exist 
    conn = sqlite3.connect(database_path)
    c = conn.cursor()  
    rush_name = c.execute("SELECT name FROM rush WHERE name = ?", (name,)).fetchone()  
    return rush_name

def GetNotAchievedRush(database_path):
    # search if rush name already exist 
    conn = sqlite3.connect(database_path)
    c = conn.cursor()  
    rush_notachieved_list = c.execute("SELECT name FROM rush WHERE achieved = ?", (False,)).fetchall()  
    return rush_notachieved_list

def GetAllRush(database_path):
    # search if rush name already exist 
    conn = sqlite3.connect(database_path)
    c = conn.cursor()  
    rush_list = c.execute("SELECT name FROM rush").fetchall()  
    return rush_list


def GetAllTasks(database_path):
    pass
