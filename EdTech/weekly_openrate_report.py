'''
Created on Oct 6, 2015

@author: HCH
'''
import pandas as pd
import numpy as np
import datetime
import csv


def export_weekly_report(date_start, date_end, file_report, aggregate = False):
    std = pd.read_csv('student.csv')
    std['date'] = std.time_1.map(lambda x : datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').date())    
    
    std_w = std[(std.date >= date_start) & (std.date <= date_end)]
    space_name_lst = ['Strategi STR3605','Kulturledelse KLS3551','Social Entrepreneurship ELE3702']
    writer_w = csv.writer(open(file_report, 'w', encoding = 'utf8'), delimiter = ',', lineterminator = '\n')
    op_file_all, op_note_all, op_link_all = [], [], []
    for space_name in space_name_lst:
        print('---' + space_name)
        std_course = std[std.defaultSpaceName == space_name]
        std_w_course = std_w[std_w.defaultSpaceName == space_name]
        std_num = len(set(std_course.distinct_id))
        print('num of std: %d' % std_num)
        log_rate = len(set(std_w_course.distinct_id)) / len(set(std_course.distinct_id))
        print('log rate: %f' % log_rate)
        ## view file
        std_w_course_content = std_w_course[(std_w_course.event_1=='Viewed content') & (std_w_course.contentTypeId == 'file')]
        temp = std_w_course_content.groupby(['contentName_2'])['distinct_id'].nunique()
        file_name = list(temp.index) + ['average']
        file_op = temp.values/std_num
        op_file_all.extend(list(file_op))
        file_op = np.append(file_op, np.array([np.mean(file_op)]))    
        ## view note
        std_w_course_content = std_w_course[(std_w_course.event_1=='Viewed content') & (std_w_course.contentTypeId == 'note')]
        temp = std_w_course_content.groupby(['contentName_2'])['distinct_id'].nunique()
        note_name = list(temp.index)+ ['average']
        note_op = temp.values/std_num
        op_note_all.extend(list(note_op))
        note_op = np.append(note_op, np.array([np.mean(note_op)]))
        ## view link
        std_w_course_content = std_w_course[std_w_course.event_1=='Viewed link']
        temp = std_w_course_content.groupby(['contentName_2'])['distinct_id'].nunique()
        link_name = list(temp.index)+ ['average']
        link_op = temp.values/std_num
        op_link_all.extend(list(link_op))
        link_op = np.append(link_op, np.array([np.mean(link_op)]))
        
        #start wrting to file
        writer_w.writerow([space_name, '','','','','','',''])
        if not aggregate:
            writer_w.writerow(['logged in rate', str(log_rate), '','','','','',''])
        writer_w.writerow(['File', '','','Note','','','Link',''])
        for idx in range(max(len(file_op), len(note_op), len(link_op))):
            l = ['', '','','','','','','']
            if idx < len(file_op):
                l[0], l[1] = file_name[idx], file_op[idx]
            if idx < len(note_op):
                l[3], l[4] = note_name[idx], note_op[idx]
            if idx <len(link_op):
                l[6], l[7] = link_name[idx], link_op[idx]
            writer_w.writerow(l)
        writer_w.writerow(['', '','','','','','',''])
        
    op_file_mean, op_note_mean, op_link_mean = np.mean(np.array(op_file_all)), np.mean(np.array(op_note_all)), np.mean(np.array(op_link_all))
    writer_w.writerow(['averages open rates',str(op_file_mean), '','',str(op_note_mean),'','',str(op_link_mean)])
if __name__ == '__main__':
    # weekly open rates report
    start_date, end_day = datetime.date(2015,11,30), datetime.date(2015,12,9)    
    file_w = 'extract_9.12/openrate_report_30.11_9.12.csv'
    export_weekly_report(start_date, end_day, file_w)
    # aggregate open rates report
    start_date, end_day = datetime.date(2015,8,3), datetime.date(2015,12,9)
    file_all = 'extract_9.12/openrate_report_6.8_9.12.csv'
    export_weekly_report(start_date, end_day, file_all, aggregate= True)
        
        
        
    