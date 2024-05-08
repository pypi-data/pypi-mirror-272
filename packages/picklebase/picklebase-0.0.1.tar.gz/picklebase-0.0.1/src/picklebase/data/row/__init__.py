import numpy as __np
import picklepie as __ap
from . import __index
from . import __value

def count (a_data) :
    return len(a_data)    
    
# check if there are duplicated rows
def duplicate (a_data) :
    return a_data.duplicated(keep=False).sum()    
    
def index (a_data,a_index) :
    '''
    Show row by index
    '''
    if type(a_index) == int or type(a_index) == __np.int64:
        loc_return = __index.int_(a_data,a_index)
    elif type(a_index) == list :
        loc_return = __index.list_(a_data,a_index)
    return loc_return

def value (a_data,a_column,a_value,b_method='=',b_action='') :
    '''
    Show row by value of column
    '''
    if b_method == '=' :
        if type(a_value) != list :
            loc_result = __value.eq_not_list(a_data,a_column,a_value)
        else : # list
            loc_result = __value.eq_list(a_data,a_column,a_value)
    elif b_method == '>' : # greater than
        loc_result = __value.gt(a_data,a_column,a_value)    
    elif b_method == '>=' : # greater than or equal to
        loc_result = __value.ge(a_data,a_column,a_value)    
    elif b_method == '<' : # less than
        loc_result = __value.lt(a_data,a_column,a_value)    
    elif b_method == '<=' : # less than or equal to
        loc_result = __value.le(a_data,a_column,a_value)    
    elif b_method == 'nearest' :
        if type(a_value) != list :
            loc_result = __value.nearest_not_list (a_data,a_column,a_value)
        else : # list
            loc_result = __value.nearest_list (a_data,a_column,a_value)
    if b_action == 'count' :
        loc_return = len(loc_result)
    else :
        loc_return = loc_result
    return loc_return
    