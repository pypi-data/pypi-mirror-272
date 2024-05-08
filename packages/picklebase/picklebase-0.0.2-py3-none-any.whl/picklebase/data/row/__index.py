import picklebase as __ap

def int_ (a_data,a_index) :
    loc_data_as_series = a_data.iloc[a_index]
    return __ap.data.series.df(loc_data_as_series)

def list_ (a_data,a_index) :
    i = 0
    for loc_index in a_index :
        i += 1
        loc_data_as_series = a_data.iloc[loc_index]
        if i == 1 :
            loc_df = __ap.data.series.df(loc_data_as_series)
        else :
            loc_df = __ap.data.union(loc_df,__ap.data.series.df(loc_data_as_series))
    return loc_df
