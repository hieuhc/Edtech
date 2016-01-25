'''
Created on Oct 11, 2015

@author: HCH
'''
import pandas as pd
import re
import csv as csv
import numpy as np
import csv

def add_content_openrate(fol_name):
    date_crr = re.split('_', fol_name)[1]
    print(date_crr)
    file = pd.read_csv(fol_name + '/' + 'openrate_report_6.8_' + date_crr + '.csv')
    report_strategi = pd.read_csv('reports/[strategi]openrate_content.csv', index_col = 0, encoding = 'utf8')
    report_kultur = pd.read_csv('reports/[kultur]openrate_content.csv', index_col = 0, encoding = 'utf8')
    report_entre = pd.read_csv('reports/[entre]openrate_content.csv', index_col = 0, encoding = 'utf8')
    report_crr = report_strategi
    date_crr = date_crr + '.2015'
    for idx in range(file.shape[0] - 1):
        if file.ix[idx,0] == 'Strategi STR3605':
            report_crr = report_strategi
        elif file.ix[idx,0] == 'Kulturledelse KLS3551':
            report_crr = report_kultur
        elif file.ix[idx,0] == 'Social Entrepreneurship ELE3702':
            report_crr = report_entre
        if (str(file.ix[idx, 1]) != 'nan') & (file.ix[idx, 0] != 'average'):
            report_crr.ix[file.ix[idx, 0], date_crr] = file.ix[idx, 1]
        if (str(file.ix[idx, 4]) != 'nan') & (file.ix[idx, 3] != 'average'):
            report_crr.ix[file.ix[idx, 3], date_crr] = file.ix[idx, 4]
        if (str(file.ix[idx, 7]) != 'nan') & (file.ix[idx, 6] != 'average'):
            report_crr.ix[file.ix[idx, 6], date_crr] = file.ix[idx, 7]
        
    report_strategi.to_csv('reports/[strategi]openrate_content.csv', header=True, index=True, encoding='utf8')
    report_kultur.to_csv('reports/[kultur]openrate_content.csv', header=True, index=True, encoding = 'utf8')
    report_entre.to_csv('reports/[entre]openrate_content.csv', header=True, index=True, encoding = 'utf8')
def name_cut_off(name):
    if len(name) < 30 :
        return name
    else:
        return str(name[:30] + ' ...')
def convert_2_r_format(file_from, file_to, line_each_graph = 6):
    data = pd.read_csv(file_from, index_col=0, encoding = 'utf8')
    file_csv = csv.writer(open(file_to,'w', encoding = 'utf8'), lineterminator = '\n', delimiter = ',')
    file_csv.writerow(['Week', 'Content', 'OpenRate', 'Group'])
    for row_idx in range(len(list(data.index))):
        row_name = list(data.index)[row_idx]
        # cut off the name        
        for col_name in data.columns:            
            file_csv.writerow([col_name, name_cut_off(row_name), data.ix[row_name, col_name], int( row_idx/ 6) ])                    
if __name__ == '__main__':
#     only add the current date 
    add_content_openrate('extract_9.12')
    convert_2_r_format('reports/[strategi]openrate_content.csv','reports/[strategi]openrate_content_rformat.csv')
    convert_2_r_format('reports/[kultur]openrate_content.csv','reports/[kultur]openrate_content_rformat.csv')
    convert_2_r_format('reports/[entre]openrate_content.csv','reports/[entre]openrate_content_rformat.csv')
        