# https://keras.io/guides/sequential_model/
# https://keras.io/api/layers/core_layers/dense/
# https://www.tutorialspoint.com/keras/keras_dense_layer.htm

from keras.models import Sequential as __seq
from keras.layers import Dense as __dense
import pandas as __pd

import picklebase as __pp

class __fit_result :
    model = None
    accuracy = None

class __result_predict :
    prediction = None
    worksheet = None

def fit (a_data,a_feature,a_target,b_node=12,b_activation='relu') : 
    loc_result = __fit_result()
    # a_data in array
    # a_feature : columns [] of features
    # a_target : column '' of target
    # b_node = nodes / neurons
    # split into input (X) and output (y) variables
    X = __pp.data.df_to_array(a_data=a_data[a_feature])
    y = __pp.data.df_to_array(a_data=a_data[a_target])
    # define the keras model
    loc_model = __seq()
    loc_model.add(__dense(b_node,input_dim=len(a_feature),activation=b_activation,name='layer1')) # first hidden layer
    # compile the keras model
    loc_model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    # fit the keras model on the dataset
    loc_model.fit(X,y,epochs=150,batch_size=10,verbose=0) # verbose is to hide progress bar
    # evaluate the keras model
    _,loc_accuracy = loc_model.evaluate(X, y, verbose=0)
    loc_result.model = loc_model
    loc_result.accuracy = loc_accuracy
    return loc_result

def predict (a_model,a_data,a_feature) :
    
    # make probability predictions with the model
    # predictions = a_model.predict(X)
    # round predictions 
    # rounded = [round(x[0]) for x in predictions]
    
    # OR
    # make class predictions with the model
    X = __pp.data.df_to_array(a_data=a_data[a_feature])
    loc_predictions = a_model.predict_classes(X)
    loc_prediction = __pp.data.array_to_df(a_array=loc_predictions,b_as_column=['__pred'])

    loc_merge = a_data
    loc_merge = __pd.merge(loc_merge,loc_prediction,left_index=True,right_index=True)

    loc_result_predict = __result_predict()
    loc_result_predict.prediction = loc_prediction
    loc_result_predict.worksheet = loc_merge
    
    return loc_result_predict

