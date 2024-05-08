import matplotlib.pyplot as __plt
import scikitplot as __skplt
import sklearn.metrics as __metrics
import numpy as __np

def show (a_model) :
    
    loc_y_test = a_model.data.y_test_actual
    loc_y_pred = a_model.data.y_test_pred
    loc_fpr = a_model.data.fpr # false positive rate
    loc_tpr = a_model.data.tpr # true positive rate
    loc_ix = a_model.data.ix_roc # index fpr & tpr
    
    loc_logit_roc_auc = __metrics.roc_auc_score(loc_y_test,loc_y_pred)
    loc_plot = __plt.figure()
    __plt.plot(loc_fpr,loc_tpr,label='Area = %0.2f' % loc_logit_roc_auc)
    __plt.plot([0, 1], [0, 1],'r--')
    __plt.scatter(loc_fpr[loc_ix],loc_tpr[loc_ix],marker='o',color='black',label='Best')
    __plt.xlim([0.0, 1.0])
    __plt.ylim([0.0, 1.05])
    __plt.xlabel('False Positive Rate')
    __plt.ylabel('True Positive Rate')
    __plt.title('Receiver Operating Characteristic')
    __plt.legend(loc="lower right")
    __plt.close()
    
    return loc_plot

# calculate the g-mean for each threshold
def gmeans (a_model) :
    loc_fpr = a_model.data.fpr # false positive rate
    loc_tpr = a_model.data.tpr # true positive rate
    return __np.sqrt(loc_tpr * (1-loc_fpr))

def best_threshold (a_model) :
    return loc_thresholds[ix_roc]
    return a_model.data.thresholds[__np.argmax(a_model.data.fscores)]

