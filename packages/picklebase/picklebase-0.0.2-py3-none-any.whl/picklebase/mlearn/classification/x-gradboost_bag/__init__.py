# https://www.pluralsight.com/guides/ensemble-methods:-bagging-versus-boosting

from sklearn.ensemble import GradientBoostingClassifier as __model
from sklearn.ensemble import BaggingClassifier as __bagging
import sklearn.metrics as __metrics
import pandas as __pd

import picklebase as __ap

class __result :
    model = None
    train_score = None
    test_score = None

class __result_predict :
    prediction = None # target value prediction
    worksheet = None # features data and target value prediction

def run (a_x_train,a_x_test,a_y_train,a_y_test) :

    loc_model = __bagging(base_estimator=__model(),n_estimators=100,bootstrap=True,n_jobs=1,random_state=42)
    loc_model.fit(a_x_train,a_y_train.values.ravel())
    
    loc_result = __result()
    loc_result.model = loc_model
    loc_result.train_score = loc_model.score(a_x_train,a_y_train)
    loc_result.test_score = loc_model.score(a_x_test,a_y_test)
    
    return loc_result

def predict (a_model,a_data,a_features='') :

    if a_features == '' :
        loc_features = a_data.columns
    else :
        loc_features = a_features
        
    loc_prediction = __pd.DataFrame(a_model.model.predict(a_data[loc_features]),columns=['__pred_y'])
    loc_merge = __pd.merge(a_data,loc_prediction,left_index=True,right_index=True)
    
    loc_result_predict = __result_predict()
    loc_result_predict.prediction = loc_prediction
    loc_result_predict.worksheet = loc_merge
    
    return loc_result_predict
