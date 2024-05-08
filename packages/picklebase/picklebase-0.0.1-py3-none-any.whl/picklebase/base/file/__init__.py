import os as __os

def delete (a_file) :
    if __os.path.exists(a_file) :
        __os.remove(a_file)
