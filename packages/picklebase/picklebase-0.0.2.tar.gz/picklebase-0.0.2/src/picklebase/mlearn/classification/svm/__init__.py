import picklebase as __pp
from sklearn.svm import SVC as __model

class params :
    kernel = 'rbf' # {‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’}, default=’rbf’
    C = 1.0 # float, default=1.0
    gamma = 'scale' # {‘scale’, ‘auto’} or float, default=’scale’
    probability = True # bool, default=False -> in picklebase it is always True
    degree = 3 # int, default=3
    coef0 = 0.0 # float, default=0.0
    shrinking = True # bool, default=True
    tol = 1e-3 # float, default=1e-3
    cache_size = 200 # float, default=200
    class_weight = None # dict or ‘balanced’, default=None
    max_iter = -1 # int, default=-1 fro no limit
    decision_function_shape = 'ovr' # {‘ovo’, ‘ovr’}, default=’ovr’

def __modeler (b_params='') :
    if (b_params == '') :
        loc_params = params
    else :
        loc_params = b_params
    if (b_params != False) :
        loc_modeler = __model( \
            kernel = loc_params.kernel, \
            C = loc_params.C, \
            gamma = loc_params.gamma, \
            probability = loc_params.probability, \
            degree = loc_params.degree, \
            coef0 = loc_params.coef0, \
            shrinking = loc_params.shrinking, \
            tol = loc_params.tol, \
            cache_size = loc_params.cache_size, \
            class_weight = loc_params.class_weight, \
            max_iter = loc_params.max_iter, \
            decision_function_shape = loc_params.decision_function_shape, \
        )
    else :
        loc_modeler = __model()
    return loc_modeler

def fit (a_data,b_params='',b_threshold=0.5) :
    loc_modeler = __modeler(b_params=b_params)
    return __pp.mlearn.classification.__base.__run(loc_modeler,a_x_train=a_data.x_train,a_x_test=a_data.x_test,a_y_train=a_data.y_train,a_y_test=a_data.y_test,b_threshold=b_threshold)

def bagging (a_data,b_params='') :
    loc_modeler = __modeler(b_params=b_params)
    return __pp.mlearn.classification.__base.__bagging(loc_modeler,a_data,b_params)

def grid_search_cv (a_data,b_params) :
    loc_modeler = __modeler(b_params=b_params)
    return __pp.mlearn.classification.__base.__grid_search_cv(loc_modeler,a_data,b_params)

def predict (a_model,a_data,b_features='',b_threshold=0.5) :
    return __pp.mlearn.classification.__base.__predict(a_model=a_model,a_data=a_data,b_features=b_features,b_threshold=b_threshold)
