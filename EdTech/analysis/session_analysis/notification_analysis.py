
import pandas as pd
import EdTech.Constant
import csv
import datetime


class NotificationAnalysis:

    def __init__(self, std_ss_file):
        print('Enter init function')
        self.std_ss = pd.read_csv(std_ss_file)
        self.std_ss['date'] = self.std_ss.time_1.map(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").date())
        self.std_ss['week_num'] = self.std_ss.date.map(lambda x: x.isocalendar()[1])

    def extract_student_open_notification(self, file_to=None):
        """
        :param file_to:
        :return: % student view notification when receiving notifications by course. And aggregate
        """
        if file_to is not None:
            file = csv.writer(open(file_to, "w"), delimiter=',', lineterminator='\n')
            file.writerow(['Course', 'Viewed notifications', 'Viewed notification', 'Ratio'])
        student_view_noti_s, student_view_noti = 0, 0
        for course in EdTech.Constant.COURSE_NAME:
            std_ss_course = self.std_ss[self.std_ss.space_1 == course]
            std_view_noti_s, std_view_noti = [], []
            for std_id in set(std_ss_course.distinct_id.values):
                events = std_ss_course[std_ss_course.distinct_id == std_id].event_1.values
                if 'Viewed notifications' in events:
                    std_view_noti_s.append(std_id)
                if 'Viewed notification' in events:
                    std_view_noti.append(std_id)
            std_view_noti_s = set(std_view_noti_s)
            std_view_noti = set(std_view_noti)
            assert (std_view_noti.issubset(std_view_noti_s), '[not contained]' + str(std_view_noti.difference(std_view_noti_s)))
            print('Course: %s\nViewed notifications: %d. Viewed notification: %d. Ratio: %f' %
                  (course, len(std_view_noti_s), len(std_view_noti), len(std_view_noti) / len(std_view_noti_s)))
            student_view_noti_s += len(std_view_noti_s)
            student_view_noti += len(std_view_noti)
            if file_to is not None:
                file.writerow([course, len(std_view_noti_s), len(std_view_noti), len(std_view_noti)/len(std_view_noti_s)])
        if file_to is not None:
            file.writerow(['aggregate', student_view_noti_s, student_view_noti, student_view_noti/student_view_noti_s])

    def extract_time_open_notification(self, file_to=None):
        """
        :param file_to:
        :return: %time viewing notification when receiving notifications by course. And aggregate
        """
        if file_to is not None:
            file = csv.writer(open(file_to, 'w'), delimiter=',', lineterminator='\n')
        time_view_noti_s, time_view_noti = 0, 0
        for course in EdTech.Constant.COURSE_NAME:
            std_ss_course = self.std_ss[self.std_ss.space_1 == course]
            t_view_noti_s, t_view_noti = 0, 0
            events_not_open_noti = []
            for session in set(std_ss_course.session.values):
                events = std_ss_course[std_ss_course.session == session].event_1.values
                if 'Viewed notifications' in events:
                    t_view_noti_s += 1
                if 'Viewed notification' in events:
                    t_view_noti += 1
                if ('Viewed notification' in events) and ('Viewed notifications' not in events):
                    print('[noti not notis' + str(session))
                if ('Viewed notification' not in events) and ('Viewed notifications' in events):
                    events_not_open_noti.append(list(events))
            for events_ in events_not_open_noti:
                print(events_)
            print('Course: %s\nViewed notifications: %d. Viewed notification: %d. Ratio: %f' %
                  (course, t_view_noti_s, t_view_noti, t_view_noti/t_view_noti_s))
            print('----------------------------')
            time_view_noti_s += t_view_noti_s
            time_view_noti += t_view_noti
            if file_to is not None:
                file.writerow([course, t_view_noti_s, t_view_noti, t_view_noti/t_view_noti_s])
        if file_to is not None:
            file.writerow(['aggregate', time_view_noti_s, time_view_noti, time_view_noti/time_view_noti_s])

    def extract_time_open_noti_by_week(self, file_to):
        file = csv.writer(open(file_to, 'w'), delimiter=',', lineterminator='\n')
        week_num_set = sorted(set(self.std_ss.week_num.values))
        print('weeks: %s' + str(week_num_set))
        week_tile_set = ['week ' + str(i) for i in week_num_set]
        file.writerow(['course'] + week_tile_set)
        for course in EdTech.Constant.COURSE_NAME:
            print('------------\nCourse: %s' % course)
            t_course_ratio = []
            for week in week_num_set:
                t_course_w_noti_s, t_course_w_noti = 0, 0
                std_ss_w_course = self.std_ss[(self.std_ss.space_1 == course) &
                                              (self.std_ss.week_num == week)]
                for session in set(std_ss_w_course.session.values):
                    events = std_ss_w_course[std_ss_w_course.session == session].values
                    if 'Viewed notifications' in events:
                        t_course_w_noti_s += 1
                    if "Viewed notification" in events:
                        t_course_w_noti += 1
                if t_course_w_noti_s > 0:
                    t_course_ratio.append(t_course_w_noti / t_course_w_noti_s)
                    print('week: %d. ratio: %f' % (week, t_course_w_noti / t_course_w_noti_s))
                else:
                    t_course_ratio.append('NA')

            file.writerow([course] + t_course_ratio)

if __name__ == '__main__':
    noti = NotificationAnalysis('/home/hieuhuynh/Documents/Projects/Edtech/EdTech/analysis/session_analysis/data/' +
                                'student_session.csv')
    # noti.extract_time_open_notification('/home/hieuhuynh/Documents/Projects/Edtech/EdTech/analysis/session_analysis/'+
    #                                     'report/spring16/time_open_noti.csv')
    noti.extract_student_open_notification('/home/hieuhuynh/Documents/Projects/Edtech/EdTech/analysis/session_analysis/'+
                                        'report/spring16/std_open_noti.csv')
    # noti.extract_time_open_noti_by_week('/home/hieuhuynh/Documents/Projects/Edtech/EdTech/analysis/session_analysis/'+
    #                                     'report/spring16/time_open_noti_by_week.csv')