#!/usr/bin/env python3
# Use to make plots about the performance of the different codes
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep
import os
import numpy as np
from multiprocessing import Pool
from pprint import pprint
import tqdm 
import time
import resource as rs
from parallelbar import progress_imap


hep.style.use(hep.style.ROOT)
mpl.use("Agg")

from data_models import Model
from hdiv import single_test_hdiv, get_js_pvalue
from music import single_test_music, get_music_pvalue

def memory_limit(limit):
    soft, hard = rs.getrlimit(rs.RLIMIT_AS)
    rs.setrlimit(rs.RLIMIT_AS, (limit, hard))


def run_js_experiments_star(args):
                    return run_js_experiments(*args)
def run_music_experiments_star(args):
                    return run_music_experiments(*args)


def prepare_outputs():
    print("Starting ...")

    print("Preparing output directory ...")
    os.system("rm -rf outputs ; mkdir outputs")
    os.system("mkdir -p outputs/music")
    os.system("mkdir -p outputs/music/temp")
    os.system("mkdir -p outputs/music/toys")
    os.system("mkdir -p outputs/hdiv")

#Defining Global Parameters
exp_mean = 10
signal_mean = 53
signal_std = 10                                                         


def run_js_experiments(ss, sf, number_of_toys):
    ref_model = Model(is_data=False, size=ss, sample_size=number_of_toys)
    data_model = ref_model.get_data_sample(signal_size=int(ss * sf),mu=signal_mean,sigma=signal_std)
    return get_js_pvalue(ref_model, data_model)


def run_music_experiments(ss, sf, number_of_toys):
    ref_model = Model(is_data=False, size=ss, sample_size=number_of_toys)
    data_model = ref_model.get_data_sample(signal_size=int(ss * sf),mu=signal_mean,sigma=signal_std)        #Wy this signal_size?
    return get_music_pvalue(ref_model, data_model)


def main():
    prepare_outputs()
    total_data = 2_000

    

    sample_sizes = np.array([100,300,500,700,1000,3000])           #Which Sizes of Data should be calculated
    signal_fractions = [0.01]                                         #Which fraction of the signal should be added

    

    signal_size = int(0.02 * total_data)
    ref_model = Model(is_data=False, size=total_data)
    data_model = ref_model.get_data_sample(signal_size=signal_size,mu=signal_mean,sigma=signal_std)

    # run a MUSiC single test and produce plots
    single_test_music(total_data, signal_size, ref_model, data_model)



    #############################################
    ## JS Experiments
    #############################################
    rounds = 3000
    NumberOfToys = 3000
    js_results = {}
    with Pool(100) as pool:
        for sf in signal_fractions:
            js_results[sf] = {}
            js_results[sf]["sample_size"] = []
            js_results[sf]["mean"] = []
            js_results[sf]["std"] = []
            print(
                "--------------------------------------------------------------------------------"
            )
            i = 0

            # run a hdiv single test and produce plots
            signal_size = int(total_data * sf)       
            ref_model = Model(is_data=False, size=total_data)
            data_model = ref_model.get_data_sample(signal_size=signal_size,mu=signal_mean,sigma=signal_std)
            single_test_hdiv(total_data, signal_size, ref_model, data_model,exp_mean,signal_mean,signal_std)



            for ss in sample_sizes:
                i = i+1                 
                
                
                adaptative_rounds = rounds

                if sf <= 0.01:
                    adaptive_round =int( 1.5 * adaptative_rounds)
                    NumberOfToys = int(1.5 * NumberOfToys)
                    ss = ss * 2 

                if ss <= 500:
                    adaptative_rounds = 2 * adaptative_rounds
                    NumberOfToys = int(1.5 * NumberOfToys)
                elif ss <= 1000:
                    adaptative_rounds = int(1.5 *adaptative_rounds)
                elif ss >= 5000:
                    adaptative_rounds = int(0.7 * adaptative_rounds)
                    NumberOfToys = int(0.7 * NumberOfToys) 
                    
                
                js_results[sf]["sample_size"].append(ss)
                js_p_values = []    
                print(f"\n--> JS - Signal fraction: {sf} - Sample size: {ss}")    
                inputs = [(ss, sf, NumberOfToys)] * adaptative_rounds    
#                js_p_values = list(
#                    
#                    pool.starmap(
#                        run_js_experiments,inputs)   
#
#                    )
#                )
                js_p_values = list(tqdm.tqdm(pool.imap(run_js_experiments_star, inputs), total=len(inputs)))
                js_results[sf]["mean"].append(np.mean(js_p_values))
                js_results[sf]["std"].append(np.std(js_p_values))
                print(js_results[sf]["mean"][-1])
#                if(i>1):
#                    if((js_results[sf]["mean"][-1]<=0.01) and (js_results[sf]["mean"][-2]<=0.05)): break

    # pprint(js_results, indent=4)

    #############################################
    ## MUSiC Experiments
    #############################################
    rounds = 300                #Anzahl an p-Werten die in jedem Schritt berechnet werden um anschließend gemittelt zu werden.
    NumberOfToys = 5000         # Die Anzahl an Toys um p~ zu berechen.
    music_results = {}
    with Pool(100) as pool:     #Multicore berechnung mit 120 cores
        for sf in signal_fractions:
            music_results[sf] = {}
            music_results[sf]["sample_size"] = []
            music_results[sf]["mean"] = []
            music_results[sf]["std"] = []
            print(
                "--------------------------------------------------------------------------------"
            )
            i = 0
            for ss in sample_sizes: #Neugeneration der Daten? Ist das Gut?
                i = i+1
                
                
                adaptative_rounds = rounds

                if sf <= 0.01:
                    adaptive_round =int( 1.5 * adaptative_rounds)
                    NumberOfToys = int(1.5 * NumberOfToys)
                    ss = ss * 2 

                if ss <= 500:
                    adaptative_rounds = 2 * adaptative_rounds
                    NumberOfToys = int(1.5 * NumberOfToys)
                elif ss <= 1000:
                    adaptative_rounds = int(1.5 *adaptative_rounds)
                elif ss >= 5000:
                    adaptative_rounds = int(0.7 * adaptative_rounds)
                    NumberOfToys = int(0.7 * NumberOfToys) 

                music_results[sf]["sample_size"].append(ss)
                music_p_values = []    
                print(f"\n--> MUSiC - Signal fraction: {sf} - Sample size: {ss}")    
                inputs =   [(ss, sf, NumberOfToys)] * adaptative_rounds
#                music_p_values = list(
#                    pool.starmap(
#                        run_music_experiments, [(ss, sf, NumberOfToys)] * adaptative_rounds #Number is the number of toys
#                    )                                                                       # Führt die Funktion run_... mit  den nachfolgenden parametern aus.
#                )
                music_p_values = list(tqdm.tqdm(pool.imap(run_music_experiments_star, inputs), total=len(inputs)))
                music_results[sf]["mean"].append(np.mean(music_p_values))
                music_results[sf]["std"].append(np.std(music_p_values))
                print(music_results[sf]["mean"][-1])
#                if(i > 1):
#                    if( (music_results[sf]["mean"][-1]<=0.01) and (music_results[sf]["mean"][-2]<=0.05) ): break


    # pprint(music_results, indent=4)

    # plot results
    for sf in signal_fractions:
        fig = plt.figure()
        ax = plt.axes()
        plt.errorbar(
            js_results[sf]["sample_size"],
            js_results[sf]["mean"],
            yerr=js_results[sf]["std"],
            fmt="o:",
            label=f"JS - Signal Fraction: {float(sf*100):.1f}%",
        )

        plt.errorbar(
            music_results[sf]["sample_size"],
            music_results[sf]["mean"],
            yerr=music_results[sf]["std"],
            fmt="s-",
            label=f"MUSiC - Signal Fraction: {float(sf*100):.1f}%",
        )
        ax.legend()
        ax.set_xlabel("Sample size")
        ax.set_ylabel("Mean p-value")
        fig.tight_layout()
        # ax.set_yscale("log")
        fig.savefig(f"outputs/experiments_{str(sf).replace('.', 'p')}.png")


if __name__ == "__main__":
    main()
