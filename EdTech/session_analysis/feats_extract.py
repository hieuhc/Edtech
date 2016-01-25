'''
Created on Oct 10, 2015

@author: HCH
'''
import pandas as pd
import numpy as np
import random as rd
import datetime
from sklearn import tree, metrics, ensemble, cross_validation
def dur_category(duration):     
    if duration < 44:
        return 44
    elif duration < 258:
        return 258
    else:
        return 5000
                
def feats_1():
    st_ss_dur = pd.read_csv('student_ss_dur.csv')
    print(st_ss_dur.shape)
    st_ss_dur = st_ss_dur.drop(['distinct_id','session','mp_country_code','time_begin','time_end'], axis = 1)
    print(st_ss_dur.shape)
    st_ss_dur['weekday'] = st_ss_dur.time_begin_1.map(lambda x : datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%a'))
    st_ss_dur['hour'] = st_ss_dur.time_begin_1.map(lambda x : int(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%H')))
    st_new = pd.DataFrame(st_ss_dur.ix[:,['screen_height','screen_width','hour']], columns=['screen_height','screen_width','hour'])
    for cate_att in ['defaultSpaceName','browser','os','weekday']:
        cate_ohe = pd.get_dummies(st_ss_dur.ix[:,cate_att], prefix = cate_att, dummy_na= True)
        st_new = pd.concat([st_new, cate_ohe], axis= 1)
    dur_cate = st_ss_dur.duration.map(lambda x: dur_category(x))
    st_new = pd.concat([st_new, dur_cate], axis= 1)
    st_new.to_csv('student_ss_dur_feats_1.csv', header=True, index=False)
def feats_teacher_activity():
    tch = pd.read_csv('../teacher.csv', encoding = 'utf8')
    act_strategi, act_kultur, act_entre = [],[],[]    
    for row_id in range(tch.shape[0]):
        if tch.event_1[row_id] in ['Created a link', 'Created a file', 'Created a note']:
            if tch.defaultSpaceName[row_id] == 'Strategi STR3605':
                act_strategi.append((tch.time[row_id], tch.event_1[row_id]))
            elif tch.defaultSpaceName[row_id] == 'Kulturledelse KLS3551':
                act_kultur.append((tch.time[row_id], tch.event_1[row_id]))   
            elif tch.defaultSpaceName[row_id] == 'Social Entrepreneurship ELE3702':
                act_entre.append((tch.time[row_id], tch.event_1[row_id]))
    act_strategi.append((1602517908, 'NA'))
    act_kultur.append((1602517908, 'NA'))
    act_entre.append((1602517908, 'NA'))
    # create tch features              
    st = pd.read_csv('student_ss_dur.csv')
    user_ing = ''
    
    for row_id in range(st.shape[0]):
        user_crr = st.distinct_id[row_id]
        if st.defaultSpaceName[row_id] == 'Strategi STR3605': act_lst = act_strategi
        elif st.defaultSpaceName[row_id] == 'Kulturledelse KLS3551' : act_lst = act_kultur
        elif  st.defaultSpaceName[row_id] == 'Social Entrepreneurship ELE3702': act_lst = act_entre                        
        if user_crr != user_ing:
            print('new user')
            act_ing_id = 0
            for idx in range(len(act_lst) - 1):
                if (st.time_begin[row_id] > act_lst[idx][0]) & (st.time_begin[row_id] <= act_lst[idx+1][0]):
                    act_ing_id = idx
                    break
            st.ix[row_id,'tch_idx'] = 1
            st.ix[row_id,'tch_prev_length'] = 0
            st.ix[row_id,'tch_num_content'] = act_ing_id + 1
            user_ing = user_crr
        # belong to same tch session
        elif st.time_begin[row_id] <= act_lst[act_ing_id + 1][0]:
            print('cont..')
            st.ix[row_id,'tch_idx'] = st.ix[row_id - 1,'tch_idx'] + 1
            st.ix[row_id,'tch_prev_length'] = st.ix[row_id - 1,'tch_prev_length'] + st.duration[row_id - 1]
            st.ix[row_id,'tch_num_content'] = st.ix[row_id - 1,'tch_num_content']
        # same user but different tch session
        else:
            print('diff session')
            for idx in range(act_ing_id + 1, len(act_lst) - 1):
                if (st.time_begin[row_id] > act_lst[idx][0]) & (st.time_begin[row_id] <= act_lst[idx+1][0]):
                    st.ix[row_id,'tch_num_content'] = idx - act_ing_id
                    act_ing_id = idx
                    break
            st.ix[row_id,'tch_idx'] = 1
            st.ix[row_id,'tch_prev_length'] = 0
        print(act_ing_id)
    return st.ix[:, ['tch_idx','tch_prev_length','tch_num_content']]
def feats_2():
    st_ss_dur = pd.read_csv('student_ss_dur.csv')
    st_ss_dur['weekday'] = st_ss_dur.time_begin_1.map(lambda x : datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%a'))
    st_ss_dur['hour'] = st_ss_dur.time_begin_1.map(lambda x : int(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%H')))
    st_ss_dur['weeknum'] = st_ss_dur.time_begin_1.map(lambda x : datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%U'))
    st_ss_dur['ss_index_week'], st_ss_dur['prev_length_total'], st_ss_dur['dur_from_last'] = st_ss_dur['hour'],st_ss_dur['hour'],st_ss_dur['hour']
    st_ss_dur['dur_last'] = st_ss_dur['hour']
    user_ing = ''
    for idx in range(st_ss_dur.shape[0]):
        week_crr, user_crr = st_ss_dur.weeknum[idx], st_ss_dur.distinct_id[idx]        
        if user_crr != user_ing:
            st_ss_dur.ss_index_week[idx] = 1
            st_ss_dur.prev_length_total[idx] = 0
            st_ss_dur.dur_from_last[idx] = 1000000
            st_ss_dur.dur_last[idx] = 0
            # update crr info
            ss_index_crr = 1
            prev_length = st_ss_dur.duration[idx]        
            user_ing = user_crr
            week_ing = week_crr
        elif week_crr != week_ing:
            st_ss_dur.ss_index_week[idx] = 1
            st_ss_dur.prev_length_total[idx] = 0
            st_ss_dur.dur_from_last[idx] = st_ss_dur.time_begin[idx] - st_ss_dur.time_end[idx-1] 
            st_ss_dur.dur_last[idx] = st_ss_dur.duration[idx - 1]
            # update crr info
            ss_index_crr = 1
            prev_length = st_ss_dur.duration[idx]      
            week_ing = week_crr
        else:
            st_ss_dur.ss_index_week[idx] = ss_index_crr + 1
            st_ss_dur.prev_length_total[idx] = prev_length 
            st_ss_dur.dur_from_last[idx] = st_ss_dur.time_begin[idx] - st_ss_dur.time_end[idx-1]
            st_ss_dur.dur_last[idx] = st_ss_dur.duration[idx - 1]
            # update crr info
            ss_index_crr += 1
            prev_length += st_ss_dur.duration[idx]              
    # convert cate to ohe, as in feats 1
    st_new = pd.DataFrame(st_ss_dur.ix[:,['screen_height','screen_width','hour','ss_index_week','prev_length_total','dur_from_last','dur_last']], 
                          columns=['screen_height','screen_width','hour','ss_index_week','prev_length_total','dur_from_last','dur_last'])
    for cate_att in ['defaultSpaceName','browser','os','weekday']:
        cate_ohe = pd.get_dummies(st_ss_dur.ix[:,cate_att], prefix = cate_att, dummy_na= True)
        st_new = pd.concat([st_new, cate_ohe], axis= 1)
    # add tch values to crr data set
    tch_df =  feats_teacher_activity()
    st_new = pd.concat([st_new, tch_df], axis= 1)
    # convert session length to categories
    dur_cate = st_ss_dur.duration.map(lambda x: dur_category(x))
    st_new = pd.concat([st_new, dur_cate], axis= 1)
    st_new.to_csv('student_ss_dur_feats_2.csv', header=True, index=False)
if __name__ == '__main__':
    feats_1()
    
    
    