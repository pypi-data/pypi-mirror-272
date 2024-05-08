import pandas as __pd
import matplotlib.pyplot as __plt
import seaborn as __sns

import picklebase as __ap

from . import outlier

class __data :
    q1 = None
    q2 = None
    q3 = None
    iqr = None
    lower_fence = None
    upper_fence = None
    n = None
    lower_outlier_count = None
    upper_outlier_count = None
    all_outlier_count = None
    lower_outlier_percent = None
    upper_outlier_percent = None
    all_outlier_percent = None
    report = None

def show (a_data,a_column) :
    loc_plot = __sns.boxplot(x=a_data[a_column])
    loc_data = __data()
    loc_data.q1 = a_data[a_column].quantile(0.25)
    loc_data.q2 = a_data[a_column].quantile(0.50)
    loc_data.q3 = a_data[a_column].quantile(0.75)
    loc_data.iqr = loc_data.q3 - loc_data.q1
    loc_data.lower_fence = loc_data.q1 - (1.5 * loc_data.iqr)
    loc_data.upper_fence = loc_data.q3 + (1.5 * loc_data.iqr)
    loc_data.n = len(a_data)
    loc_data.lower_outlier_count = __ap.data.row.value(a_data=a_data,a_column=a_column,a_value=loc_data.lower_fence,b_method='<',b_action='count')
    loc_data.upper_outlier_count = __ap.data.row.value(a_data=a_data,a_column=a_column,a_value=loc_data.upper_fence,b_method='>',b_action='count')
    loc_data.all_outlier_count = loc_data.lower_outlier_count + loc_data.upper_outlier_count
    loc_data.lower_outlier_percent = round(loc_data.lower_outlier_count/loc_data.n*100.00,2)
    loc_data.upper_outlier_percent = round(loc_data.upper_outlier_count/loc_data.n*100.00,2)
    loc_data.all_outlier_percent = round(loc_data.all_outlier_count/loc_data.n*100.00,2)
    loc_data_to_report = {
        'key': ['Q1','Q2','Q3','IQR','Lower Fence','Upper Fence', \
            'n','Lower Outlier(s) Count','Upper Outlier(s) Count','All Outlier(s) Count'], \
        'value':[loc_data.q1,loc_data.q2,loc_data.q3,loc_data.iqr,loc_data.lower_fence,loc_data.upper_fence, \
            loc_data.n,loc_data.lower_outlier_count,loc_data.upper_outlier_count,loc_data.all_outlier_count], \
        'note': ['','Median','','','Lower Bound','Upper Bound', \
            'Number of data',str(loc_data.lower_outlier_percent) + '%',str(loc_data.upper_outlier_percent) + '%',str(loc_data.all_outlier_percent) + '%']
    } 
    loc_data.report = __pd.DataFrame(loc_data_to_report)
    return loc_plot,loc_data

def shows (a_data,a_column_x,a_column_y,b_group_by='',b_orientation='') :
    """
    b_orientation = '', 'v' or 'h'
    """
    if b_orientation == 'v' :
        if b_group_by == '' :
            loc_plot = __sns.boxplot(data=a_data,y=a_column_x,x=a_column_y,orient=b_orientation)
        else :
            loc_plot = __sns.boxplot(data=a_data,y=a_column_x,x=a_column_y,hue=b_group_by,orient=b_orientation)            
    else :
        if b_group_by == '' :
            loc_plot = __sns.boxplot(data=a_data,x=a_column_x,y=a_column_y,orient=b_orientation)
        else :
            loc_plot = __sns.boxplot(data=a_data,x=a_column_x,y=a_column_y,hue=b_group_by,orient=b_orientation)
    return loc_plot
    
    # function to draw points on the plot
    # loc_plot = __sns.swarmplot(data=a_data,y=a_column_x,x=a_column_y,orient=b_orientation,color=".25")

'''    
Q1 = df["COLUMN_NAME"].quantile(0.25)
Q3 = df["COLUMN_NAME"].quantile(0.75)
IQR = Q3 - Q1
Lower_Fence = Q1 - (1.5 * IQR)
Upper_Fence = Q3 + (1.5 * IQR)
'''