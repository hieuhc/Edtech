'''
Created on Oct 20, 2015

@author: HCH

This file contains code for analyzing sessions-related users
'''
import pandas as pd
import datetime
from collections import Counter
import csv


class SessionAnalysis:
    def __init__(self, ss_file):
        print('init function')
        self.ss_data = pd.read_csv(ss_file)

    def export_duration_view_content(self, file_name):
        """
        :return: duration of 'viewed content' action respect to places action comes from
        """
        screen_duration_dict = {}
        for idx in range(self.ss_data.shape[0]):
            event_1_crr = self.ss_data.event_1[idx]
            if event_1_crr == 'Viewed content' and (idx > 0):
                event_1_prev = self.ss_data.event_1[idx - 1]
                if event_1_prev not in screen_duration_dict:
                    screen_duration_dict[event_1_prev] = [self.ss_data.duration[idx]]
                elif self.ss_data.session[idx] == self.ss_data.session[idx - 1]:
                    screen_duration_dict[event_1_prev].append(self.ss_data.duration[idx])

        file = csv.writer(open(file_name, 'w', encoding='utf8'), delimiter=',', lineterminator='\n')
        file.writerow(list(screen_duration_dict.keys()))
        for key in screen_duration_dict.keys():
            print('-----------')
            print('%s: %s' % (key, str(screen_duration_dict[key])))
        row_idx = 0
        while True:
            row_value = []
            stop = True
            for key in screen_duration_dict.keys():
                if len(screen_duration_dict[key]) > row_idx:
                    row_value.append(screen_duration_dict[key][row_idx])
                    stop = False
                else:
                    row_value.append('')
            file.writerow(row_value)
            row_idx += 1
            if stop:
                break

    def export_duration_screen(self, file_name):
        duration_screen_dict = {'content': [], 'feed': []}
        ss_cur = ''
        for idx in range(self.ss_data.shape[0]):
            ss_ing = self.ss_data.session[idx]
            screen_ing = self.ss_data.screen[idx]

            if ss_ing != ss_cur:
                screen_crr, ss_cur = screen_ing, ss_ing
                time_start = time_end = self.ss_data.time[idx]
            elif (ss_ing == ss_cur) and (screen_ing != screen_crr):
                if screen_crr in duration_screen_dict:
                    duration_screen_dict[screen_crr].append(time_end - time_start)
                screen_crr = screen_ing
                time_start = time_end = self.ss_data.time[idx]
            elif (ss_ing == ss_cur) and (screen_ing == screen_crr):
                time_end = self.ss_data.time[idx]
        file = csv.writer(open(file_name, 'w', encoding='utf8'), delimiter=',', lineterminator='\n')
        file.writerow(list(duration_screen_dict.keys()))
        row_idx = 0
        while True:
            stop = True
            row_vale = []
            for key in duration_screen_dict.keys():
                if len(duration_screen_dict[key]) > row_idx:
                    stop = False
                    row_vale.append(duration_screen_dict[key][row_idx])
                else:
                    row_vale.append('')
            file.writerow(row_vale)
            row_idx += 1
            if stop:
                break

    def export_duration_content_topic(self, file_name):
        duration_content_topic = {'Viewed content/all': [], 'Viewed content/topic': []}
        for idx in range(self.ss_data.shape[0]):
            ss_ing, event_ing, screen_ing, time_ing = self.ss_data.session[idx], self.ss_data.event_1[idx], \
                                            self.ss_data.screen[idx], self.ss_data.time[idx]

            if ss_ing != ss_crr:
                if event_crr in duration_content_topic:
                    duration_content_topic[event_crr].append(time_end - time_start)
                ss_crr, event_crr, screen_crr, time_start, time_end = ss_ing, event_ing, screen_ing, time_ing, time_ing
            elif (screen_ing == screen_crr) and (event_crr in duration_content_topic):
                if (event_ing in duration_content_topic) and (event_crr != event_ing):
                    duration_content_topic[event_crr].append(time_ing - time_start)
                    event_crr, screen_crr, time_start, time_end = event_ing, screen_ing, time_ing, time_ing
                else:
                    time_end = time_ing
            elif (screen_ing != screen_crr) and (event_crr in duration_content_topic):
                duration_content_topic[event_crr].append(time_ing - time_start)
                if event_ing in duration_content_topic:
                    event_crr, screen_crr, time_start, time_end = event_ing, screen_ing, time_ing, time_ing

        print(duration_content_topic['Viewed content/all'])
        print(duration_content_topic['Viewed content/topic'])

    @staticmethod
    def users_log_all_week():
        # Print usrs loged in corresponding weeks
        st = pd.read_csv('student_ss_dur.csv')
        st['weeknum'] = st['time_begin_1'].map(lambda x : datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%U'))
        print(sorted(set(st.weeknum)))
        usr_ing, week_ing = '', []
        usr_week_list = []
        for idx in range(st.shape[0]):
            usr_crr = st.distinct_id[idx]
            if usr_crr!=usr_ing:
                if idx > 0:
                    week_ing = list(sorted(set(week_ing)))
                    usr_week_list.append((len(week_ing), usr_ing, week_ing))
                usr_ing = usr_crr
                week_ing = [st.weeknum[idx]]
            else:
                week_ing.append(st.weeknum[idx])
        weeks_active = [usr_week_list[idx][0] for idx in range(len(usr_week_list))]
        print(Counter(weeks_active))
        for item in sorted(usr_week_list):
            print(item)
        
if __name__ == '__main__':
    ss_obj = SessionAnalysis('data/student_session.csv')
    # ss_obj.export_duration_view_content('report/spring16/duration_view_content.csv')
    ss_obj.export_duration_screen('report/spring16/duration_screen.csv')