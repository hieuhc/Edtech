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

    @staticmethod
    def write_dict_2_file(dict_2_write, file_name):
        file = csv.writer(open(file_name, 'w', encoding='utf8'), delimiter=',', lineterminator='\n')
        file.writerow(list(dict_2_write.keys()))
        row_idx = 0
        while True:
            stop = True
            row_vale = []
            for key in dict_2_write.keys():
                if len(dict_2_write[key]) > row_idx:
                    stop = False
                    row_vale.append(dict_2_write[key][row_idx])
                else:
                    row_vale.append('')
            file.writerow(row_vale)
            row_idx += 1
            if stop:
                break

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
        self.write_dict_2_file(duration_screen_dict, file_name)

    def export_duration_content_topic(self, file_name):
        duration_content_topic = {'Viewed content/all': [], 'Viewed content/topic': []}
        ss_crr, event_crr, time_start, time_end = '', '', 0, 0
        for idx in range(self.ss_data.shape[0]):
            ss_ing, event_ing, screen_ing, time_ing = self.ss_data.session[idx], self.ss_data.event_1[idx], \
                                            self.ss_data.screen[idx], self.ss_data.time[idx]

            if ss_ing != ss_crr:
                if event_crr in duration_content_topic:
                    duration_content_topic[event_crr].append(time_end - time_start)
                ss_crr, event_crr, screen_crr, time_start, time_end = ss_ing, event_ing, screen_ing, time_ing, time_ing
            elif event_crr in duration_content_topic:
                if ((event_ing in duration_content_topic) and (event_crr != event_ing)) or (screen_ing != screen_crr):
                    duration_content_topic[event_crr].append(time_ing - time_start)
                    event_crr, screen_crr, time_start, time_end = event_ing, screen_ing, time_ing, time_ing
                else:
                    time_end = time_ing
            else:
                event_crr, screen_crr, time_start, time_end = event_ing, screen_ing, time_ing, time_ing

        print(duration_content_topic['Viewed content/all'])
        print(duration_content_topic['Viewed content/topic'])
        self.write_dict_2_file(duration_content_topic, file_name=file_name)

    def export_duration_selecting_content(self, file_name):
        duration_selecting_content = {'Viewed content/all': [], 'Viewed content/topic': []}
        for idx in range(self.ss_data.shape[0] - 1):
            s_ing, event_ing, screen_ing, time_ing = self.ss_data.session[idx], self.ss_data.event_1[idx], \
                                                     self.ss_data.screen[idx], self.ss_data.time[idx]
            if (s_ing == self.ss_data.session[idx + 1]) and (event_ing in duration_selecting_content) and \
                    (self.ss_data.event_1[idx + 1] == 'Viewed content'):
                duration_selecting_content[event_ing].append(self.ss_data.time[idx + 1] - time_ing)

        self.write_dict_2_file(duration_selecting_content, file_name=file_name)

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
    # ss_obj.export_duration_screen('report/spring16/duration_screen.csv')
    # ss_obj.export_duration_content_topic('report/spring16/duration_content_topic.csv')
    ss_obj.export_duration_selecting_content('report/spring16/duration_selecting_content.csv')