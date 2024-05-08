import pandas as __pd
from numpy import loadtxt as __loadtxt
import pyodbc as __odbc

import twint as __tw
import nest_asyncio as __na

import picklebase as __pp

def array (a_file,b_separator=',') :
    # no-header file
    return __loadtxt(a_file,delimiter=b_separator)

def csv (a_file,b_separator=',') :
    return __pd.read_csv(a_file,sep=b_separator)

# https://www.pythontutorial.net/python-basics/python-read-text-file/

def content (a_file,a_type='') :
    # all string content
    loc_file = open(a_file)
    if (a_type == '' or a_type == 'plain') :
        loc_return = loc_file.read()
    elif (a_type == 'lines') :
        loc_return = loc_file.readlines()
    return loc_return

def odbc (a_dsn,a_userid,a_password,a_sql) :
    loc_conn = __odbc.connect('DSN=' + a_dsn + ';UID=' + a_userid + ';PWD=' + a_password)
    return __pd.read_sql(a_sql,loc_conn)

def txt (a_file,b_separator=',') :
    return __pd.read_csv(a_file,sep=b_separator)

def twitter (b_user_name='',b_search_keyword='',b_since='',b_until='',b_lang='',b_limit=100,b_save_to_file=True,b_file='pickle_twitter.csv') :
    __na.apply()
    # configure
    c = __tw.Config()
    if (b_user_name != '') :
        c.Username = b_user_name
    if (b_search_keyword != '') :
        c.Search = b_search_keyword
    if (b_limit != '') :
        c.Limit = b_limit
    if (b_since != '') :
        c.Since = b_since # example "2021-03-01"
    if (b_until != '') :
        c.Until = b_until # example "2021-03-31"
    if (b_lang != '') :
        c.Lang = b_lang # example "id","en"
    # c.Translate = True
    # c.TranslateDest = "en"
    if (b_save_to_file == True) :
        c.Store_csv = b_save_to_file
    if (b_file != '') :
        c.Output = b_file
    if (b_save_to_file == True) and (b_file != '') :
        __pp.base.file.delete(b_file)
    # run
    __tw.run.Search(c)

def xls (a_file,a_sheet) :
    return __pd.read_excel(a_file,sheet_name=a_sheet)

