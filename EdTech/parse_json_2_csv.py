'''
Created on Sep 10, 2015

@author: HCH
'''
import csv
import json


def json2csv(json_file_name, csv_file_name):
    json_file = open(json_file_name) 
    data = json.load(json_file) 
    f = csv.writer(open(csv_file_name, "w", encoding='utf8'), delimiter=',', lineterminator='\n')
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
    
    # convert a overall data
    file_json = 'json_data/anonymous-student-events7.json'
    file_csv = 'raw/student_raw7.csv'
    json2csv(file_json, file_csv)
