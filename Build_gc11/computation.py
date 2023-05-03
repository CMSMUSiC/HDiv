#!/usr/bin/env python3

import argparse
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import mplhep as hep
# import os
import numpy as np
# from multiprocessing import Pool
# from pprint import pprint
# import tqdm 
# import time
# import resource as rs


# hep.style.use(hep.style.ROOT)
# mpl.use("Agg")

from data_models import Model
#from hdiv import single_test_hdiv, get_js_pvalue
from music import single_test_music, get_music_pvalue


# def run_js_experiments(ss, sf, number_of_toys):
#     ref_model = Model(is_data=False, size=ss, sample_size=number_of_toys)
#     data_model = ref_model.get_data_sample(signal_size=int(ss * sf),mu=signal_mean,sigma=signal_std)
#     return get_js_pvalue(ref_model, data_model)


#Defining Global Parameters
exp_mean = 10
signal_mean = 7
signal_std = 1    


def run_music_experiments_star(args):
                    return run_music_experiments(*args)

def run_music_experiments(ss, sf, number_of_toys):
    ref_model = Model(is_data=False, size=ss, sample_size=number_of_toys)
    data_model = ref_model.get_data_sample(signal_size=int(ss * sf),mu=signal_mean,sigma=signal_std)        #Wy this signal_size?
    return get_music_pvalue(ref_model, data_model)







#inputs =  [(ss, sf, NumberOfToys)] 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ss", type=int)
    parser.add_argument("sf", type=float)
    parser.add_argument("numberoftoys", type=int)
    args = parser.parse_args()



    T = run_music_experiments_star([args.ss, args.sf, args.numberoftoys]) 

    print("(" + str(np.round(T[0],16)) + "," + str(np.round(T[1],16)) + ")")


if __name__ == "__main__":
    main()
