import pandas as pd
import datetime
import csv
from EdTech import Constant
from collections import Counter


class StudentBehaviorAnalysis:

    def __init__(self, file_data):
        self.std = pd.read_csv(file_data)
        self.std['date'] = self.std.time_begin_1.map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').date())
        self.std['week_num'] = self.std.date.map(lambda x: x.isocalendar()[1])

    def export_std_login_by_week(self, file_name):
        file = csv.writer(open(file_name, 'w'), delimiter=',', lineterminator='\n')
        week_num_set = list(sorted(set(self.std.ix[:, 'week_num'].values)))
        file.writerow(['space_1', 'distinct_id'] + [str(w) for w in week_num_set] + ['week_login_total'])
        for course in Constant.COURSE_NAME:
            std_course = pd.DataFrame(self.std[self.std.space_1 == course].values, columns=self.std.columns)
            for std_idx in list(set(std_course.distinct_id.values)):
                week_counter = Counter(std_course[std_course.distinct_id == std_idx].week_num.values)
                row_val = [course, std_idx]
                week_time_total = 0
                for w in week_num_set:
                    if w in week_counter:
                        row_val.append(week_counter[w])
                        week_time_total += week_counter[w]
                    else:
                        row_val.append(0)
                        week_time_total += 0
                row_val.append(week_time_total)
                file.writerow(row_val)
        pd.read_csv(file_name).sort_values(by=['space_1', 'week_login_total']).to_csv(file_name, header=True, index=False)

if __name__ == '__main__':
    std_analysis = StudentBehaviorAnalysis('/home/hieuhuynh/Documents/Projects/Edtech/EdTech/analysis/' +
                                           'session_analysis/data/student_ss_dur.csv')
    std_analysis.export_std_login_by_week('/home/hieuhuynh/Documents/Projects/Edtech/EdTech/analysis/' +
                                          'student_behavior_analysis/data/std_login_by_week.csv')