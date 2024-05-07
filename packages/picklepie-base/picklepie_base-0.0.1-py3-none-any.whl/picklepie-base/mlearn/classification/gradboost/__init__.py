import picklepie as __pp
from sklearn.ensemble import GradientBoostingClassifier as __model

class params :
    loss = 'deviance' # {‘deviance’, ‘exponential’}, default=’deviance’
    learning_rate = 0.1 # float, default=0.1
    n_estimators = 100 # int, default=100
    subsample = 1.0 # float, default=1.0
    criterion = 'friedman_mse' # {‘friedman_mse’, ‘mse’, ‘mae’}, default=’friedman_mse’
    min_samples_split = 2 # int or float, default=2
    min_samples_leaf = 1 # int or float, default=1
    min_weight_fraction_leaf = 0.0 # float, default=0.0
    max_depth = 3 # int, default=3
    min_impurity_decrease = 0.0 # float, default=0.0
    min_impurity_split = None # float, default=None
    init = None # testimator or ‘zero’, default=None
    random_state = None # int, RandomState instance or None, default=None
    max_features = None # {‘auto’, ‘sqrt’, ‘log2’}, int or float, default=None
    verbose = 0 # int, default=0
    max_leaf_nodes = None # int, default=None
    warm_start = False # bool, default=False
    validation_fraction = 0.1 # float, default=0.1
    n_iter_no_change = None # int, default=None
    tol = 1e-4 # float, default=1e-4
    ccp_alpha = 0.0 # non-negative float, default=0.0

def __modeler (b_params='') :
    if (b_params == '') :
        loc_params = params
    else :
        loc_params = b_params
    if (b_params != False) :
        loc_modeler = __model( \
            loss = loc_params.loss, \
            learning_rate = loc_params.learning_rate, \
            n_estimators = loc_params.n_estimators, \
            subsample = loc_params.subsample, \
            criterion = loc_params.criterion, \
            min_samples_split = loc_params.min_samples_split, \
            min_samples_leaf = loc_params.min_samples_leaf, \
            min_weight_fraction_leaf = loc_params.min_weight_fraction_leaf, \
            max_depth = loc_params.max_depth, \
            min_impurity_decrease = loc_params.min_impurity_decrease, \
            min_impurity_split = loc_params.min_impurity_split, \
            init = loc_params.init, \
            random_state = loc_params.random_state, \
            max_features = loc_params.max_features, \
            verbose = loc_params.verbose, \
            max_leaf_nodes = loc_params.max_leaf_nodes, \
            warm_start = loc_params.warm_start, \
            validation_fraction = loc_params.validation_fraction, \
            n_iter_no_change = loc_params.n_iter_no_change, \
            tol = loc_params.tol, \
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

