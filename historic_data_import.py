import json, sqlite3

if __name__ == "__main__":
    """
    importing old rush or project into my "rush_app"
    and generating report 
    """

    # load setting data
    f = open('ressources/rush_settings.json')
    settings = json.load(f)
    f.close()
    database_path = settings['database_path']

    # test using context manager instead of classic try, except
    with sqlite3.connect(database_path) as conn:
        c = conn.cursor()
        achieved_rush = c.execute("SELECT * FROM rush WHERE achieved = ?", (True,)).fetchall()
    
    # get all rush id with list comprehension instead of classic list
    achieved_rush_id_list = []
    achieved_rush_id_list = [ achieved_rush_id_list.append(achieved_rush[i][0]) for i,v in enumerate(achieved_rush) ]

    # for all ended rush  generate report
    for rush_id in achieved_rush_id_list :
        report_path = create_html_report(rush_data, settings)
        convert_html_to_pdf(rush_data, report_path)

    # # rush_data = {"id" : 3}

    
    

    # path = "output/reports/pdf/report_4_21-Oct-2022.pdf"