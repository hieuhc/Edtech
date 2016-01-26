'''
Created on Oct 6, 2015

@author: HCH
'''
import pandas as pd
import numpy as np
import datetime
import csv


def export_weekly_report(date_start, date_end, file_report, aggregate=False):
    std = pd.read_csv('data/student.csv')
    std['date'] = std.time_1.map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').date())
    
    std_w = std[(std.date >= date_start) & (std.date <= date_end)]
    space_name_lst = ['KLS3551 Kulturledelse', 'MRK3480 Forbrukeratferd', 'ORG3402 Organisasjonsatferd og ledelse']
    writer_w = csv.writer(open(file_report, 'w', encoding='utf8'), delimiter=',', lineterminator='\n')
    op_file_all, op_note_all, op_link_all, op_topic_feed_all, op_topic_content_all = [], [], [], [], []
    for space_name in space_name_lst:
        print('---' + space_name)
        std_course = std[std.space_1 == space_name]
        std_w_course = std_w[std_w.space_1 == space_name]
        std_num = len(set(std_course.distinct_id))
        print('num of std: %d' % std_num)
        log_rate = len(set(std_w_course.distinct_id)) / len(set(std_course.distinct_id))
        print('log rate: %f' % log_rate)
        # view file
        std_w_course_content = std_w_course[(std_w_course.event_1 == 'Viewed content') &
                                            (std_w_course.contentType == 'file')]
        temp = std_w_course_content.groupby(['contentName'])['distinct_id'].nunique()
        file_name = list(temp.index) + ['average']
        file_op = temp.values/std_num
        op_file_all.extend(file_op.tolist())
        file_op = np.append(file_op, np.array([np.mean(file_op)]))    
        # view note
        std_w_course_content = std_w_course[(std_w_course.event_1 == 'Viewed content') &
                                            (std_w_course.contentType == 'note')]
        temp = std_w_course_content.groupby(['contentName'])['distinct_id'].nunique()
        note_name = list(temp.index) + ['average']
        note_op = temp.values/std_num
        op_note_all.extend(note_op.tolist())
        note_op = np.append(note_op, np.array([np.mean(note_op)]))
        # view link
        std_w_course_content = std_w_course[std_w_course.event_1 == 'Viewed link']
        temp = std_w_course_content.groupby(['contentName'])['distinct_id'].nunique()
        link_name = list(temp.index) + ['average']
        link_op = temp.values/std_num
        op_link_all.extend(link_op.tolist())
        link_op = np.append(link_op, np.array([np.mean(link_op)]))

        # view topic feed
        std_w_course_topic = std_w_course[std_w_course.event_1 == 'Viewed feed screen']
        temp = std_w_course_topic.groupby(['topic'])['distinct_id'].nunique()
        topic_feed_name = list(temp.index) + ['average']
        topic_feed_op = temp.values/std_num
        op_topic_feed_all.extend(topic_feed_op.tolist())
        topic_feed_op = np.append(topic_feed_op, np.array([np.mean(topic_feed_op)]))

        # view topic content
        std_w_course_topic = std_w_course[std_w_course.event_1 == 'Viewed content screen']
        temp = std_w_course_topic.groupby(['topic'])['distinct_id'].nunique()
        topic_content_name = list(temp.index) + ['average']
        topic_content_op = temp.values/std_num
        op_topic_content_all.extend(topic_content_op.tolist())
        topic_content_op = np.append(topic_content_op, np.array([np.mean(topic_content_op)]))

        # start writing to file
        writer_w.writerow([space_name, '', '', '', '', '', '', '', '', '', '', '', '', ''])
        if not aggregate:
            writer_w.writerow(['logged in rate', str(log_rate), '', '', '', '', '', '', '', '', '', '', '', ''])
        writer_w.writerow(['File', '', '', 'Note', '', '', 'Link', '', '', 'Topic (feed)', '', '', 'Topic (content)', ''
                           ])
        for idx in range(max(len(file_op), len(note_op), len(link_op), len(topic_feed_op), len(topic_content_op))):
            l = ['', '', '', '', '', '', '', '', '', '', '', '', '', '']
            if idx < len(file_op):
                l[0], l[1] = file_name[idx], file_op[idx]
            if idx < len(note_op):
                l[3], l[4] = note_name[idx], note_op[idx]
            if idx < len(link_op):
                l[6], l[7] = link_name[idx], link_op[idx]
            if idx < len(topic_feed_op):
                l[9], l[10] = topic_feed_name[idx], topic_feed_op[idx]
            if idx < len(topic_content_op):
                l[12], l[13] = topic_content_name[idx], topic_content_op[idx]
            writer_w.writerow(l)
        writer_w.writerow(['', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        
    op_file_mean, op_note_mean, op_link_mean, op_topic_feed_mean,  op_topic_content_mean = \
        np.mean(np.array(op_file_all)), np.mean(np.array(op_note_all)), np.mean(np.array(op_link_all)), \
        np.mean(np.array(op_topic_feed_all)), np.mean(np.array(op_topic_content_all))
    writer_w.writerow(['averages open rates', str(op_file_mean), '', '', str(op_note_mean), '', '', str(op_link_mean)
                          , '', '', str(op_topic_feed_mean), '', '', str(op_topic_content_mean)])
if __name__ == '__main__':
    # weekly open rates report
    start_date, end_day = datetime.date(2016, 1, 13), datetime.date(2016, 1, 26)
    file_w = 'extract_26.1/openrate_report_13.1_26.1.csv'
    export_weekly_report(start_date, end_day, file_w)
    # aggregate open rates report
    start_date, end_day = datetime.date(2016, 1, 10), datetime.date(2016, 1, 26)
    file_all = 'extract_26.1/openrate_report_10.1_26.1.csv'
    export_weekly_report(start_date, end_day, file_all, aggregate=True)