import numpy as np
from scipy.spatial import distance     
from scipy import stats
from data_models_new import Model


def get_js_pvalue(ref_model, data_model):
    js_data = distance.jensenshannon(
        ref_model.values,
        data_model.values,
        2.0,
    ) # calculation of p
    toys = ref_model.sample()
    js_toys = []
    for t in toys:
        js_toys.append(
            distance.jensenshannon(
                ref_model.values,
                t,
                2.0,                            #Base of the used log
            )
        )

    result = np.sum(np.array(js_toys) >= js_data) / len(js_toys)   #calculation of p~
    # return -1 * np.log(max(result, 1e-8))
    return result
