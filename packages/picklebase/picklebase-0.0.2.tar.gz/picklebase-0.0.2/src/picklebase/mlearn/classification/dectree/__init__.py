import picklebase as __pp
from sklearn.tree import DecisionTreeClassifier as __model

class params :
    criterion = 'gini' # {“gini”, “entropy”}, default=”gini”
    splitter = 'best' # {“best”, “random”}, default=”best”
    max_depth = None # int, default=None
    min_samples_split = 2 # int or float, default=2
    min_samples_leaf = 1 # int or float, default=1
    min_weight_fraction_leaf = 0.0 # float, default=0.0
    max_features = None # int, float or {“auto”, “sqrt”, “log2”}, default=None
    random_state = None # int, RandomState instance or None, default=None
    max_leaf_nodes = None # int, default=None
    min_impurity_decrease = 0.0 # float, default=0.0
    # min_impurity_split = 0 # float, default=0 # deprecated
    class_weight = None # dict, list of dict or “balanced”, default=None
    ccp_alpha = 0.0 # non-negative float, default=0.0
    
def __modeler (b_params='') :
    if (b_params == '') :
        loc_params = params
    else :
        loc_params = b_params
    if (b_params != False) :
        loc_modeler = __model( \
            criterion = loc_params.criterion, \
            splitter = loc_params.splitter, \
            max_depth = loc_params.max_depth, \
            min_samples_split = loc_params.min_samples_split, \
            min_samples_leaf = loc_params.min_samples_leaf, \
            min_weight_fraction_leaf = loc_params.min_weight_fraction_leaf, \
            max_features = loc_params.max_features, \
            random_state = loc_params.random_state, \
            max_leaf_nodes = loc_params.max_leaf_nodes, \
            min_impurity_decrease = loc_params.min_impurity_decrease, \
            class_weight = loc_params.class_weight, \
            ccp_alpha = loc_params.ccp_alpha, \
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

