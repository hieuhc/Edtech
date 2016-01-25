'''
Created on Sep 10, 2015

@author: HCH
'''
import csv
import json
import re


def json2csv(json_file_name, csv_file_name):
    json_file = open(json_file_name) 
    data = json.load(json_file) 
    f = csv.writer(open(csv_file_name, "w", encoding='utf8'), delimiter = ',', lineterminator='\n')
        
    
    print(len(data))
    properties_all = ['event']
    for x in data:
        properties_all.extend(x['properties'].keys())
    properties_all = set(properties_all)
    print('num of properties: %d' % len(properties_all))
    col_names = [col_na.replace('$', '') for col_na in properties_all]
    f.writerow(col_names)
    for x in data:    
        row_content = []    
        for prop in properties_all:
            item_val = ''
            if prop == 'event':
                item_val = x['event']
            elif prop not in x['properties']:
                item_val = ''
            else:
                item_val = x['properties'][prop]
            row_content.append(item_val)
               
        f.writerow(row_content)
if __name__ == '__main__':
    # convert weekly data
#     student_json = 'data/anonymous-student-events_21-9.json'
#     teacher_json = 'data/anonymous-teacher-events_21-9.json'
#     student_csv = 'data/student_21-9_raw.csv'
#     teacher_csv = 'data/teacher_21-9_raw.csv'
#     json2csv(student_json, student_csv)
#     json2csv(teacher_json, teacher_csv)
    
    # convert a overall data
    teacher_json = 'data/anonymous-teacher.json'
    teacher_csv = 'raw/teacher_raw.csv'
    json2csv(teacher_json, teacher_csv)
     
    
    
    