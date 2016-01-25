'''
Created on Oct 10, 2015

@author: HCH
'''
import pandas as pd
import numpy as np
from sklearn import tree, metrics, ensemble, cross_validation, preprocessing, svm, cross_validation
import xgboost as xgb
SEED = 2015
############# FEATURE ENGINEERING METHODS
def eliminate_recursive(X,y,model, columns):
    feat_crr = list(range(X.shape[1]))
    cv_crr = 0
    while len(feat_crr) >= 2:
        feats_bin = []
        for feat_idx in range(X.shape[1]):
            if feat_idx in feat_crr:
                feat_use = [i for i in feat_crr if i != feat_idx]
                X_use = X[:, feat_use]
                cv_score = np.mean(np.array(cross_val(X_use, y, model, metrics_use='favor_3')))
                feats_bin.append((cv_score, feat_idx))
        feats_bin = sorted(feats_bin, reverse = True)
        cv_score_best = feats_bin[0][0]
        if cv_score_best >= cv_crr * 0.98:
            cv_crr = cv_score_best
            
            feat_to_remove_idx  = feats_bin[0][1]
            feat_crr = [i for i in feat_crr if i != feat_to_remove_idx]
            feat_to_remove = columns[feat_to_remove_idx]
            print('----------')            
            print(feat_crr)
            print('remove (%d, %s): %f' % (feat_to_remove_idx, str(feat_to_remove), cv_crr))
        else:
            break
    col_sel = [columns[idx] for idx in feat_crr]
    print('features selected: %s' % str(col_sel))
    return X[:,feat_crr]
############# MODELS SELECTION
def cross_val(X,y,model, cv = 5, print_cfmat = False, metrics_use = 'accuracy'):
    kf = cross_validation.KFold(n = len(y), n_folds = cv, shuffle = True, random_state = SEED)
    acc_lst = []
    for train, test in kf:
        X_train, y_train = X[train],y[train]
        X_test, y_test = X[test],y[test]
        model.fit(X_train, y_train)
        y_preds = model.predict(X_test)
        ## choose metrics for use
        if metrics_use == 'accuracy':
            acc_lst.append(metrics.accuracy_score(y_test, y_preds))
        elif metrics_use == 'f1_micro':
            acc_lst.append(metrics.f1_score(y_test, y_preds, average = 'micro'))
        elif metrics_use == 'f1_macro':
            acc_lst.append(metrics.f1_score(y_test, y_preds, average = 'macro'))
        elif metrics_use == 'f1_weighted':
            acc_lst.append(metrics.f1_score(y_test, y_preds, average = 'weighted'))
        elif metrics_use == 'favor_3':
            acc_lst.append(metrics.confusion_matrix(y_test, y_preds)[2,2])
        if print_cfmat:
            print(metrics.confusion_matrix(y_test, y_preds))
    return acc_lst
def tree_model(data):
    X,y = data.values[:,:-1], data.duration.values
    model = tree.DecisionTreeClassifier(criterion='gini', splitter ='best', max_depth = None, 
                                        min_samples_leaf= 10,
                                        max_features = 'sqrt', random_state=None, max_leaf_nodes=None)    
    model.fit(X,y)
    y_preds = model.predict(X)
    print(metrics.accuracy_score(y, y_preds))
    print(metrics.confusion_matrix(y, y_preds))
    tree.export_graphviz(model, out_file= 'tree_2.dot', 
                         feature_names= np.array(list(data.columns))[:-1])
    
    ### validation
    print('validation stage')
    cv_lst = cross_val(X, y, model, cv = 5)
    print(cv_lst)
    print(np.mean(np.array(cv_lst)))
    
    ### features importance
    feat_impor_tuple = [(model.feature_importances_[idx],data.columns[idx]) for idx in range(X.shape[1])]
    feat_impor_sort = sorted(feat_impor_tuple, reverse = True)
    print(feat_impor_sort)
    for tup in feat_impor_sort:
        print('%s, %f' % (tup[1], tup[0]))
def xgb_model(data):
    data_sf = data.values.copy()
    np.random.shuffle(data_sf)
    X,y = data_sf[:,:-1], data_sf[:,-1]
    lb = preprocessing.LabelEncoder()
    y = lb.fit_transform( y)
    dtrain = xgb.DMatrix(X[700:], y[700:])
    deval = xgb.DMatrix(X[:700], y[:700])
    watch_list = [ (dtrain, 'train'), (deval, 'eval')]
    xgb_params = {'silent'  : 1,
                  'eta': 0.0002, 'gamma' : 1.0, 'max_depth' : 20, 'subsample' : 0.7,'min_child_weight' : 5,
                  'colsample_bytree' : 0.9,
                  'objective' : 'multi:softmax','num_class' : 3, 'eval_metric': 'merror'}
    model = xgb.train(xgb_params, dtrain, 10000, watch_list, early_stopping_rounds = 70)   
def std_ss_dur_model():
    data = pd.read_csv('student_ss_dur_feats_2.csv')
    X,y = data.values[:,:-1], data.duration.values
    # features engineering
#     data.dur_from_last = data.dur_from_last.map(lambda x : int(x / 3600))
    model = tree.DecisionTreeClassifier(criterion='gini', splitter ='best', max_depth = None, 
                                        min_samples_split = 10,
                                        max_features = 'sqrt', random_state=None, max_leaf_nodes=None)
#     X_sel = eliminate_recursive(X,y,model, data.columns)

    # build model and evaluate
#     print(cross_val(X_sel, y, model, cv= 5, print_cfmat = True))
    tree_model(data)
     
    
if __name__ == '__main__':
    std_ss_dur_model()
    
    