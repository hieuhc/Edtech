"""
Created on Oct 6, 2015

@author: HCH
"""
from EdTech import Constant
import pandas as pd
import numpy as np
import datetime
import csv
from collections import Counter


class WeeklyReport:
    def __init__(self, data_file, date_start, date_end):
        self.std = pd.read_csv(data_file)
        self.date_start = date_start
        self.date_end = date_end
        self.std['date'] = self.std.time_1.map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').date())
        self.std['week_num'] = self.std.date.map(lambda x: x.isocalendar()[1])

    def log_x_time_per_week(self, x_time):
        res, std_x_time_total, std_num_total = [], 0, 0
        std_w = self.std[(self.std.date >= self.date_start) & (self.std.date <= self.date_end)]
        for course_idx in range(len(Constant.COURSE_NAME)):
            space_name = Constant.COURSE_NAME[course_idx]
            std_num = Constant.COURSE_NUM_STD[course_idx]
            std_w_course = std_w[std_w.space_1 == space_name]
            std_count = Counter(list(std_w_course.distinct_id))
            std_x_time = [std_id for std_id in std_count if std_count[std_id] == x_time]
            res.append(len(std_x_time) / std_num)
            std_x_time_total += len(std_x_time)
            std_num_total += std_num
        res.append(std_x_time_total / std_num_total)
        return res

    def log_x_day_per_week(self, x_day, week_num=None):
        if week_num is None:
            std_w = self.std[(self.std.date >= self.date_start) & (self.std.date <= self.date_end)]
        else:
            std_w = self.std[self.std.week_num == week_num]
        res, log_x_day_total, std_num_total = [], 0, 0
        for course_idx in range(len(Constant.COURSE_NAME)):
            space_name = Constant.COURSE_NAME[course_idx]
            std_num = Constant.COURSE_NUM_STD[course_idx]
            std_w_course = std_w[std_w.space_1 == space_name]
            log_x_day_df = std_w_course.groupby(['distinct_id'])['date'].nunique()
            log_x_day_lst = [log_x_day_df.index[idx] for idx in range(len(log_x_day_df.index))
                             if log_x_day_df.values[idx] >= x_day]
            res.append(len(log_x_day_lst) / std_num)
            log_x_day_total += len(log_x_day_lst)
            std_num_total += std_num
            print('-- %s:' % space_name)
            print('%d day: %f' % (x_day, len(log_x_day_lst) / std_num))
        res.append(log_x_day_total / std_num_total)
        return res

    def export_x_day_per_week(self, file_name):
        file = csv.writer(open(file_name, 'w', encoding='utf8'), delimiter=',', lineterminator='\n')
        file.writerow(['no. login >=', '1 day/week', '2 days/week', '3 days/week', '4 days/week',
                       '5 days/week', '6 days/week'])
        day_lst = [1, 2, 3, 4, 5, 6]
        log_x_day = [self.log_x_day_per_week(x) for x in day_lst]
        log_x_day_data = np.vstack(log_x_day).T
        labels = Constant.COURSE_NAME + ['Aggregate']
        for idx in range(len(labels)):
            label = labels[idx]
            file.writerow([label] + list(log_x_day_data[idx]))

    def export_x_day_every_week(self, file_name):
        file = csv.writer(open(file_name, 'w', encoding='utf8'), delimiter=',', lineterminator='\n')
        file.writerow(['no. login >=', '1 day/week', '2 days/week', '3 days/week', '4 days/week',
                       '5 days/week', '6 days/week'])
        day_lst = [1, 2, 3, 4, 5, 6]
        week_num_set = sorted(set(self.std.week_num))
        for week_num in week_num_set:
            print('- week num: %d' % week_num)
            log_x_day_week = [self.log_x_day_per_week(x, week_num)[3] for x in day_lst]
            file.writerow(['week ' + str(week_num)] + log_x_day_week)


def export_weekly_report(data_file, content_id_file, date_start, date_end, file_report, aggregate=False):
    std = pd.read_csv(data_file)
    std['date'] = std.time_1.map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').date())
    
    std_w = std[(std.date >= date_start) & (std.date <= date_end)]

    writer_w = csv.writer(open(file_report, 'w', encoding='utf8'), delimiter=',', lineterminator='\n')
    op_file_all, op_note_all, op_link_all, op_topic_feed_all, op_topic_content_all, download_rate_all\
        = [], [], [], [], [], []
    for course_idx in range(len(Constant.COURSE_NAME)):
        space_name = Constant.COURSE_NAME[course_idx]
        std_num = Constant.COURSE_NUM_STD[course_idx]
        print('---' + space_name)
        std_w_course = std_w[std_w.space_1 == space_name]
        print('num of std: %d' % std_num)
        log_rate = len(set(std_w_course.distinct_id)) / std_num
        total_open, std_open = 0, []
        print('log rate: %f' % log_rate)
        # view file
        std_w_course_content = std_w_course[(std_w_course.event_1 == 'Viewed content') &
                                            (std_w_course.contentType == 'file')]
        total_open += std_w_course_content.shape[0]
        std_open.extend(list(std_w_course_content.distinct_id.values))
        temp = std_w_course_content.groupby(['contentName'])['distinct_id'].nunique()
        file_name = list(temp.index) + ['average']
        file_op = temp.values/std_num
        op_file_all.extend(file_op.tolist())
        file_op = np.append(file_op, np.array([np.mean(file_op)]))
        # view link
        std_w_course_content = std_w_course[std_w_course.event_1 == 'Viewed link']
        total_open += std_w_course_content.shape[0]
        std_open.extend(list(std_w_course_content.distinct_id.values))
        if std_w_course_content.shape[0] > 0:
            temp = std_w_course_content.groupby(['contentName'])['distinct_id'].nunique()
            link_name = list(temp.index) + ['average']
            link_op = temp.values/std_num
            op_link_all.extend(link_op.tolist())
            link_op = np.append(link_op, np.array([np.mean(link_op)]))
        else:
            link_name, link_op = [], []

        # Downloaded file
        content_id_data = pd.read_csv(content_id_file, encoding='utf8')
        content_id_data = pd.DataFrame(content_id_data[content_id_data.space_1 == space_name].values,
                                       columns=content_id_data.columns)
        content_id_map = {content_id_data.contentName[idx]: content_id_data.contentId[idx] for idx in
                          range(content_id_data.shape[0])}
        std_w_course_download = std_w_course[std_w_course.event_1 == 'Downloaded file']
        total_download = std_w_course_download.shape[0]
        std_download = list(std_w_course_download.distinct_id.values)
        temp = std_w_course_download.groupby(['contentId'])['distinct_id'].nunique()
        download_rate = temp.values/std_num
        id_download_map = {temp.index[idx]: download_rate[idx] for idx in range(len(temp.index))}
        download_rate_by_name = []
        for file_each in file_name:
            if (file_each in content_id_map) and (content_id_map[file_each] in id_download_map):
                download_rate_by_name.append(id_download_map[content_id_map[file_each]])
            elif file_each != 'average':
                download_rate_by_name.append(0.0)
        download_rate_by_name.append(np.mean(download_rate))
        print(download_rate_by_name)
        print('download rate average: %f' % np.mean(download_rate))
        download_rate_all.extend(download_rate.tolist())

        # view topic feed
        std_w_course_topic = std_w_course[(std_w_course.event_1 == 'Viewed feed/all') |
                                          (std_w_course.event_1 == 'Viewed feed/findOne') |
                                          (std_w_course.event_1 == 'Viewed feed/topic')]
        temp = std_w_course_topic.groupby(['topic'])['distinct_id'].nunique()
        topic_feed_name = list(temp.index) + ['average']
        topic_feed_op = temp.values/std_num
        op_topic_feed_all.extend(topic_feed_op.tolist())
        topic_feed_op = np.append(topic_feed_op, np.array([np.mean(topic_feed_op)]))

        # view topic content
        std_w_course_topic = std_w_course[(std_w_course.event_1 == 'Viewed content/all') |
                                          (std_w_course.event_1 == 'Viewed content/topic')]
        temp = std_w_course_topic.groupby(['topic'])['distinct_id'].nunique()
        topic_content_name = list(temp.index) + ['average']
        topic_content_op = temp.values/std_num
        op_topic_content_all.extend(topic_content_op.tolist())
        topic_content_op = np.append(topic_content_op, np.array([np.mean(topic_content_op)]))

        # start writing to file
        writer_w.writerow([space_name, '', '', '', '', '', '', '', '', '', '', ''])
        if not aggregate:
            writer_w.writerow(['logged in rate', str(log_rate), '', '', '', '', '', '', '', '', ''])
            writer_w.writerow(['total content opened', str(total_open), '', '', '', '', '', '', '', '', ''])
            writer_w.writerow(['%user opened', str(len(set(std_open))/std_num), '', '', '', '', '', '', '', '', ''])
            writer_w.writerow(['total downloads', str(total_download), '', '', '', '', '', '', '', '', ''])
            writer_w.writerow(['%user downloaded', str(len(set(std_download))/std_num), '', '', '', '', '', '', '', '', ''])
        writer_w.writerow(['File', '', '', '', 'Link', '', '', 'Topic (feed)', '', '', 'Topic (content)', ''
                           ])
        for idx in range(max(len(file_op), len(link_op), len(topic_feed_op), len(topic_content_op))):
            l = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
            if idx < len(file_op):
                l[0], l[1], l[2] = file_name[idx], file_op[idx], download_rate_by_name[idx]
            if idx < len(link_op):
                l[4], l[5] = link_name[idx], link_op[idx]
            if idx < len(topic_feed_op):
                l[7], l[8] = topic_feed_name[idx], topic_feed_op[idx]
            if idx < len(topic_content_op):
                l[10], l[11] = topic_content_name[idx], topic_content_op[idx]
            writer_w.writerow(l)
        writer_w.writerow(['', '', '', '', '', '', '', '', '', '', '', ''])
        
    op_file_mean, download_mean, op_link_mean, op_topic_feed_mean,  op_topic_content_mean = \
        np.mean(np.array(op_file_all)), np.mean(np.array(download_rate_all)), np.mean(np.array(op_link_all)), \
        np.mean(np.array(op_topic_feed_all)), np.mean(np.array(op_topic_content_all))
    writer_w.writerow(['averages open rates', str(op_file_mean), str(download_mean), '', '', str(op_link_mean)
                          , '', '', str(op_topic_feed_mean), '', '', str(op_topic_content_mean)])
if __name__ == '__main__':
    # weekly open rates report
    # start_date, end_day = datetime.date(2016, 2, 15), datetime.date(2016, 2, 21)
    # file_w = 'reports/extract_16.2.21/openrate_report_16.2.15_16.2.21.csv'
    # export_weekly_report('data/data/student.csv', 'data/data/content_id_map.csv',
    #                      start_date, end_day, file_w)
    # print('----- Aggregate -----')
    # # aggregate open rates report
    # start_date, end_day = datetime.date(2016, 1, 15), datetime.date(2016, 2, 21)
    # file_all = 'reports/extract_16.2.21/openrate_report_16.1.15_16.2.21.csv'
    # export_weekly_report('data/data/student.csv', 'data/data/content_id_map.csv',
    #                      start_date, end_day, file_all, aggregate=True)
    start_date, end_day = datetime.date(2016, 2, 22), datetime.date(2016, 2, 28)
    w_obj = WeeklyReport('data/data/student.csv', start_date, end_day)
    file_w = 'reports/log_x_day_per_week.csv'
    file_every_w = 'reports/log_x_day_every_week.csv'
    w_obj.export_x_day_per_week(file_w)
    w_obj.export_x_day_every_week(file_every_w)