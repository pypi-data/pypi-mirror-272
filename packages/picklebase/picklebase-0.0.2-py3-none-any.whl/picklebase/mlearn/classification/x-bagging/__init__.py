# https://www.pluralsight.com/guides/ensemble-methods:-bagging-versus-boosting


from sklearn.ensemble import BaggingClassifier as __bagging
from sklearn.tree import DecisionTreeClassifier as __dectree
from sklearn.ensemble import GradientBoostingClassifier as __gradboost
from sklearn.neighbors import KNeighborsClassifier as __knn
from sklearn.linear_model import LogisticRegression as __logreg
from sklearn.ensemble import RandomForestClassifier as __rndforest
from sklearn.svm import SVC as __svm
import pandas as __pd

import picklebase as __pp


class __result :
    model = None
    classifier = None
    train_score = None
    test_score = None


class __result_predict :
    prediction = None # target value prediction
    worksheet = None # features data and target value prediction


def run (a_classifier,a_x_train,a_x_test,a_y_train,a_y_test) :

    loc_true = True
    if (a_classifier == 'dectree') :
        loc_classifier = __dectree()
    elif (a_classifier == 'gradboost') :
        loc_classifier = __gradboost(n_estimators=100,learning_rate=1.0,max_depth=1)
    elif (a_classifier == 'knn') :
        loc_classifier = __knn(n_neighbors=3)
    elif (a_classifier == 'logreg') :
        loc_classifier = __logreg(solver="lbfgs",multi_class="auto",max_iter=5000)
    elif (a_classifier == 'rndforest') :
        loc_classifier = __rndforest()
    elif (a_classifier == 'svm') :
        loc_classifier = __svm()
    else :
        loc_classifier = ''
        loc_true = False

    if (loc_true == True) :
        loc_model = __bagging(base_estimator=loc_classifier,n_estimators=100,bootstrap=True,n_jobs=1,random_state=0)
        loc_model.fit(a_x_train,a_y_train.values.ravel())
        loc_result = __result()
        loc_result.model = loc_model
        loc_result.classifier = loc_classifier
        loc_result.train_score = loc_model.score(a_x_train,a_y_train) # Return the mean accuracy on the given test data and labels.
        loc_result.test_score = loc_model.score(a_x_test,a_y_test)
    else :
        loc_result = ''
    
    return loc_result


def runs (a_classifiers,a_x_train,a_x_test,a_y_train,a_y_test) :
    loc_result = []
    for loc_classifier in a_classifiers :
        loc_model = __pp.mlearn.classification.bagging.run(a_classifier=loc_classifier,a_x_train=a_x_train,\
            a_x_test=a_x_test,a_y_train=a_y_train,a_y_test=a_y_test)
        loc_result.append(loc_model)
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
