import picklepie as __ap

def show (a_data,a_column,a_box_plot_data,b_which='all') :
    if b_which == 'lower' :
        loc_return = __ap.data.row.value(a_data=a_data,a_column=a_column,a_value=a_box_plot_data.lower_fence,b_method='<')
    elif b_which == 'upper' :
        loc_return = __ap.data.row.value(a_data=a_data,a_column=a_column,a_value=a_box_plot_data.upper_fence,b_method='>')
    elif b_which == 'all' :
        loc_lower = __ap.data.row.value(a_data=a_data,a_column=a_column,a_value=a_box_plot_data.lower_fence,b_method='<')
        loc_upper = __ap.data.row.value(a_data=a_data,a_column=a_column,a_value=a_box_plot_data.upper_fence,b_method='>')
        loc_return = __ap.data.union(loc_lower,loc_upper)
    return loc_return
    