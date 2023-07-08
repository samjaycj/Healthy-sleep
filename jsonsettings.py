import json

settings_json = json.dumps([
    {'type': 'title',
     'title': 'Healthy Sleep Settings'},
    {'type': 'numeric',
     'title': 'Time to Fall Asleep',
     'desc': 'Enter time in minutes',
     'section': 'HealthySleep',
     'key': 'timetosleep'},
    {'type': 'options',
     'title': 'Time Format',
     'desc': 'Enter Time format to display',
     'section': 'HealthySleep',
     'key': 'timeformat',
     'options': ['24H', '12H']}])