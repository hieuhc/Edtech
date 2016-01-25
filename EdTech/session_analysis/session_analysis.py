'''
Created on Oct 20, 2015

@author: HCH

This file contains code for analyzing sessions-related users
'''
import pandas as pd
import numpy  as np
import datetime
from collections import Counter
def users_log_allweek():
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
    users_log_allweek()