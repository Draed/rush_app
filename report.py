# import os
# import shutil
# import numpy as np
# import pandas as pd
# import calendar
# import sqlite3
# from datetime import datetime
# from fpdf import FPDF

# import matplotlib.pyplot as plt
# from matplotlib import rcParams

from datetime import datetime as dt
import dominate
from dominate.tags import *

def create_graph_report(rush_data, database_path):
    doc = dominate.document(title='Rush report : ' + rush_data['name'])
    date = dt.now().strftime('%d-%b-%Y')

    # head part of html
    with doc.head:
        link(rel='stylesheet', href='style.css')
        script(type='text/javascript', src='script.js')

    # body part of html
    with doc:
        
        with div(id='header').add(ol()):
            for i in ['home', 'about', 'contact']:
                li(a(i.title(), href='/%s.html' % i))

        with div():
            attr(cls='main_info')
            p("report create at : " + date)

        with div():
            attr(cls='body')
            p('Lorem ipsum..')

    # write result to html file
    report_path = "ressources/templates/report_" + date
    with open(report_path, "w") as file1:
        file1.write(doc)



def create_html_report_file():
    #Dominate
    pass

def convert_html_to_pdf_report_file():
    pass

