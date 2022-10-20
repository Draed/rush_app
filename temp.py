

# ===========================
# Condition thread testing 

# c = threading.Condition()
# c.acquire()

# def countdown ():
#     c.acquire()
#     print('start countdown')
#     duration_in_sec = 8
#     while duration_in_sec:
#         print(duration_in_sec, "\r")
#         time.sleep(1)
#         duration_in_sec -= 1
        
#     else:
#         c.notify()
#         c.release()
#     print('The timer has finish') 
    
# def question():
#     c.acquire()
#     time.sleep(2)
#     print("ending rush right now")
#     c.notify()
#     c.release
  
# t1 = threading.Thread(target = countdown)
# t2 = threading.Thread(target = question)
# t1.start()
# t2.start()
# # wait for the countdown to end or question
# c.wait()

# print("wait for the countdown to stop ... ")

# c.release()




# ===========================
# event thread testing

# def countdown(stop_event):
#     print('start countdown')
#     duration_in_sec = 8
#     while duration_in_sec and (not stop_event.is_set()):
#         print(duration_in_sec, "\r")
#         time.sleep(1)
#         duration_in_sec -= 1

# def endQuestion(stop_event):
#     print("This Thread will kill countdown is 2 second")
#     time.sleep(2)
#     print("ending rush right now")
#     stop_event.set()

# print("Stop event is set as False by default")
# stop_event = threading.Event()
# print(stop_event.is_set())

# print("\n")

# t1 = threading.Thread(target = countdown, args = (stop_event,))
# t2 = threading.Thread(target = endQuestion, args = (stop_event,))

# print("Starting countdown")
# t1.start()
# print("Starting EndQuestion")
# t2.start()


# print("waiting for EndQuestion to end")
# t2.join()

# print("Programm ended")

# ===========================
# datetime duration calcul with strftime
# start_pause_dateTime = dt.now()
# start_pause_dateTime_str = start_pause_dateTime.strftime('%H:%M:%S')
# time.sleep(2)
# end_pause_dateTime = dt.now()
# end_pause_dateTime_str = end_pause_dateTime.strftime('%H:%M:%S')

# final_duration = end_pause_dateTime - start_pause_dateTime
# print(dt.now().day)



# ===========================
# testing pdf report generation with xhtml2pdf

# from xhtml2pdf import pisa 


# # Define your data
# output_filename = "output/reports/test.pdf"
# html_template = "ressources/templates/main.html"

# def create_pdf_report(template, output_filename):
#     # Reading our template
#     source_html = open(template, "r")
#     content = source_html.read() # the HTML to convert
#     source_html.close() # close template file

#     html_to_pdf(content, output_filename)

# # Utility function
# def convert_html_to_pdf(source_html, output_filename):
#     # Reading our template
#     source_html = open(template, "r")
#     content = source_html.read() # the HTML to convert
#     source_html.close() # close template file

#     html_to_pdf(content, output)

#     # open output file for writing (truncated binary)
#     result_file = open(output_filename, "w+b")

#     # convert HTML to PDF
#     pisa_status = pisa.CreatePDF(
#             source_html,                # the HTML to convert
#             dest=result_file)           # file handle to recieve result

#     # close output file
#     result_file.close()                 # close output file

#     # return False on success and True on errors
#     return pisa_status.err


# import threading
# import time
import datetime 
from dominate.tags import *
from utils import parse_time
import matplotlib.pyplot as plt
import json
import dominate
import sqlite3
import pdfkit
import math


def create_timeline(rush_data,settings):

    database_path = settings['database_path']
    rush_id = str(rush_data[0])
    conn = sqlite3.connect(database_path)
    timeline_ordered_list = []
    
    c = conn.cursor() 
    ## rush data
    rush_data = c.execute('SELECT * FROM rush WHERE id=?;', (rush_id)).fetchone()
    start_time = rush_data[7]
    start_event = {
        "time" : start_time,
        "title" : "Rush start",
        "description" : "",
    }
    timeline_ordered_list.append(start_event)
    end_time = rush_data[8]
    end_event = {
        "time" : end_time,
        "title" : "Rush end",
        "description" : "",
    }
    timeline_ordered_list.append(end_event)
    meeting_list = c.execute('SELECT * FROM meeting WHERE rush=?;', (rush_id)).fetchall()
    meeting_list = list(map(lambda data: {"time" : data[2], "title" : "meeting", "description" : data[1]},meeting_list))
    timeline_ordered_list.extend(meeting_list)
    pause_list = c.execute('SELECT * FROM pause WHERE rush=?;', (rush_id)).fetchall()
    pause_list = list(map(lambda data: {"time" : data[2], "title" : "pause", "description" : data[1]}, pause_list))
    timeline_ordered_list.extend(pause_list)
    # event_list = c.execute('SELECT pause.rush as rush1, meeting.rush as rush2, reason, start_time, description, time FROM pause JOIN meeting ON pause.rush=meeting.rush WHERE rush1=? GROUP BY rush1 ORDER BY start_time ;', (rush_id)).fetchall()
    conn.commit()
    conn.close()

    timeline_ordered_list.sort(key = lambda date: datetime.datetime.strptime(date['time'], '%Y-%m-%d %H:%M:%S.%f'))

    return timeline_ordered_list

def create_html_report(rush_data, settings):

    # get data from settings
    database_path = settings['database_path']
    user = settings['user']

    # get data from database
    conn = sqlite3.connect(database_path)
    c = conn.cursor()        
    rush_id = str(rush_data['id'])
    ## rush data
    rush_data = c.execute('SELECT * FROM rush WHERE id=?;', (rush_id)).fetchone()
    ## task data
    task_list = c.execute('SELECT * FROM task WHERE rush=?;', (rush_id)).fetchall()
    achieved_task_number = c.execute("SELECT COUNT(achieved) FROM task WHERE rush=? AND achieved=?", (rush_id, True)).fetchone()
    not_achieved_task_number = c.execute("SELECT COUNT(achieved) FROM task WHERE rush=? AND achieved=?", (rush_id, False)).fetchone()
    total_task_number = c.execute("SELECT COUNT(achieved) FROM task WHERE rush=?", (rush_id)).fetchone()
    total_task_time = datetime.timedelta(seconds=0)

    for task in task_list:
        # get the total time with all task : 
        total_task_time += parse_time(task[3])

    total_task_time = total_task_time.total_seconds()// 60
    ## pause data
    pause_list = c.execute('SELECT * FROM pause WHERE rush=?;', (rush_id)).fetchall()
    total_pause_time = datetime.timedelta(seconds=0)
    for pause in pause_list:
        total_pause_time += parse_time(pause[4])
    total_pause_time = total_pause_time.total_seconds()// 60

    ## aar data
    aar_data = c.execute('SELECT * FROM aar WHERE rush=?;', (rush_id)).fetchone()

    ## duration data :
    # rush

    conn.commit()
    conn.close()

    timeline_ordered_list = create_timeline(rush_data,settings)

    # creating plot / graphs :
    graph_colors = ["#04aa6d","#aa0441", "#025f3d", "#03784d", "#03915d", "#04aa6d", "#05c37d", "#05dc8d", "#06f59d"]
    # Graph 1 : achieved task graph
    plt.figure(figsize=(6, 2))
    # subplot 1 : task achieved bar
    task_achieved_name = ['achieved task', 'unachieved task']
    task_achieved_name_value = [achieved_task_number[0], not_achieved_task_number[0]]
    plt.subplot(121)
    plt.pie(task_achieved_name_value, labels=task_achieved_name, colors=graph_colors, rotatelabels=True, wedgeprops = {'linewidth': 3})
    # subplot 2 : time managing
    time_value = [total_task_time, total_pause_time]
    print(time_value)
    time_label = ["work time", "pause time"]
    plt.subplot(122)
    plt.pie(time_value, labels=time_label, colors=graph_colors, rotatelabels=True, wedgeprops = {'linewidth': 3})

    # Graph 3 : Average time (duration) per task
    
    # plt.subplot(133)
    # plt.plot(names, values)
    # plt.suptitle('Task Charts')
    plt.savefig('output/plots/test.png')
    

    doc = dominate.document(title='Rush report : ' + rush_data[1])
    timeline_page = dominate.document()
    date = datetime.datetime.now()
    date = date.strftime('%d-%b-%Y')

    # page 1
    with doc.head:
        style("""
            body {
                font-family: Helvetica, Arial, sans-serif;
            }

            #header a {line-height: 1.8;}

            .container {position: relative;}

            #task_table {
                font-family: Helvetica, Arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }

            #task_table td, #task_table th {
                border: 1px solid #ddd;
                padding: 8px;
            }

            #task_table tr:nth-child(even){background-color: #f2f2f2;}

            #task_table tr:hover {background-color: #ddd;}

            #task_table th {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #04AA6D;
            color: white;
            }

            """)

    with doc:
        with div(id="pdf_header", cls="l-content"):
            with div(id="header", style="padding: 1%; color: white; background: #04AA6D; border: 1px solid #ddd; border-radius: 4px;"):
                with div(id="header-center", cls="", style="width: 100%; display: inline-block;"):
                    h1("Report for rush : " + rush_data[1])
                with div(id="header-left", cls="", style="display: inline-block; width: 65%;"):
                    b("Tag : ")
                    a(rush_data[4])
                    br()
                    b("Type : ")
                    a(rush_data[3])
                    br()
                    b("Estimated duration : ")
                    a(rush_data[5])
                with div(id="header-right", cls="", style="display: inline-block; width: 34%;"):
                    b("Start at : ")
                    a(rush_data[7])
                    br()
                    b("End at : ")
                    a(rush_data[8])
                    br()
                    b("Duration : ")
                    a(rush_data[9])
        with div(id="pdf_centent", cls="l-content"):
            with div(id="description", cls="description"):
                with div(cls=""):
                    h3("Description : ", cls="description-head")
                    p(rush_data[2], style="display: inline-block; width: 99%;")
            with div(id="graph", cls="graph pure-g"):
                with div(cls="pure-u-1"):
                    h3("Graphs : ", cls="graphs-head")
                with div(cls="pure-u-1-2", style="width:45%; display: inline-block;"):
                    # with div(cls="l-box"):
                    img(src="/Users/dreadper/Git/1_Private_work/1_1_my_tools/rush_app/output/plots/test.png", width="1000px", height="350px")
            with div(id="tasks", cls="tasks pure-g"):
                with div(cls="pure-u-1"):
                    h3("Tasks :", cls="tasks-head")
                    with table(id="task_table", cls="pure-table"):
                        with thead():
                            with tr():
                                th("Task name")
                                th("Description")
                                th("Estimated duration ")
                                th("Real duration")
                        with tbody():
                            for task in task_list:
                                with tr(cls="pure-table-odd"):
                                    td(task[1])
                                    td(task[2])
                                    td(task[3])
                                    td(task[4])

    # page 2
    with timeline_page.head:
        style("""
            * {
            box-sizing: border-box;
            }

            body {
                font-family: Helvetica, Arial, sans-serif;
            }

            /* The actual timeline (the vertical ruler) */
            .timeline {
            position: relative;
            width: 6px;
            margin: 0 43%;
            }

            /* The actual timeline (the vertical ruler) */
            .timeline::after {
            content: '';
            position: absolute;
            width: 6px;
            background-color: #04AA6D;
            top: 0;
            bottom: 0;
            margin-left: -3px;
            }

            /* Container around content */
            .container {
            padding: 20px 20px;
            position: relative;
            background-color: inherit;
            width: 100%;
            }

            /* The circles on the timeline */
            .container::after {
            content: '';
            position: absolute;
            width: 25px;
            height: 25px;
            right: -17px;
            background-color: white;
            border: 4px solid lightgray;
            top: 15px;
            border-radius: 50%;
            z-index: 1;
            }

            /* Fix the circle for containers on the right side */
            .right::after {
            left: -16px;
            }

            /* The actual content */
            .content {
            padding: 1px 1px;
            background-color: white;
            position: relative;
            width: 300px;
            border-radius: 6px;
            }

            .timeline::after {
                left: 32px;
            }

            /* Full-width containers */
            .container {
                width: 100%;
                padding-left: 60px;
                padding-right: 25px;
            }


            /* Make sure all circles are at the same spot */
            .left::after, .right::after {
                left: 14px;
            }

            .time {
                font-size: 11px;
                margin-top: -16px;
            }

        """)

    with timeline_page :
        with div(id="content"):
            h3("Timeline : ", cls="timeline-head")
            with div(id="timeline", cls="timeline"):
                with div():
                    with div(cls="timeline"):
                        for event in timeline_ordered_list:
                            with div(cls="container right"):
                                with div(cls="content"):
                                    h3(event["title"])
                                    div(event["time"], cls="time")
                                    p(event["description"])
            
            if aar_data:
                with div(id="AAR"):
                    h3("After Action Report (AAR) : ", cls="timeline-head")
                    p(aar_data, style="display: inline-block; width: 99%;")

    # write result to html file
    report_path1 = "output/reports/html/report_" + rush_id + "_" + date +"p1.html"
    report_path2 = "output/reports/html/report_" + rush_id + "_" + date +"p2.html"
    page1 = open(report_path1, "w")
    page1.write((str(doc)))
    page2 = open(report_path2, "w")
    page2.write((str(timeline_page)))
    report_path = [report_path1, report_path2]

    return report_path

def convert_html_to_pdf(rush_data, report_path):
    rush_id = str(rush_data['id'])
    date = datetime.datetime.now()
    date = date.strftime('%d-%b-%Y')
    pdf_report_path = "output/reports/pdf/report_" + rush_id + "_" + date +".pdf"    
    pdfkit.from_file(report_path, pdf_report_path, {'enable-local-file-access': True})


if __name__ == "__main__":
    
    # load setting data
    f = open('ressources/rush_settings.json')
    settings = json.load(f)
    f.close()

    rush_data = {"id" : 3}

    report_path = create_html_report(rush_data, settings)
    convert_html_to_pdf(rush_data, report_path)
    
