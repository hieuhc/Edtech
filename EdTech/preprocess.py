'''
Created on Sep 11, 2015

@author: HCH
'''
import pandas as pd
import pytz
from datetime import datetime
import re
from EdTech import parse_json_2_csv, Constant
import numpy as np


# 55caf449a9fa340800ae192b
# 55caf449a9fa340800ae192c
# 55caf449a9fa340800ae192d


def get_space_name(url, event):
    for course_id in Constant.ID_COURSE_DICT.keys():
        if course_id in (url + event):
            return Constant.ID_COURSE_DICT[course_id]
    return ''


def process_time(epoch):
    #   human_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))
    tz = pytz.timezone('Europe/Oslo')
    dt = datetime.fromtimestamp(epoch, tz)   
    human_time = dt.strftime('%Y-%m-%d %H:%M:%S') 
    return human_time


def get_topic_screen(event_topic_string):
    assert 'topics' in event_topic_string, 'event: %s does not contain topics' % event_topic_string
    if '//' in event_topic_string:
        topic = 'all'
        event_tail = re.split(' ', re.split('//', event_topic_string)[1])[0]
        screen = re.split('/', event_tail)[0]
    else:
        path = re.split(' ', event_topic_string)[1]
        path_comp = re.split('/', path)
        topic, screen = path_comp[4], path_comp[5]

    if screen == 'contents':
        screen = 'content'
    return topic, screen


def process_event(event_string, current_url):
    if 'Viewed space' in event_string:
        event_1, topic, screen = 'Viewed space', '', ''
    elif '/topics/' in event_string:
        topic, screen = get_topic_screen(event_string)
        if screen == 'feed':
            if 'findOne' in event_string:
                event_1 = 'Viewed feed/findOne'
            elif ('/topics//' in event_string) or ('/topics/all') in event_string:
                event_1 = 'Viewed feed/all'
            else:
                event_1 = 'Viewed feed/topic'
        else:  # screen == 'content'
            if ('/topics//' in event_string) or ('/topics/all' in event_string):
                event_1 = 'Viewed content/all'
            else:
                event_1 = 'Viewed content/topic'

    else:
        '''extract topic and screen Page in e.g, 'Viewed content' '''
        event_1 = event_string
        if '/topics//' in current_url:
            topic = 'all'
            screen = re.split('/', current_url)[7]
        elif '/topics/' in current_url:
            eles = re.split('/', current_url)
            topic, screen = eles[6], eles[7]
        else:
            topic, screen = '', ''
        if screen == 'contents':
            screen = 'content'
    return event_1, topic, screen


def pre_process_data(data):
    data['time_1'] = data.time.map(lambda x: process_time(x))
    #     create space name column
    for row_idx in range(data.shape[0]):
        event_crr, current_url = data.event[row_idx], data.current_url[row_idx]
        event_1, topic, screen = process_event(event_crr, current_url)
        data.ix[row_idx, 'event_1'], data.ix[row_idx, 'topic'], data.ix[row_idx, 'screen'] = event_1, topic, screen
        data.ix[row_idx, 'space_1'] = get_space_name(data.ix[row_idx, 'current_url'], data.ix[row_idx, 'event'])

    return data


def process_overlap(data_1, data_2):
    # time_end_1 = data_1.time[data_1.shape[0] - 1]
    # for idx in range(data_2.shape[0]):
    #     if data_2.time[idx] > time_end_1:
    #         idx_to_del = idx
    #         break
    # data_2_new = data_2.drop(range(idx_to_del), axis=0)
    data = pd.concat([data_1, data_2], ignore_index=True)
    return data


def weekly2all(data_file, data_weekly_json_file):
    parse_json_2_csv.json2csv(data_weekly_json_file, 'data/raw/temp.csv')
    data_weekly_raw = pd.read_csv('data/raw/temp.csv', encoding='utf8')
    data_weekly_processed = pre_process_data(data_weekly_raw)
    print('this week: %s' % str(data_weekly_processed.shape))
    data_processed = pd.read_csv(data_file, encoding='utf8')
    data = process_overlap(data_processed, data_weekly_processed)
    print('total: %s' % str(data.shape))
    data.to_csv(data_file, index=False, encoding='utf8')


def export_content_id_map(student_data_file, teacher_data_file, content_map_file):
    student_data = pd.read_csv(student_data_file, encoding='utf8')
    teacher_data = pd.read_csv(teacher_data_file, encoding='utf8')
    data = pd.concat([student_data, teacher_data], ignore_index=True)
    print(data.shape); print(teacher_data.shape); print(data.shape)
    content_name, content_id, course = [], [], []
    for row_idx in range(data.shape[0]):
        if (data.event_1[row_idx] == 'Viewed content') and (data.contentType[row_idx] == 'file'):
            if data.contentName[row_idx] not in content_name:
                content_name.append(data.contentName[row_idx])
                content_id.append(data.contentId[row_idx])
                course.append(data.space_1[row_idx])
    df = pd.DataFrame(np.vstack([content_id, content_name, course]).T, columns=['contentId', 'contentName', 'space_1'])
    df.to_csv(content_map_file, index=False, header=True)


def recover_data_file(indicator):
    data_init_file = 'data/json_data/anonymous-' + indicator + '-events.json'
    data_file = 'data/data/' + indicator + '.csv'
    parse_json_2_csv.json2csv(data_init_file, 'data/raw/temp.csv')
    data_init_raw = pd.read_csv('data/raw/temp.csv', encoding='utf8')
    data_init_processed = pre_process_data(data_init_raw)
    print(data_init_processed.shape)
    data_init_processed.to_csv(data_file, index=False, encoding='utf8')

if __name__ == '__main__':
    # first data.csv
    # recover_data_file('teacher')

    # add weekly data to the current overall data
    # weekly2all('data/data/teacher.csv', 'data/json_data/anonymous-teacher-events6.json')
    # weekly2all('data/data/student.csv', 'data/json_data/anonymous-student-events7.json')
    # export_content_id_map('data/data/student.csv', 'data/data/teacher.csv', 'data/data/content_id_map.csv')

    # data = pd.read_csv('raw/student_raw2.csv')
    # event_url = {data.event.values[idx]: data.current_url[idx] for idx in range(data.shape[0])}
    # known = list(Constant.ID_COURSE_DICT.keys())
    # urls = set(data.current_url.values)
    # for url in urls:
    #     if not any(k in url for k in known):
    #         print(url)
    #
    # ids = set(data.currentSpaceId.values)
    # for id in ids:
    #     print(id)

    data = pd.read_csv('data/data/student.csv')
    courses = Constant.ID_COURSE_DICT.values()
    for course in courses:
        std = data[data.space_1 == course].distinct_id.values
        print('%s: %d' % (course, len(set(std))))