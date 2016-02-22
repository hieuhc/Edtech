"""
Created on Oct 10, 2015

@author: HCH
"""

import pandas as pd
import numpy as np
import random as rd


def check_logout():
    student = pd.read_csv('../../data/data/student.csv')
    id_time_dict = dict()
    dura = []
    stu = []
    for idx in range(student.shape[0]):
        if student.event_1[idx] == 'Logged out':
            id_time_dict[student.distinct_id[idx]] = student.time[idx]
            print('**********')
            print(idx)
            print(student.time[idx])
            
        else:
            student_crr = student.distinct_id[idx]             
            if (student_crr in id_time_dict) and (id_time_dict[student_crr] > 0):
                print('--------')
                
                print(id_time_dict[student_crr])
                print(student.time[idx])
                print(idx)
                dura.append(student.time[idx] - id_time_dict[student_crr])
                id_time_dict[student_crr] = -1
                stu.append(student_crr)
    log_out = student[student.event_1 == 'Logged out']
    print(log_out.shape[0])
    print(len(dura))
    print(dura)    
    print(stu)


def check_continuity():
    data = pd.read_csv('../../data/data/student.csv', encoding='utf8')
    student = pd.DataFrame(data.sort(['distinct_id', 'time']).values, columns=data.columns)
    stu_ing = ''
    time_lst = []
    for idx in range(student.shape[0]):
        stu_crr = student.distinct_id[idx]
        if stu_crr != stu_ing:            
            interval_lst = [(time_lst[i+1] - time_lst[i]) for i in range(len(time_lst) - 1)]
            print('%s, %s' % (stu_ing, str(interval_lst)))
            stu_ing = stu_crr
            time_lst = [student.time[idx]]
        else:            
            time_lst.append(student.time[idx])


def create_session_id(session_col):
    while True:
        r = rd.randrange(0, 100000)
        if r not in session_col:
            break
    return r


def csv2session(thres=1200):
    # split sequences of events to sessions
    data = pd.read_csv('../../data/data/student.csv', encoding='utf8')
    student = pd.DataFrame(data.sort(['distinct_id', 'time']).values, columns=data.columns)
    time_ing, stu_ing = 0, ''
    session_col = []
    for idx in range(student.shape[0]):
        time_crr, stu_crr = student.time[idx], student.distinct_id[idx]
        if (time_crr - time_ing > thres) or stu_crr != stu_ing:
            session_crr = create_session_id(session_col)
            session_col.append(session_crr)
            session_ing = session_crr
            time_ing, stu_ing = time_crr, stu_crr
        
        else:
            session_col.append(session_ing)
            time_ing = time_crr
    student['session'] = session_col
    # calculate duration of each event
    ev_dur = []
    for idx in range(student.shape[0] - 1):
        if student.session[idx + 1] == student.session[idx]:
            ev_dur.append(student.time[idx+1] - student.time[idx])
        else:
            ev_dur.append(-1)
    ev_dur.append(-1)
    student['duration'] = ev_dur 
    student.to_csv('data/student_session.csv', header=True, index=False)


def extract_ss_dur(file_from, file_to):
    # calculate duration for each event 
    data = pd.read_csv(file_from, encoding='utf8')
    data_dur = []
    ss_ing = -1
    row_ing = []
    for idx in range(data.shape[0]):
        ss_crr = data.session[idx]
        if ss_crr != ss_ing:
            if (idx > 0) and row_ing[3] > 1:
                row_ing.append(data.time[idx - 1])            
                data_dur.append(row_ing)
            row_ing = [data.distinct_id[idx], data.session[idx], data.space_1[idx],
                       data.time[idx], data.time_1[idx]
                       ]
            ss_ing = ss_crr
        else:
            if len(str(data.space_1[idx])) > 3:
                row_ing[2] = data.space_1[idx]
            
    columns_name = ['distinct_id', 'session', 'space_1', 'time_begin', 'time_begin_1',
                    'time_end']
    df = pd.DataFrame(np.array(data_dur), columns=columns_name)
    df['duration'] = df.time_end.astype(int) - df.time_begin.astype(int)
    df.to_csv(file_to, index=False)


def create_transition_matrix_event(file_result_from, file_result_to, course=None):
    # calculate transition matrix from the sequence of events
    
    st_ss = pd.read_csv('data/student_session.csv')
    if course is not None:
        st_ss = pd.DataFrame(st_ss[st_ss.space_1 == course].values, columns=st_ss.columns)
    # remove additional 'Viewed folder' event within two 'Viewed space' events
    event_seq_lst, event_seq = [], []
    ss_ing = -1
    for idx in range(st_ss.shape[0]):
        ss_crr = st_ss.session[idx]
        event_crr = st_ss.event_1[idx]
        if ss_crr != ss_ing:            
            if idx > 0:
                event_seq.append('End')
                event_seq_lst.append(event_seq)
            ss_ing = ss_crr
            event_seq = ['Start', event_crr]
        else:
            event_seq.append(event_crr)
    print('session seq lst: %s' % str(event_seq_lst))     
    
    event_lb = set(np.hstack(event_seq_lst))
    event_lb_dict = {ev: idx for idx, ev in enumerate(event_lb)}
    mat_trans = np.zeros((len(event_lb), len(event_lb)), dtype=float)
    for idx in range(len(event_seq_lst)):
        event_seq = event_seq_lst[idx]
        for i in range(len(event_seq) - 1):
            row_i, col_i = event_lb_dict[event_seq[i]], event_lb_dict[event_seq[i + 1]]
            mat_trans[row_i, col_i] += 1
    ''' cell[i,j] = transition prob for state i to convert to j '''
    row_sum = np.sum(mat_trans, axis=1)
    mat_trans_from = mat_trans / row_sum.reshape(-1, 1)
    df = pd.DataFrame(mat_trans_from, index=list(event_lb), columns=list(event_lb))
    df.to_csv(file_result_from, header=True, index=True)
    ''' cell[i,j] = transition prob for state j to be converted from i '''
    col_sum = np.sum(mat_trans, axis=0)
    mat_trans_to = mat_trans / col_sum
    df = pd.DataFrame(mat_trans_to, index=list(event_lb), columns=list(event_lb))
    df.to_csv(file_result_to, header=True, index=True)


def create_transition_matrix_folder(course):
    st_ss = pd.read_csv('data/student_session.csv')
    print(st_ss.shape)
    st_ss_course = pd.DataFrame(st_ss[(st_ss.defaultSpaceName == course) & (st_ss.event_1 == 'Viewed folder')].values,
                                columns=st_ss.columns)
    print(st_ss_course.shape)
    folder_set = list(set(st_ss_course.contentName_2.values)) + ['Start', 'End']
    print(folder_set)
    trans_matrix = pd.DataFrame(np.zeros((len(folder_set), len(folder_set))), 
                                index=list(folder_set), columns=list(folder_set))
    ss_ing = -1
    for row_idx in range(st_ss_course.shape[0]):
        ss_crr = st_ss_course.session[row_idx]
        folder_crr = st_ss_course.contentName_2[row_idx]
        if ss_crr != ss_ing: 
            if str(folder_crr) != 'nan':
                trans_matrix.ix['Start', folder_crr] += 1
                ss_ing = ss_crr
        else:
            trans_matrix.ix[st_ss_course.contentName_2[row_idx-1], folder_crr] += 1
            if (row_idx == st_ss_course.shape[0] - 1) or (st_ss_course.session[row_idx + 1] != ss_crr):
                trans_matrix.ix[folder_crr, 'End'] += 1
    trans_sum = np.sum(trans_matrix.values, axis = 1)
    trans_matrix_values = trans_matrix.values / trans_sum.reshape(-1,1)
    pd.DataFrame(trans_matrix_values, index=list(folder_set), columns=list(folder_set)).to_csv('trans_matrix_folder_' + course + '.csv', header=True, index=True)
    
if __name__ == '__main__':
    # check_logout()
    # check_continuity()
    csv2session()
    extract_ss_dur('data/student_session.csv', 'data/student_ss_dur.csv')
    # create_transition_matrix_folder()
    # create_transition_matrix_event('report/spring16/event_matrix_from.csv', 'report/spring16/event_matrix_to.csv')
