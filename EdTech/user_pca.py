'''
Created on Sep 22, 2015
This file implements approach of using PCA in sklearn to find patterns among users though weekdays

@author: HCH
'''
import pandas as pd
from sklearn import decomposition, preprocessing
import datetime
import numpy as np
from scipy.stats.stats import pearsonr
import matplotlib.pylab as plt
import re
if __name__ == "__main__":
    data = pd.read_csv('student.csv', encoding = 'utf8')    
#     students in strategi course who viewed content/link    
    data_strategi = data[(data.space_1 == 'Entrepreneurship ELE3702') & 
                         (data.event_1  == 'Viewed folder') ]
    print(data_strategi.shape)
    # data from 2015-08-24 to 2015-09-21
    data_strategi['date'] = data_strategi.time_1.map(lambda x : datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S').date())
    data_sl = data_strategi[(data_strategi.date >datetime.date(2015,8,30))
                                  &
                            (data_strategi.date < datetime.date(2015,9,21))]
    print(data_sl.shape)    
    data_sl['weekday'] = data_sl.time_1.map(lambda x : datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S').strftime('%a'))
    df = pd.crosstab(data_sl.distinct_id, data_sl.name)
#     df = df.loc[:, ['Mon', 'Tue', 'Wed', 'Thu','Fri','Sat','Sun']]        
    user_id = df.index.values    
    ##### pca transform
    # scale array
    usr_day = df.values
    usr_day = usr_day / np.sum(usr_day, axis = 1).reshape(-1,1)    
    usr_day = usr_day.T
    scl = preprocessing.StandardScaler()
    usr_day_scl = scl.fit_transform(usr_day)
    # fit pca
    n_components = 0.95
    pca = decomposition.PCA(n_components = n_components, copy = True, whiten = True)
    pca.fit(usr_day_scl)        
    print(pca.explained_variance_ratio_)
#     print(pca.mean_)
    print(pca.n_components_)
    
    ### find most correlated variables/students
    usr_cmp = pca.transform(usr_day_scl)    
    usr_view_col = []
    for i in range(pca.n_components_):
        cor_lst = []
        for j in range(usr_day.shape[1]):
            cor = np.abs(pearsonr(usr_day[:,j], usr_cmp[:,i])[0])
            cor_lst.append((cor, user_id[j], usr_day[:,j]))
        
        cor_lst = sorted(cor_lst, reverse= True)        
        print(cor_lst[0])
        usr_view_col.append(cor_lst[0][2])
#     df = pd.DataFrame(usr_cmp, columns = ['Type 1','Type 2', 'Type 3'])
#     df.to_csv('pca_analysis/pca_3.csv', index=False)
    
    ### plot the system 
    color_vec = ['red','green', 'blue', 'yellow', 'black', 'cyan', 'magenta']
#     x_lev = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sar', 'Sun')
    print(df.columns)
    x_lev = tuple(map(lambda x: re.split(' ', x)[0], df.columns))
    print(x_lev)
    legend, legend_name = [], []
    for idx in range(len(usr_view_col)):
        p = plt.plot(usr_view_col[idx], c = color_vec[idx], linestyle = '-')
        legend.append(p[0])
        legend_name.append(str(int(pca.explained_variance_ratio_[idx] * 100 )) + '%')
    plt.xticks(np.arange(len(x_lev)), x_lev)
    plt.xlabel('folder name'); plt.ylabel('folder view ratio')
    plt.title('User types on folder view ratio - Entrepreneurship')
    plt.legend(tuple(legend), tuple(legend_name))
    plt.show()
    
    
    
    
    
    