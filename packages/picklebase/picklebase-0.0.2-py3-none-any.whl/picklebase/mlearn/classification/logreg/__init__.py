import picklebase as __pp
from sklearn.linear_model import LogisticRegression as __model

class params :
    penalty = 'l2' # {‘l1’, ‘l2’, ‘elasticnet’, ‘none’}, default=’l2’
    dual = False # bool, default=False
    tol = 1e-4 # float, default=1e-4
    C = 1.0 # float, default=1.0
    fit_intercept = True # bool, default=True
    intercept_scaling = 1 # float, default=1
    class_weight = None # dict or ‘balanced’, default=None
    random_state = None # int, RandomState instance, default=None
    solver = 'lbfgs' # {‘newton-cg’, ‘lbfgs’, ‘liblinear’, ‘sag’, ‘saga’}, default=’lbfgs’
    max_iter = 5000 # int, default=100
    multi_class = 'auto' # {‘auto’, ‘ovr’, ‘multinomial’}, default=’auto’
    verbose = 0 # int, default=0
    warm_start = False # bool, default=False
    n_jobs = 1 # int, default=None
    l1_ratio = None # float, default=None

def __modeler (b_params='') :
    if (b_params == '') :
        loc_params = params
    else :
        loc_params = b_params
    if (b_params != False) :
        loc_modeler = __model( \
            penalty = loc_params.penalty, \
            dual = loc_params.dual, \
            tol = loc_params.tol, \
            C = loc_params.C, \
            fit_intercept = loc_params.fit_intercept, \
            intercept_scaling = loc_params.intercept_scaling, \
            class_weight = loc_params.class_weight, \
            random_state = loc_params.random_state, \
            solver = loc_params.solver, \
            max_iter = loc_params.max_iter, \
            multi_class = loc_params.multi_class, \
            verbose = loc_params.verbose, \
            warm_start = loc_params.warm_start, \
            n_jobs = loc_params.n_jobs, \
            l1_ratio = loc_params.l1_ratio, \
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

