from sklearn.ensemble import BaggingClassifier as __bagclass
from sklearn.model_selection import GridSearchCV as __gridscv

import sklearn.metrics as __metrics
import matplotlib.pyplot as __plt
import scikitplot as __skplt
import pandas as __pd
import numpy as __np

import picklebase as __pp

class __data :
    y_test_actual = None
    y_test_pred = None
    y_test_pred_proba_all = None
    fpr = None # false positive rate
    tpr = None # true positive rate
    ix_roc = None # index fpr & tpr
    best_threshold = None
    prc_precisions = None
    prc_recalls = None
    prc_fscores = None
    prc_thresholds = None

class __best_threshold :
    value : None
    precision = None
    recall = None

class __result :
    model = None
    evals = {}
    report = None
    best_threshold = None
    data = None

class __result_bagging :
    model = None
    train_score = None
    test_score = None

class __result_grid_search_cv :
    model = None
    evals = None
    best_estimator = None
    best_score = None
    best_params = None

class __result_predict :
    probability = None
    prediction = None
    worksheet = None


def __run (a_model,a_x_train,a_x_test,a_y_train,a_y_test,b_threshold=0.5) :
    
    loc_model = a_model
    loc_model.fit(a_x_train,a_y_train.values.ravel())
       
    loc_prob_train = loc_model.predict_proba(a_x_train)[:,1]
    if b_threshold == 0.5 :
        loc_predic_train = loc_model.predict(a_x_train)
    else :
        loc_predic_train = (loc_prob_train >= b_threshold).astype(int)

    loc_prob_test = loc_model.predict_proba(a_x_test)[:,1]
    if b_threshold == 0.5 :
        loc_predic_test = loc_model.predict(a_x_test)
    else :
        loc_predic_test = (loc_prob_test >= b_threshold).astype(int)

    loc_report = __metrics.classification_report(a_y_test,loc_predic_test)
    
    loc_predict_proba_all = loc_model.predict_proba(a_x_test)
    loc_predict_proba = loc_model.predict_proba(a_x_test)[:,1]
    # calculate roc curves : false positive rate, true positive rate
    loc_fpr, loc_tpr, loc_thresholds = __metrics.roc_curve(a_y_test,loc_predict_proba)
    # calculate the g-mean for each threshold
    loc_gmeans = __np.sqrt(loc_tpr * (1-loc_fpr))
    # locate the index of the largest g-mean
    ix_roc = __np.argmax(loc_gmeans)
    loc_best_threshold = loc_thresholds[ix_roc]
    
    # calculate prc (precision-recall curve)
    loc_prc_precisions,loc_prc_recalls,loc_prc_thresholds = __metrics.precision_recall_curve(a_y_test,loc_predict_proba)
    loc_prc_fscores = (2 * loc_prc_precisions * loc_prc_recalls) / (loc_prc_precisions + loc_prc_recalls)
        
    loc_result = __result()
    loc_result.model = loc_model
    loc_result.evals['train'] = __pp.__eval.evals(a_y_train.to_numpy(),loc_predic_train)
    loc_result.evals['test'] = __pp.__eval.evals(a_y_test.to_numpy(),loc_predic_test)
    loc_result.report = loc_report
    loc_result.best_threshold = loc_best_threshold
    
    loc_result.data = __data()
    loc_result.data.y_test_actual = a_y_test
    loc_result.data.y_test_pred = loc_predic_test
    loc_result.data.y_test_pred_proba_all = loc_predict_proba_all
    loc_result.data.fpr = loc_fpr # false positive rate
    loc_result.data.tpr = loc_tpr # true positive rate
    loc_result.data.ix_roc = ix_roc # index fpr & tpr
    loc_result.data.prc_precisions = loc_prc_precisions
    loc_result.data.prc_recalls = loc_prc_recalls
    loc_result.data.prc_fscores = loc_prc_fscores
    loc_result.data.prc_thresholds = loc_prc_thresholds

    return loc_result


def __bagging (a_modeler,a_data,b_params='') :
    loc_model = __bagclass(base_estimator=a_modeler,n_estimators=100,bootstrap=True,n_jobs=1,random_state=42)
    loc_model.fit(a_data.x_train,a_data.y_train.values.ravel())
    loc_result = __result_bagging()
    loc_result.model = loc_model
    loc_result.train_score = loc_model.score(a_data.x_train,a_data.y_train)
    loc_result.test_score = loc_model.score(a_data.x_test,a_data.y_test)
    return loc_result


def __grid_search_cv (a_modeler,a_data,b_params) :
    loc_x = __pp.data.union(a_data.x_train,a_data.x_test)
    loc_y = __pp.data.union(a_data.y_train,a_data.y_test)

    loc_parameters = {}

    loc_model = __gridscv(a_modeler,loc_parameters,n_jobs=-1)
    loc_model.fit(loc_x,loc_y.values.ravel())
    loc_predict = loc_model.predict(loc_x)

    loc_result = __result_grid_search_cv()
    loc_result.model = loc_model
    loc_result.evals = __pp.__eval.evals(loc_y.to_numpy(),loc_predict)
    loc_result.best_estimator = loc_model.best_estimator_
    loc_result.best_score = loc_model.best_score_
    loc_result.best_params = loc_model.best_params_
    
    return loc_result


def __predict (a_model,a_data,b_features='',b_threshold=0.5) :
    if b_features == '' :
        loc_features = a_data.columns
    else :
        loc_features = b_features
        
    loc_prob_y = a_model.model.predict_proba(a_data[loc_features])[:,1]
    if b_threshold == 0.5 :
        loc_pred_y = a_model.model.predict(a_data[loc_features])
    else :
        loc_pred_y = (loc_prob_y >= b_threshold).astype(int)
        
    loc_probability = __pd.DataFrame(loc_prob_y,columns=['__prob_y'])
    loc_prediction = __pd.DataFrame(loc_pred_y,columns=['__pred_y'])
    
    loc_merge = a_data
    loc_merge = __pd.merge(loc_merge,loc_probability,left_index=True,right_index=True)
    loc_merge = __pd.merge(loc_merge,loc_prediction,left_index=True,right_index=True)

    loc_result_predict = __result_predict()
    loc_result_predict.probability = loc_probability
    loc_result_predict.prediction = loc_prediction
    loc_result_predict.worksheet = loc_merge
    
    return loc_result_predict


