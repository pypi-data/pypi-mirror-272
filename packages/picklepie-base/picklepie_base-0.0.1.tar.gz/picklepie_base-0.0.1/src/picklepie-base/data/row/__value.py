import numpy as __np
import picklepie as __ap

def eq_not_list (a_data,a_column,a_value) :
    return a_data.loc[a_data[a_column] == a_value]

def eq_list (a_data,a_column,a_value) :
    i = 0
    for loc_value in a_value :
        i += 1
        if i == 1 :
            loc_result = a_data.loc[a_data[a_column] == loc_value]
        else :
            loc_result = __ap.data.union(loc_result,a_data.loc[a_data[a_column] == loc_value])
    return loc_result
    
def gt (a_data,a_column,a_value) :
    return a_data.loc[a_data[a_column] > a_value]

def ge (a_data,a_column,a_value) :
    return a_data.loc[a_data[a_column] >= a_value]

def lt (a_data,a_column,a_value) :
    return a_data.loc[a_data[a_column] < a_value]

def le (a_data,a_column,a_value) :
    return a_data.loc[a_data[a_column] <= a_value]

def nearest_not_list (a_data,a_column,a_value) :
    loc_array = __ap.data.df_to_array(a_data[a_column])
    loc_difference_array = __np.absolute(loc_array - a_value)
    loc_index = loc_difference_array.argmin()
    loc_row = __ap.data.row.index(a_data=a_data,a_index=loc_index)
    loc_value_at_df = loc_row.at[loc_index,a_column]
    return __ap.data.row.value(a_data=a_data,a_column=a_column,a_value=loc_value_at_df,b_method='=')
    
def nearest_list (a_data,a_column,a_value) :
    i = 0
    for loc_value in a_value :
        loc_array = __ap.data.df_to_array(a_data[a_column])
        loc_difference_array = __np.absolute(loc_array - loc_value)
        loc_index = loc_difference_array.argmin()
        loc_row = __ap.data.row.index(a_data=a_data,a_index=loc_index)
        loc_value_at_df = loc_row.at[loc_index,a_column]
        i += 1
        if i == 1 :
            loc_result = __ap.data.row.value(a_data=a_data,a_column=a_column,a_value=loc_value_at_df,b_method='=')
        else :
            loc_result = __ap.data.union(loc_result,__ap.data.row.value(a_data=a_data,a_column=a_column,a_value=loc_value_at_df,b_method='='))
    return loc_result
    
