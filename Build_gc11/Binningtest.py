#!/usr/bin/env python3

import argparse

import numpy as np


from data_models import Model
from music import single_test_music, get_music_pvalue



#Defining Global Parameters
exp_mean = 10
signal_mean = 35
signal_std = 10    


def run_music_experiments_star(args):
                    return run_music_experiments(*args)

def run_music_experiments(ss, sf, number_of_toys,bins):
    ref_model = Model(is_data=False, size=ss, sample_size=number_of_toys,bins=bins)
    data_model = ref_model.get_data_sample(signal_size=int(ss * sf),mu=signal_mean,sigma=signal_std)        #Wy this signal_size?
    return get_music_pvalue(ref_model, data_model)







#inputs =  [(ss, sf, NumberOfToys)] 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ss", type=int)
    parser.add_argument("sf", type=float)
    parser.add_argument("numberoftoys", type=int)
    parser.add_argument("bins", type=int)
    args = parser.parse_args()



    T = run_music_experiments_star([args.ss, args.sf, args.numberoftoys,args.bins]) 

    print("(" + str(np.round(T[0],16)) + "," + str(np.round(T[1],16)) + ")")


if __name__ == "__main__":
    main()
