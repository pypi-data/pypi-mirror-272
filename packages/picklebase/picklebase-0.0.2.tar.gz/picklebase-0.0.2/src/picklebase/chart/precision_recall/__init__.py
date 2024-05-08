import matplotlib.pyplot as __plt
import numpy as __np

import picklebase as __ap

def show (a_model) :

    loc_precisions = a_model.data.prc_precisions
    loc_recalls = a_model.data.prc_recalls
    loc_ix = __np.argmax(a_model.data.prc_fscores)
    
    loc_plot = __plt.figure()
    __plt.plot(loc_recalls,loc_precisions,marker='.',label='Plot')
    __plt.scatter(loc_recalls[loc_ix],loc_precisions[loc_ix],marker='o',color='black',label='Best')
    __plt.xlabel('Recall')
    __plt.ylabel('Precision')
    __plt.title('Precision-Recall Curve')
    __plt.legend(loc="upper right")
    __plt.close()

    return loc_plot

def precisions (a_model) :
    return __ap.data.array_to_df(a_model.data.prc_precisions,['precisions'])

def recalls (a_model) :
    return __ap.data.array_to_df(a_model.data.prc_recalls,['recalls'])

def fscores (a_model) :
    return __ap.data.array_to_df(a_model.data.prc_fscores,['fscores'])

def thresholds (a_model) :
    return __ap.data.array_to_df(a_model.data.prc_thresholds,['thresholds'])

def data (a_model) :
    return __ap.data.merge(precisions(a_model),recalls(a_model),fscores(a_model),thresholds(a_model))

def best_threshold (a_model) :
    return a_model.data.prc_thresholds[__np.argmax(a_model.data.prc_fscores)]

def best_fscore (a_model) :
    return a_model.data.prc_fscores[__np.argmax(a_model.data.prc_fscores)]
