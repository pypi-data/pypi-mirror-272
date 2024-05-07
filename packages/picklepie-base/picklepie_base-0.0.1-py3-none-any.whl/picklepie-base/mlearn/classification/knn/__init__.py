import picklepie as __pp
from sklearn.neighbors import KNeighborsClassifier as __model

class params :
    n_neighbors = 5 # int, default=5
    weights = 'uniform' # {‘uniform’, ‘distance’} or callable, default=’uniform’
    algorithm = 'auto' # {‘auto’, ‘ball_tree’, ‘kd_tree’, ‘brute’}, default=’auto’
    leaf_size = 30 # int, default=30
    p = 2 # int, default=2
    metric = 'minkowski' # str or callable, default=’minkowski’
    metric_params = None # dict, default=None
    n_jobs = 1 # int, default=None

def __modeler (b_params='') :
    if (b_params == '') :
        loc_params = params
    else :
        loc_params = b_params
    if (b_params != False) :
        loc_modeler = __model( \
            n_neighbors = loc_params.n_neighbors, \
            weights = loc_params.weights, \
            algorithm = loc_params.algorithm, \
            leaf_size = loc_params.leaf_size, \
            p = loc_params.p, \
            metric = loc_params.metric, \
            metric_params = loc_params.metric_params, \
            n_jobs = loc_params.n_jobs, \
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

