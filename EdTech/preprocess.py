'''
Created on Sep 11, 2015

@author: HCH
'''
import pandas as pd
import pytz
from datetime import datetime
from collections import Counter
from EdTech import parse_json_2_csv

# 55caf449a9fa340800ae192b
# 55caf449a9fa340800ae192c
# 55caf449a9fa340800ae192d


def process_url(url):
    if 'https://learn.bi.no/spaces/55caf449a9fa340800ae192b' in url:
        return 'Kulturledelse KLS3551'
    elif 'https://learn.bi.no/spaces/55caf449a9fa340800ae192c' in url:
        return 'Strategi STR3605'
    elif 'https://learn.bi.no/spaces/55caf449a9fa340800ae192d' in url:
        return 'Entrepreneurship ELE3702'
    else:
        return ''


def process_time(epoch):
    #   human_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))
    tz = pytz.timezone('Europe/Oslo')
    dt = datetime.fromtimestamp(epoch, tz)   
    human_time = dt.strftime('%Y-%m-%d %H:%M:%S') 
    return human_time


def process_event(event_name):
    if 'Viewed content' in event_name:
        return 'Viewed content'
    if 'Deleted' in event_name and 'content' in event_name:
        return 'Deleted content'
    if 'Viewed folder' in event_name:
        return 'Viewed folder'
    if 'Viewed link' in event_name:
        return 'Viewed link'
    if 'Viewed space' in event_name:
        return 'Viewed space'
    else:
        return event_name


def preprocess_data(data):    
    data['event_1'] = data.event.map(lambda x : process_event(x))    
    data['time_1']= data.time.map(lambda x : process_time(x))    
    for idx in range(data.shape[0]):
        if str(data.name[idx]) != 'nan':
            data.ix[idx,'contentName_2'] = data.name[idx]
        elif str(data.contentName[idx]) != 'nan':
            data.ix[idx,'contentName_2'] = data.contentName[idx]
        else:
            data.ix[idx,'contentName_2'] = data.name[idx]
    print('done contentName_2 creation')
    print(data.shape)
    row_drop = []
#     remove 'spaces' in event
    spaces_rows = [idx for idx in range(data.shape[0]) if 'spaces' in data.event[idx]]
    row_drop.extend(spaces_rows)
#     remove bot user    
    row_bots = [idx for idx in range(data.shape[0]) if data.distinct_id[idx] == '55caf449a9fa340800ae1929']
    row_drop.extend(row_bots)    
#     remove userid with hyphen
    hyphen_users = [idx for idx in range(data.shape[0]) if '-' in str(data.distinct_id[idx])]
    row_drop.extend(hyphen_users)    
#     remove userid with only numbers/short len
    short_id_users = [idx for idx in range(data.shape[0]) if len(str(data.distinct_id[idx])) != 24]
    row_drop.extend(short_id_users)    
#     create space name column
    data['space_1'] = data.current_url.map(lambda x : process_url(x))
    data = data.drop(row_drop, axis= 0)
    print(data.shape)
#     data.to_csv(data_to, index = False, encoding = 'utf8')
    return data


def process_overlap(data_1, data_2):
    time_end_1 = data_1.time[data_1.shape[0] - 1]
    for idx in range(data_2.shape[0]):
        if data_2.time[idx] > time_end_1:
            idx_to_del = idx
            break
    print(data_2.shape)
    data_2_new = data_2.drop(range(idx_to_del), axis = 0)
    print(data_2_new.shape)
    data = pd.concat([data_1, data_2_new], ignore_index= True)
    return data


def weekly2all(data_overall_processed_file, data_overall_raw_file, data_weekly_json, data_weekly_raw_file):
    parse_json_2_csv.json2csv(data_weekly_json, data_weekly_raw_file)
    data_weekly_raw = pd.read_csv(data_weekly_raw_file, encoding ='utf8')
    data_overall_raw = pd.read_csv(data_overall_raw_file, encoding = 'utf8')
    data_raw = process_overlap(data_overall_raw, data_weekly_raw)
    print(data_raw.shape)   
    data_raw = pd.DataFrame(data_raw.drop_duplicates().values, columns = data_raw.columns)
    print(data_raw.shape)
    data_processed = preprocess_data(data_raw)        
                 
    data_raw.to_csv(data_overall_raw_file, index = False, encoding='utf8')
    data_processed.to_csv(data_overall_processed_file, index = False, encoding = 'utf8')


def main_old():
    # add weekly data to the current overall data
    #     weekly2all('teacher.csv','raw/teacher_raw.csv','data/anonymous-teacher-events_1-12.json', 'raw/teacher_1-12_raw.csv')
    #     weekly2all('student.csv','raw/student_raw.csv','data/anonymous-student-events_1-12.json', 'raw/student_1-12_raw.csv')

    # pre_process all data
    # teacher
    parse_json_2_csv.json2csv('data/anonymous-teacher-events.json', 'raw/teacher_raw.csv')
    data_raw = pd.read_csv('raw/teacher_raw.csv')
    data = preprocess_data(data_raw)
    data.to_csv('teacher.csv', index=False, encoding = 'utf8')
    # student
    parse_json_2_csv.json2csv('data/anonymous-student-events.json', 'raw/student_raw.csv')
    data_raw = pd.read_csv('raw/student_raw.csv')    
    data = preprocess_data(data_raw)
    data.to_csv('student.csv', index=False, encoding = 'utf8')

if __name__ == '__main__':
    data_raw = pd.read_csv('raw/student_raw.csv')
    for event in set(data_raw.event.values):
        print(event)