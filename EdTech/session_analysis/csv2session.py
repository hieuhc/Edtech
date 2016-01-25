'''
Created on Oct 10, 2015

@author: HCH
'''
import pandas as pd
import numpy as np
import random as rd
import datetime
from sklearn import tree, metrics, ensemble, cross_validation

def check_logout():
    student = pd.read_csv('student.csv')
    id_time_dict = dict()
    dura = []
    stu = []
    for idx in range(student.shape[0]):
        if student.event_1[idx] == 'Logged out':
            id_time_dict[student.distinct_id[idx]] = student.time[idx]
            print('**********')
            print(idx); print(student.time[idx])
            
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
    data = pd.read_csv('student.csv', encoding = 'utf8')
    student = pd.DataFrame(data.sort(['distinct_id', 'time']).values, columns= data.columns)    
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
def csv2session(thres = 1200):
    # split sequences of events to sessions
    data = pd.read_csv('../student.csv', encoding = 'utf8')
    student = pd.DataFrame(data.sort(['distinct_id', 'time']).values, columns= data.columns) 
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
    student.to_csv('student_session.csv', header=True, index=False)
def extract_ss_dur(file_from, file_to):
    # calculate duration for each event 
    data = pd.read_csv(file_from, encoding = 'utf8')
    data_dur = []
    ss_ing = -1
    row_ing = []
    for idx in range(data.shape[0]):
        ss_crr = data.session[idx]
        if ss_crr != ss_ing:
            if (idx > 0) and row_ing[3] > 1:
                row_ing.append(data.time[idx - 1])            
                data_dur.append(row_ing)
            row_ing = [data.distinct_id[idx], data.session[idx], data.defaultSpaceName[idx], data.time[idx], data.time_1[idx],
                       data.browser[idx], data.mp_country_code[idx], data.os[idx],data.screen_height[idx], data.screen_width[idx]]
            ss_ing = ss_crr
        else:
            if len(str(data.defaultSpaceName[idx])) > 3:
                row_ing[2] = data.defaultSpaceName[idx]
            
    columns_name =  ['distinct_id', 'session', 'defaultSpaceName', 'time_begin', 'time_begin_1',
                     'browser','mp_country_code','os', 'screen_height','screen_width',
                     'time_end']
    df = pd.DataFrame(np.array(data_dur), columns = columns_name)
    df['duration'] = df.time_end.astype(int) - df.time_begin.astype(int)
    df.to_csv(file_to, index=False)   
def create_transition_matrix_event():
    # calculate transition matrix from the sequence of events
    
    st_ss = pd.read_csv('student_session.csv')
    # select relevant criteria        
#     temp = st_ss[(st_ss.os == 'iOS') | (st_ss.os == 'Android')]
#     st_ss = pd.DataFrame(temp.values, columns= st_ss.columns)
#     print(set(st_ss.os))
    # code use for analyzing users did not view any content/link
    usr_not_view = ["55d1d40f9997410800eefbc9", "55d1d4a19997410800eefc9b", "55d1d40f9997410800eefbdf", 
                    "55d1d6279997410800eefdcf", "55d1d4a19997410800eefc6b", "55d1d4a19997410800eefc55",
                    "55d1d40f9997410800eefbfd", "55d1d7749997410800eefe85", "55d1d40f9997410800eefbe3",
                    "55d1c04dc55fa508003dc65f", "55d1d4a19997410800eefc4e", "55d1d5d39997410800eefdae",
                    "55d1d3769997410800eefbad", "55d1d6769997410800eefe16", "55d1d40f9997410800eefbf9",
                    "55d1d6769997410800eefe1b", "55d1d63f9997410800eefded", "55d1d40f9997410800eefbd6",
                    "55d1c04dc55fa508003dc67d", "55d1d6769997410800eefe22", "55d1c04dc55fa508003dc677",
                    "55d1d4a19997410800eefcb3", "55d1d7609997410800eefe6c", "55d1d4a19997410800eefc96",
                    "55d1d40f9997410800eefbf3"]
    
    # remove additional 'Viewed folder' event within two 'Viewed space' events
    event_seq_lst, event_seq = [], []
    ss_ing = -1
    for idx in range(st_ss.shape[0]):
        ss_crr = st_ss.session[idx]
        event_crr = st_ss.event_1[idx]
        if ss_crr != ss_ing:            
            if idx > 0:
#                 # code to print usr not view in week
#                 if st_ss.distinct_id[idx - 1] in usr_not_view:
#                     x = datetime.datetime.strptime(st_ss.time_1[idx - 1], '%Y-%m-%d %H:%M:%S').date()
#                     if (x >= datetime.date(2015,10,5)) & (x <= datetime.date(2015,10,11)):
#                         print('%s : %s' % (st_ss.distinct_id[idx - 1], event_seq))
                # print all usr session actions
#                 print('%s : %s' % (st_ss.distinct_id[idx - 1], event_seq))
                event_seq.append('End')
                event_seq_lst.append(event_seq)
            ss_ing = ss_crr
            event_seq = ['Start', event_crr]
            if event_crr == 'Viewed space':
                space_folder = 1
            elif event_crr == 'Viewed folder':
                space_folder = 2
            else:
                space_folder = 1                        
        else:
            if space_folder == 1:
                event_seq.append(event_crr)
                if event_crr == 'Viewed folder':
                    space_folder = 2                
            else:
                if event_crr != 'Viewed folder':
                    event_seq.append(event_crr)
                    if event_crr == 'Viewed space':
                        space_folder = 1
    print('session seq lst: %s' % str(event_seq_lst))     
    
    event_lb = set(np.hstack(event_seq_lst))
#     assert len(event_lb) == 28, 'Len not match: %d' % len(event_lb)
    event_lb_dict = {ev : idx for idx,ev in enumerate(event_lb)} 
    mat_trans = np.zeros((len(event_lb), len(event_lb)), dtype = float)
    for idx in range(len(event_seq_lst)):
        event_seq = event_seq_lst[idx]
        for i in range(len(event_seq) - 1):
            row_i, col_i = event_lb_dict[event_seq[i]], event_lb_dict[event_seq[i + 1]]
            mat_trans[row_i, col_i] += 1
    row_sum = np.sum(mat_trans, axis = 1)
    mat_trans = mat_trans / row_sum.reshape(-1,1)
    df = pd.DataFrame(mat_trans, index= list(event_lb), columns = list(event_lb))
    df.to_csv('matrix_trans.csv', header= True, index = True)
def create_transition_matrix_folder(course):
    st_ss = pd.read_csv('student_session.csv')
    print(st_ss.shape)
    st_ss_course = pd.DataFrame(st_ss[(st_ss.defaultSpaceName == course) & (st_ss.event_1 == 'Viewed folder')].values,
                                columns= st_ss.columns)
    print(st_ss_course.shape)
    folder_set = list(set(st_ss_course.contentName_2.values)) + ['Start','End']
    print(folder_set)
    trans_matrix = pd.DataFrame(np.zeros((len(folder_set), len(folder_set))), 
                                index= list(folder_set), columns=list(folder_set))
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
    pd.DataFrame(trans_matrix_values, index= list(folder_set), columns=list(folder_set)).to_csv('trans_matrix_folder_' + course + '.csv', header=True, index=True)           
    
if __name__ == '__main__':
    #     check_logout()
#     check_continuity()
#     csv2session() 
#     extract_ss_dur('student_session.csv', 'student_ss_dur.csv')
    create_transition_matrix_folder('Social Entrepreneurship ELE3702')
#     create_transition_matrix_event()