# Rush app

## Description

A terminal (pyton) app for managing rush (my IT challenge limited in time).

## Features 

### TODO : 

<!-- - make the endtime equal to rush endtime if not "end this rush right now" -->

- add start_time for task
- add end_time for task
- add a currently working on task automatically to count time on it

- graph achieved task per hour

- generate global report for all rush : 
    - features and tasks accomplish 
    - number : 
        - total rush
    - graphs : 
        - by tags
        - by duration

### DONE : 

- add a regex validation for dates format (00:00:00)

- adding question for repo path at the end

- push last rush pdf report to rush repo

- add an option 'show me data' which show :
    - rush start time
    - rush time available
    - estimated rush end time
    - last pause (was for "name" at 'time')
    - ration : task done / total task

- change the end all task have been done

- generate pdf report for each rush : 
    - estimated time
    - duration
    - starttime
    - endtime
    - datetime (day)
    - tag
    - type
    - task list with infos
    - show the aar

- AAR (After Action Report) :
    - question : "would you like to write an AAR ?
    - advice in yellow : "How was this session, efficient , productive ?"
    - (if yes) just a text
- (if rush type not learning) scrum meeting question : 
    - Are you late ?
    - (if yes) why ?
    - Is it possible to make up for lost time ?
    - (if yes) How ?
- Pause feature to add : 
    - add choice "make a pause" 
- notifier for pause,coffee,physical activity, advancement report
- store each rush data on sqlite database
- scrum meeting feature
- add a notification at the end 


### Backlogs : 
- Tester le temp de concentration nécessaire 
Exemple de situation de rush : 
- test de situation de fatigue : dans un rush au bout de 12 heure de travail mesurer les performances (comment ? tâches , avancement ...)
- test de stress en situation de fatigue : dans un rush au bout de 6h, changer les priorités des tâches, analyser la réponse

idées de niveau de rush : 
- Facile : 24h, pas de restrictions
- Moyen : 12h, changement des priorités aléatoirement
- Difficile : 6h, incident aléatoire, changement des priorités aléatoirement
- hardcore : 6h, coupure internet, incident aléatoire, changement des priorités aléatoirement

## sources : 

- pdf report with python : https://plotly.com/python/v3/pdf-reports/