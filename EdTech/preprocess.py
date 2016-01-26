'''
Created on Sep 11, 2015

@author: HCH
'''
import pandas as pd
import pytz
from datetime import datetime
import  re
from EdTech import parse_json_2_csv

# 55caf449a9fa340800ae192b
# 55caf449a9fa340800ae192c
# 55caf449a9fa340800ae192d


def process_url(url):
    if '56936bb72bea66f99e5af2a6' in url:
        return 'KLS3551 Kulturledelse'
    elif '569384db2bea66f99e5af2e7' in url:
        return 'MRK3480 Forbrukeratferd'
    elif '56936bd32bea66f99e5af2a7' in url:
        return 'ORG3402 Organisasjonsatferd og ledelse'
    else:
        return ''


def process_time(epoch):
    #   human_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))
    tz = pytz.timezone('Europe/Oslo')
    dt = datetime.fromtimestamp(epoch, tz)   
    human_time = dt.strftime('%Y-%m-%d %H:%M:%S') 
    return human_time


def get_topic_screen(event_string):
    assert 'topics' in event_string, 'event: %s does not contain topics' % event_string
    if '//' in event_string:
        topic = 'all topics'
        event_tail = re.split(' ', re.split('//', event_string)[1])[0]
        screen = re.split('/', event_tail)[0]
        '''
        TO DO: feed/findOne Page and contents/view Page
        '''
    else:
        path = re.split(' ', event_string)[1]
        path_comp = re.split('/', path)
        topic, screen = path_comp[4], path_comp[5]

        '''
        TO DO: feed/findOne Page and contents/view Page
        '''
    if screen == 'contents':
        screen = 'content'
    return topic, screen


def process_event(event_string):
    if 'Viewed space' in event_string:
        event_1, topic, screen = 'Viewed space', '', ''
    elif '/topics/' in event_string:
        topic, screen = get_topic_screen(event_string)
        if screen == 'feed':
            event_1 = 'Viewed feed screen'
        else:  # screen == 'content'
            event_1 = 'Viewed content screen'

        '''
        TO DO: feed/findOne Page and contents/view Page
        '''
    else:
        '''
        TO DO: extract topic and screen Page in e.g, 'Viewed content'
        '''
        event_1, topic, screen = event_string, '', ''
    return event_1, topic, screen


def pre_process_data(data):
    data['time_1'] = data.time.map(lambda x: process_time(x))
    for row_idx in range(data.shape[0]):
        event_crr = data.event[row_idx]
        event_1, topic, screen = process_event(event_crr)
        data.ix[row_idx, 'event_1'], data.ix[row_idx, 'topic'], data.ix[row_idx, 'screen'] = event_1, topic, screen
    print(data.shape)
#     create space name column
    data['space_1'] = data.current_url.map(lambda x: process_url(x))
    print(data.shape)
    return data


def process_overlap(data_1, data_2):
    time_end_1 = data_1.time[data_1.shape[0] - 1]
    for idx in range(data_2.shape[0]):
        if data_2.time[idx] > time_end_1:
            idx_to_del = idx
            break
    print(data_2.shape)
    data_2_new = data_2.drop(range(idx_to_del), axis=0)
    print(data_2_new.shape)
    data = pd.concat([data_1, data_2_new], ignore_index=True)
    return data


def weekly2all(data_overall_processed_file, data_overall_raw_file, data_weekly_json, data_weekly_raw_file):
    parse_json_2_csv.json2csv(data_weekly_json, data_weekly_raw_file)
    data_weekly_raw = pd.read_csv(data_weekly_raw_file, encoding='utf8')
    data_overall_raw = pd.read_csv(data_overall_raw_file, encoding='utf8')
    data_raw = process_overlap(data_overall_raw, data_weekly_raw)
    print(data_raw.shape)   
    data_raw = pd.DataFrame(data_raw.drop_duplicates().values, columns=data_raw.columns)
    print(data_raw.shape)
    data_processed = pre_process_data(data_raw)
                 
    data_raw.to_csv(data_overall_raw_file, index=False, encoding='utf8')
    data_processed.to_csv(data_overall_processed_file, index=False, encoding='utf8')


def main_old():
    # add weekly data to the current overall data
    #     weekly2all('teacher.csv','raw/teacher_raw.csv','data/anonymous-teacher-events_1-12.json', 'raw/teacher_1-12_raw.csv')
    #     weekly2all('student.csv','raw/student_raw.csv','data/anonymous-student-events_1-12.json', 'raw/student_1-12_raw.csv')

    # pre_process all data
    # teacher
    parse_json_2_csv.json2csv('data/anonymous-teacher-events.json', 'raw/teacher_raw.csv')
    data_raw = pd.read_csv('raw/teacher_raw.csv')
    data = pre_process_data(data_raw)
    data.to_csv('teacher.csv', index=False, encoding='utf8')
    # student
    parse_json_2_csv.json2csv('data/anonymous-student-events.json', 'raw/student_raw.csv')
    data_raw = pd.read_csv('raw/student_raw.csv')    
    data = pre_process_data(data_raw)
    data.to_csv('student.csv', index=False, encoding='utf8')

if __name__ == '__main__':
    data_raw = pd.read_csv('raw/student_raw.csv')
    data_processed = pre_process_data(data_raw)
    data_processed.to_csv('data/student.csv', index=False, encoding='utf8')