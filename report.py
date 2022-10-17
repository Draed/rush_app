import os
import shutil
import numpy as np
import pandas as pd
import calendar
import sqlite3
from datetime import datetime
from fpdf import FPDF

import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False

def generate_pdf(database_path):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    # filter by duration
    #rowsQuery = "select duration,count(duration) from rush group by duration"
    # filter by tag
    
    count_tag_list_query = "select count(tag) from rush group by tag"
    c.execute(count_tag_list_query)
    count_tag_list = c.fetchall()
    count_tag_list = list(map(lambda x: x[0], count_tag_list))

    tag_list_query = "select tag from rush group by tag"
    c.execute(tag_list_query)
    tag_list = c.fetchall()
    tag_list = list(map(lambda x: x[0], tag_list))

    conn.close()

    # plot
    # defining labels
    activities = tag_list
    
    # portion covered by each label
    slices = count_tag_list
    
    # color for each label
    colors = ['r', 'y', 'g', 'b']
    
    # plotting the pie chart
    plt.pie(slices, labels = activities, colors=colors, 
            startangle=90, shadow = True,
            radius = 1.2, autopct = '%1.1f%%')
    
    # plotting legend
    plt.legend()
    plt.savefig("plots/pie_tag.png", dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()

    # pdf
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Hello World!')
    pdf.image("plots/pie_tag.png", 15, 25)
    pdf.output('reports/tuto1.pdf', 'F')


# def generate_sales_data(month: int) -> pd.DataFrame:
#     # Date range from first day of month until last
#     # Use ```calendar.monthrange(year, month)``` to get the last date
#     dates = pd.date_range(
#         start=datetime(year=2020, month=month, day=1),
#         end=datetime(year=2020, month=month, day=calendar.monthrange(2020, month)[1])
#     )
    
#     # Sales numbers as a random integer between 1000 and 2000
#     sales = np.random.randint(low=1000, high=2000, size=len(dates))
    
#     # Combine into a single dataframe
#     return pd.DataFrame({
#         'Date': dates,
#         'ItemsSold': sales
#     })

# def plot(data: pd.DataFrame, filename: str) -> None:
#     plt.figure(figsize=(12, 4))
#     plt.grid(color='#F2F2F2', alpha=1, zorder=0)
#     plt.plot(data['Date'], data['ItemsSold'], color='#087E8B', lw=3, zorder=5)
#     plt.title(f'Sales 2020/{data["Date"].dt.month[0]}', fontsize=17)
#     plt.xlabel('Period', fontsize=13)
#     plt.xticks(fontsize=9)
#     plt.ylabel('Number of items sold', fontsize=13)
#     plt.yticks(fontsize=9)
#     plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
#     plt.close()
#     return

# PLOT_DIR = 'plots'

# def construct():
#     # Delete folder if exists and create it again
#     try:
#         shutil.rmtree(PLOT_DIR)
#         os.mkdir(PLOT_DIR)
#     except FileNotFoundError:
#         os.mkdir(PLOT_DIR)
        
#     for i in range(2, 5):
#         # Save visualization
#         plot(data=generate_sales_data(month=i), filename=f'{PLOT_DIR}/{i}.png')
        
#     # Construct data shown in document
#     counter = 0
#     pages_data = []
#     temp = []
#     # Get all plots
#     files = os.listdir(PLOT_DIR)
#     # Sort them by month - a bit tricky because the file names are strings
#     files = sorted(os.listdir(PLOT_DIR), key=lambda x: int(x.split('.')[0]))
#     # Iterate over all created visualization
#     for fname in files:
#         # We want 3 per page
#         if counter == 3:
#             pages_data.append(temp)
#             temp = []
#             counter = 0

#         temp.append(f'{PLOT_DIR}/{fname}')
#         counter += 1

#     return [*pages_data, temp]


# class PDF(FPDF):
#     def __init__(self):
#         super().__init__()
#         self.WIDTH = 210
#         self.HEIGHT = 297
        
#     def header(self):
#         # Custom logo and positioning
#         # Create an `assets` folder and put any wide and short image inside
#         # Name the image `logo.png`
#         self.image('ressources/assets/logo.png', 10, 8, 33)
#         self.set_font('Arial', 'B', 11)
#         self.cell(self.WIDTH - 80)
#         self.cell(60, 1, 'Sales report', 0, 0, 'R')
#         self.ln(20)
        
#     def footer(self):
#         # Page numbers in the footer
#         self.set_y(-15)
#         self.set_font('Arial', 'I', 8)
#         self.set_text_color(128)
#         self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

#     def page_body(self, images):
#         # Determine how many plots there are per page and set positions
#         # and margins accordingly
#         if len(images) == 3:
#             self.image(images[0], 15, 25, self.WIDTH - 30)
#             self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
#             self.image(images[2], 15, self.WIDTH / 2 + 90, self.WIDTH - 30)
#         elif len(images) == 2:
#             self.image(images[0], 15, 25, self.WIDTH - 30)
#             self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
#         else:
#             self.image(images[0], 15, 25, self.WIDTH - 30)
            
#     def print_page(self, images):
#         # Generates the report
#         self.add_page()
#         self.page_body(images)