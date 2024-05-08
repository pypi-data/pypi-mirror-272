import pandas as __pd

def count (a_data) :
    return len(a_data.columns)    
    
def data_type (a_data) :
    return a_data.dtypes
    
def delete (a_data,a_column) :
    loc_data = a_data.drop(a_column, axis = 1)    
    return loc_data

def list_ (a_data) :
    return list(a_data)
    
def rename (a_data,a_new_names) :
    """
    Rename columns, always use []
    """
    a_data.columns = a_new_names
    
def to_float (a_data,a_cols) :
    """
    Convert column data type to float or numeric
    Always use [] for a_cols
    """
    a_data[a_cols] = __pd.to_numeric(a_data[a_cols])
    
def to_int (a_data,a_cols) :
    """
    Convert column data type to integer
    Always use [] for a_cols
    """
    for loc_col in a_cols :
        a_data[loc_col] = a_data[loc_col].astype(int)
