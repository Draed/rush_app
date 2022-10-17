# Rush app

## Description

A terminal (pyton) app for managing rush (my IT challenge limited in time).

- name
- description
- tags (theme)
- start time
- end time
- duration
- level
- achieved : bool, if goals have been achieved during the time (or not)
- final time : time when goals have been achieved
- tasks

## Features 

- notifier for pause,coffee,physical activity, advancement report
- generate pdf report for each rush
- store each rush data on sqlite database
- generate general report for all rush
- push last rush pdf report to rush repo
- pause button feature
- simuler une réunion "scrum" à interval régulier (toutes les 6 heures) :
    - avancement 
    - retard, raison, temps en retard, possibilité de rattraper
    - changement de plan ? de priorité des tâches, abandon de certaines fonctionnalités
- inclure les pauses (café, eau, effort physique, étirement)
- inclure les heures de repos

- Tester le temp de concentration nécessaire 
Exemple de situation de rush : 
- test de situation de fatigue : dans un rush au bout de 12 heure de travail mesurer les performances (comment ? tâches , avancement ...)
- test de stress en situation de fatigue : dans un rush au bout de 6h, changer les priorités des tâches, analyser la réponse

faire un AAR après chaque rush (12 ou 24 heures après) : afin de voir ce qui à été fait dans les situations de stress et comment corriger les erreurs.

idées de niveau de rush : 
- Facile : 24h, pas de restrictions
- Moyen : 12h, changement des priorités aléatoirement
- Difficile : 6h, incident aléatoire, changement des priorités aléatoirement
- hardcore : 6h, coupure internet, incident aléatoire, changement des priorités aléatoirement

### report : 

- features and tasks accomplish 

- number : 
    - total rush

- graphs : 
    - by tags
    - by duration



## sources : 

- pdf report with python : https://plotly.com/python/v3/pdf-reports/