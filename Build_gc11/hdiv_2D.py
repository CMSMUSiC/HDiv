import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.spatial import distance     
from scipy import stats
from data_models_2D import Model_2D

def get_js_pvalue_2D(ref_model, data_model):

    #Calculation of the js distance of the data modell
    js_data = 0
    
    js_data = js_data + distance.jensenshannon(
        ref_model.values.flatten(),
        data_model.flatten(),
        2.0,
    ) 

    toys = ref_model.sample()
    js_toys = []

    #calculating the js values for the toys
    for t in toys:
        js_toys.append(
            distance.jensenshannon(
                ref_model.values.flatten(),
                t.flatten(),
                2.0,                               
                )
            )
    
    #Calculation of the p Value for the 2D 
    result_2D = max(np.sum(np.array(js_toys) >= js_data) / len(js_toys),1/len(js_toys))   #calculation of p~


    #Summing over all Cullums / Rows to get 1D data
    ref_model_xvalues = []
    data_model_xvalues = []
    for i in range(ref_model.nbins):
        R = 0
        D = 0
        for j in range(ref_model.nbins):
            R = R + ref_model.values[i][j]
            D = D + data_model[i][j]
        ref_model_xvalues.append(R) 
        data_model_xvalues.append(D)

    #Calculating the JS distance
    js_data_x =distance.jensenshannon(
            ref_model_xvalues,
            data_model_xvalues,
            2.0,
        )

    #Sampling the toys with the 1D data
    js_toys_x = []
    toys_x = ref_model.sample_1D(values_1d = np.array(ref_model_xvalues))

    for t in toys_x:
        js_toys_x.append(distance.jensenshannon(
            ref_model_xvalues,
            t,
            2.0,
        ))

    result_x = max(np.sum(np.array(js_toys_x) >= js_data_x) / len(js_toys_x),1/len(js_toys_x))    


    ref_model_yvalues = []  
    data_model_yvalues = []   
    for i in range(ref_model.nbins):
        R = 0
        D = 0
        for j in range(ref_model.nbins):
            R = R + ref_model.values[j][i]
            D = D + data_model[j][i]
        ref_model_yvalues.append(R) 
        data_model_yvalues.append(D)

    js_data_y =distance.jensenshannon(
            ref_model_yvalues,
            data_model_yvalues,
            2.0,
        )
    
    js_toys_y = []
    toys_y = ref_model.sample_1D(values_1d = np.array(ref_model_yvalues))

    for t in toys_y:
        js_toys_y.append(distance.jensenshannon(
            ref_model_yvalues,
            t,
            2.0,
        ))
    

    result_y = max(np.sum(np.array(js_toys_y) >= js_data_y) / len(js_toys_y),1/len(js_toys_y))   



    return result_2D,result_x,result_y
  
