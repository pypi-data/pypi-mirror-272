import scikitplot as __skplt

import picklepie as __ap

class __data :
    # xy = None
    xy = {}

def show (a_model) :

    loc_y_test = a_model.data.y_test_actual
    loc_y_pred_proba_all = a_model.data.y_test_pred_proba_all # all means 2 values included : positive, negative
    
    loc_plt = __skplt.metrics.plot_lift_curve(loc_y_test,loc_y_pred_proba_all).figure
    __skplt.plotters.plt.close()
    
    loc_data = __data()
    loc_data.xy[0] = __get_data(loc_plt,0)
    loc_data.xy[1] = __get_data(loc_plt,1)
    '''
    loc_ax = loc_plt.gca()
    loc_line = loc_ax.lines[1]
    loc_data_x = __ap.data.array_to_df(a_array=loc_line.get_xdata(),b_as_column=['x'])
    loc_data_y = __ap.data.array_to_df(a_array=loc_line.get_ydata(),b_as_column=['y'])
    loc_data.xy = __ap.data.merge(loc_data_x,loc_data_y)
    '''
    
    return loc_plt,loc_data

def __get_data (a_plot,a_series) :
    loc_ax = a_plot.gca()
    loc_line = loc_ax.lines[a_series]
    loc_data_x = __ap.data.array_to_df(a_array=loc_line.get_xdata(),b_as_column=['x'])
    loc_data_y = __ap.data.array_to_df(a_array=loc_line.get_ydata(),b_as_column=['y'])
    return __ap.data.merge(loc_data_x,loc_data_y)

