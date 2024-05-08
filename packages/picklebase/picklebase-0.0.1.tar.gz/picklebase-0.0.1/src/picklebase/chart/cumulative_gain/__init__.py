import scikitplot as __skplt

def show (a_model) :

    loc_y_test = a_model.data.y_test_actual
    loc_y_pred_proba_all = a_model.data.y_test_pred_proba_all # all means 2 values included : positive, negative
    
    loc_plt = __skplt.metrics.plot_cumulative_gain(loc_y_test,loc_y_pred_proba_all).figure
    __skplt.plotters.plt.close()

    return loc_plt