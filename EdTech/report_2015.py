'''
Created on Dec 12, 2015

@author: HCH
'''
import pandas as pd
import numpy as np
import datetime
def usage(data_frame):
    course_set = set(data_frame.defaultSpaceName.values)
    print(course_set)
    # daily usage
    print(' =================== DAILY USAGE')
    data_frame['date'] = data_frame.time_1.map(lambda x : datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S').date())    
    for course in course_set:
        print('-----'); print(course)
        data_course = data_frame.ix[data_frame.defaultSpaceName == course]
        usage_daily = data_course.groupby(['date'])['distinct_id'].nunique()        
        print(np.mean(np.array(usage_daily)))
    usage_daily_total = data_frame.groupby(['date'])['distinct_id'].nunique()
    print(np.mean(np.array(usage_daily_total)))
    
    # weekly usage
    print('======================= WEEKLY USAGE')
    data_frame['week'] = data_frame.time_1.map(lambda x : datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S').strftime('%U'))    
    for course in course_set:
        print('-----'); print(course)
        data_course = data_frame.ix[data_frame.defaultSpaceName == course]
        usage_weekly = data_course.groupby(['week'])['distinct_id'].nunique()        
        print(np.mean(np.array(usage_weekly)))
    usage_weekly_total = data_frame.groupby(['week'])['distinct_id'].nunique()
    print(np.mean(np.array(usage_weekly_total)))
    
    # monthly usage
    print(' ================ MONTHLY USAGE')
    data_frame['month'] = data_frame.time_1.map(lambda x : datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S').strftime('%B'))    
    for course in course_set:
        print('-----'); print(course)
        data_course = data_frame.ix[data_frame.defaultSpaceName == course]
        usage_monthly = data_course.groupby(['month'])['distinct_id'].nunique()        
        print(np.mean(np.array(usage_monthly)))
    usage_monthly_total = data_frame.groupby(['month'])['distinct_id'].nunique()
    print(np.mean(np.array(usage_monthly_total)))
    

if __name__ == '__main__':
    student = pd.read_csv('student.csv')
    usage(student)