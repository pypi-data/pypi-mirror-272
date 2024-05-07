from . import column
from . import create
from . import load
from . import null
from . import row
from . import save
from . import series
from . import stat
from . import value

import pandas as __pd
from sklearn.preprocessing import MinMaxScaler as __minmax
from sklearn.preprocessing import StandardScaler as __standard
from imblearn.over_sampling import SMOTE as __smote

import picklepie as __pp

def array_merge (*a_array) :
    """
    Merge arrays
    """
    i = 0
    for loc_array in a_array :
        i += 1
        if i == 1 :
            loc_new_array = loc_array
        else :
            loc_new_array = loc_new_array + loc_array
    return loc_new_array

def array_to_df (a_array,b_as_column='') :
    """
    This will convert array to pandas dataframe
    use [] for b_as_column
    """
    if b_as_column == '' :
        loc_result = __pd.DataFrame(data=a_array)
    else :
        loc_result = __pd.DataFrame(data=a_array,columns=b_as_column)
    return loc_result

def array_to_str (a_array,b_delimiter=' ') :
    return b_delimiter.join(a_array)

def cell_value (a_data='',a_index='',a_column='') :
    return a_data.iloc[a_index][a_column]

def copy (a_data) :
    """
    This function is aimed to copy one dataframe to another dataframe.
    This will prevent a dataframe to be affected by another dataframe.
    """
    return a_data.copy()

def dict_to_array (a_dict) :
    return list(a_dict.items())

def dict_to_df (a_dict) :
    loc_array = list(a_dict.items())
    return __pp.data.array_to_df(loc_array,b_as_column=['Key','Value'])

def df_to_array (a_data,b_type='numpy',b_column='') :
    if (b_type == 'list') :
        if (b_column != '') :
            loc_data = a_data[b_column].values.tolist()
        else :
            loc_data = a_data.values.tolist()
    elif (b_type == 'numpy') :
        loc_data = a_data.to_numpy()
    else :
        loc_data = a_data.to_numpy()
    return loc_data

def deselect (a_data,a_column) :
    """
    Not to select a_column in a_data
    Get remaining columns
    Use [] in a_column
    """
    loc_data = a_data.drop(a_column,axis = 1)    
    return loc_data

def dimension (a_data) :
    print (str(row.count(a_data)) + ' rows x ' + str(column.count(a_data)) + ' columns')

def frozenset_to_array (a_frozen_set='') :
    return list(a_frozen_set)
    
def frozenset_to_df (a_frozen_set='') :
    loc_array = __pp.data.frozenset_to_array(a_frozen_set)
    return __pp.data.array_to_df(loc_array)
    
def groupby (a_data,a_column,b_method='count') :
    if b_method == 'count' :
        loc_result = a_data.groupby(a_column).count() 
    elif b_method == 'mean' :
        loc_result = a_data.groupby(a_column).mean() 
    return loc_result
    # for future dev : 
    # from collections import Counter
    # print(sorted(Counter(a_data[a_column]).items()))
    
def info (a_data) :
    '''
    Deprecated
    '''
    return a_data.info()
    
def map (a_data,a_column,a_old,a_new) :
    """
    Map value a_old of a_column in a_data with a_new
    Use [] in a_old and a_new
    a_new must match in length with a_old
    """
    loc_new_data = a_data
    a_data[a_column].replace(a_old,a_new,inplace=True)

def merge (*a_data) :
    """
    Merge dataframes by index
    """
    i = 0
    for loc_data in a_data :
        i += 1
        if i == 1 :
            loc_new_df = loc_data
        else :
            loc_new_df = __pd.merge(loc_new_df,loc_data,left_index=True,right_index=True)
    return loc_new_df

def normalize (a_data,a_column,b_method='MinMax') :
    """
    This function is aimed to normalize data.
    Use [] when passing parameter to a_column.
    Options for b_method = 'MinMax' (default),'Standard'
    Return directly to a_data[a_column]
    """
    if b_method == 'MinMax' :
        loc_scaler = __minmax()
        a_data[a_column] = loc_scaler.fit_transform(a_data[a_column])
    elif b_method == 'Standard' :
        loc_scaler = __standard()
        a_data[a_column] = loc_scaler.fit_transform(a_data[a_column])

def replace (a_data,a_column,a_old,a_new) :
    """
    Replace value a_old of a_column in a_data with a_new
    Use [] in a_old and a_new
    a_new must match in length with a_old
    """
    loc_new_data = a_data
    a_data[a_column].replace(a_old,a_new,inplace=True)
        
def sample (a_data,a_row=5) :
    return a_data.head(a_row)

def schema (a_data) :
    return a_data.info()

def select (a_data,a_column) :
    """
    Select a_column in a_data
    Use [] in a_column
    """
    return a_data[a_column]
                
def show (a_data,a_index_begin,a_index_end) :
    x = 0
    for i in range(0,len(a_data)) :
        if i >= a_index_begin and i <= a_index_end :
            x += 1
            loc_this_df = __pp.data.row.index(a_data=a_data,a_index=i)
            if x == 1 :
                loc_new_data = loc_this_df
            else :
                loc_new_data = __pp.data.union(loc_new_data,loc_this_df)
    return loc_new_data
            
def smote (a_x,a_y) :
    loc_smote = __smote()
    loc_x = __pp.data.df_to_array(a_x)
    loc_y = __pp.data.df_to_array(a_y)
    loc_x_smote,loc_y_smote = loc_smote.fit_resample(loc_x,loc_y)
    loc_x_smote = __pp.data.array_to_df(loc_x_smote)
    loc_y_smote = __pp.data.array_to_df(loc_y_smote)
    return loc_x_smote,loc_y_smote

def top (a_data,a_row=5) :
    return a_data.head(a_row)
        
def type_ (a_data='') :
    return type(a_data)
        
def union (*a_data) :
    x = 0
    for loc_data in a_data :
        x += 1
        if x == 1 :
            loc_new_data = loc_data
        else :
            loc_new_data = __pd.concat([loc_new_data,loc_data])
    return loc_new_data
    
def unique (a_data,a_column) :
    """
    Get unique value of a_column in a_data (for int or float data type only)
    """
    return list(__np.unique(a_data[a_column]))
        
    
    
    
    

