from data_models_2D import Model_2D
import numpy as np
from hdiv_2D import get_js_pvalue_2D
from multiprocessing import Pool
from tqdm import tqdm
import time
import resource as rs
from parallelbar import progress_imap
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
from scipy.special import erf
from uncertainties import ufloat
# hep.style.use(hep.style.ROOT)
# mpl.use("Agg")

# ss = 300
# number_of_toys = 3000
# signal_mean = (30, 30)
# signal_std = [[5, 0], [0, 5]]
# sf = 0.03
# rounds = 1


# # print(ref_model.nbins)
# # print(ref_model.values)
# # print(data_model)

# js_2D = []
# js_x = []
# js_y = []

# for i in tqdm(range(rounds)):
#     ref_model = Model_2D(is_data=False, size=ss, sample_size=number_of_toys)
#     data_model = ref_model.get_data_sample(
#         signal_size=int(ss * sf), mu=signal_mean, sigma=signal_std)
#     js = get_js_pvalue_2D(ref_model, data_model)
#     js_2D.append(js[0])
#     js_x.append(js[1])
#     js_y.append(js[2])


# print("2D :", np.mean(js_2D))
# print("X :", np.mean(js_x))
# print("Y :", np.mean(js_y))

# Bugfixing


# Defining Global Parameters
exp_mean = 10
signal_mean = (350, 530)
signal_std = [[5, 5], [5, 5]]


def run_js_experiments_star(args):
    return run_js_experiments(*args)


def prepare_outputs():
    print("Starting ...")

    print("Preparing output directory ...")
    os.system("rm -rf outputs ; mkdir outputs")
    os.system("mkdir -p outputs/music")
    os.system("mkdir -p outputs/music/temp")
    os.system("mkdir -p outputs/music/toys")
    os.system("mkdir -p outputs/hdiv")


def run_js_experiments(ss, sf, number_of_toys):
    ref_model = Model_2D(is_data=False, size=ss, sample_size=number_of_toys)
    data_model = ref_model.get_data_sample(
        signal_size=int(ss * sf), mu=signal_mean, sigma=signal_std)
    return get_js_pvalue_2D(ref_model, data_model)


def main():
    total_data = 2_000
    # Directory
    directory = "exp-" + str(exp_mean) + ", sig_mean-" + str(signal_mean) + ", sig_std- " + str(signal_std)
  
    # Parent Directory pathw
    parent_dir = "./Results/2D_JS"
  
    # Path
    path = os.path.join(parent_dir, directory)
    
    os.mkdir(path)

    # Which Sizes of Data should be calculated
    sample_sizes = np.array([100, 300, 500, 700, 1000, 2000])
    signal_fractions = [0.03]  # Which fraction of the signal should be added

    #############################################
    # MUSiC Experiments
    #############################################
    rounds = 1
    NumberOfToys = 1
    js_results_2D = {}
    js_results_x = {}
    js_results_y = {}
    with Pool(105) as pool:  # Multicore berechnung mit 120 cores
        for sf in signal_fractions:
            js_results_2D[sf] = {}
            js_results_2D[sf]["sample_size"] = []
            js_results_2D[sf]["mean"] = []
            js_results_2D[sf]["std"] = []

            js_results_x[sf] = {}
            js_results_x[sf]["sample_size"] = []
            js_results_x[sf]["mean"] = []
            js_results_x[sf]["std"] = []

            js_results_y[sf] = {}
            js_results_y[sf]["sample_size"] = []
            js_results_y[sf]["mean"] = []
            js_results_y[sf]["std"] = []

            print("-------------------------------------------------------------------------")
            i = 0
            for ss in sample_sizes:
                i = i+1

                adaptative_rounds = rounds

                js_results_2D[sf]["sample_size"].append(ss)
                js_results_x[sf]["sample_size"].append(ss)
                js_results_y[sf]["sample_size"].append(ss)

                print(
                    f"\n--> MUSiC / JS - Signal fraction: {sf} - Sample size: {ss}")
                inputs = [(ss, sf, NumberOfToys)] * adaptative_rounds

                start = time.monotonic()
                # Optimierung über simple run und paralelisierung!
                run_js_experiments_star([ss, sf, NumberOfToys])
                timeout =  (time.monotonic() - start)
                print("Time per Job: " + str(np.round(timeout/60, 0)) +
                      " minutes and " + str(np.round(timeout % 60, 0)) + " seconds")
                results = progress_imap(run_js_experiments_star, inputs,
                                        process_timeout=8 *timeout,
                                        initargs=(100,),
                                        n_cpu=80,
                                        error_behavior='coerce',
                                        set_error_value=("nan", "nan", "nan"),
                                        )
                results = np.array(results, dtype=object)
                js_p_values_2D = [
                    value for value in results[:, 0] if value != "nan"]
                js_p_values_x = [
                    value for value in results[:, 1] if value != "nan"]
                js_p_values_y = [
                    value for value in results[:, 2] if value != "nan"]

                print("JS_2D:\t" + str(np.round(np.mean(js_p_values_2D), 4)))
                print("JS_X:\t" + str(np.round(np.mean(js_p_values_x), 4)))
                print("JS_Y:\t" + str(np.round(np.mean(js_p_values_y), 4)))


                js_results_2D[sf]["mean"].append(np.mean(js_p_values_2D))
                js_results_2D[sf]["std"].append(np.std(js_p_values_2D))
                js_results_x[sf]["mean"].append(np.mean(js_p_values_x))
                js_results_x[sf]["std"].append(np.std(js_p_values_x))
                js_results_y[sf]["mean"].append(np.mean(js_p_values_y))
                js_results_y[sf]["std"].append(np.std(js_p_values_y))

    

    for sf in signal_fractions:
        fig, ax = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [5, 2]})

        ax[0].errorbar(
            sample_sizes,
            js_results_2D[sf]["mean"],
            yerr=js_results_2D[sf]["std"],
            fmt="o:",
            capsize = 5,
            label=f"JS_2D P-Value",
            )

        ax[0].errorbar(
            sample_sizes,
            js_results_x[sf]["mean"],
            yerr=js_results_x[sf]["std"],
            fmt="o:",
            capsize = 5,
            label=f"JS_X P-Value",
            )
        
        ax[0].errorbar(
            sample_sizes,
            js_results_y[sf]["mean"],
            yerr=js_results_y[sf]["std"],
            fmt="o:",
            capsize = 5,
            label=f"JS_Y P-Value",
            )
        
        difference = []
        difference_std = []
        for i in range(len(sample_sizes)):
            js_1d = 0.5*(ufloat(js_results_y[sf]["mean"][i],js_results_y[sf]["std"][i]) + ufloat(js_results_x[sf]["mean"][i],js_results_x[sf]["std"][i]) )
            js_2d = ufloat(js_results_2D[sf]["mean"][i],js_results_2D[sf]["std"][i])
            difference.append( ((js_1d - js_2d) / js_1d ).n)
            difference_std.append( ((js_1d - js_2d) / js_1d ).s)
        ax[1].errorbar(
            sample_sizes,
            difference,
            yerr=difference_std,
            fmt='.', 
            marker='o',
            capsize = 4,
            markersize = 4,
            color = "red"
        )
        ax[0].grid()
        ax[1].grid()

        ax[0].set_title(r"$\mu$ = " + str(signal_mean) + r", $\sigma$ = " + str(signal_std) + ", Signal Fraction = " + str(sf))
        
        ax[1].set_xlabel("Sample size")
        ax[0].set_ylabel("Mean p-value")
        ax[1].set_ylabel("$(P_{js_1D} - P_{js_2D})/ P_{js_1D}$")
        fig.tight_layout()
        ax[1].set_xscale("log")
        ax[0].set_yscale("log")
        #ax[1].set_yscale("symlog")

        ax[1].axhline(y=0., color='black', linestyle='--')
        ymax = max([abs(x) for x in ax[1].get_ylim()])
        ax[1].set_ylim(-ymax, ymax)
        p = 0.5 * (1-erf([1,2,3]/np.sqrt(2)))
        xmin = min([abs(x) for x in ax[0].get_xlim()])
        xmax = max([abs(x) for x in ax[1].get_xlim()])
        ax[0].set_xlim(xmin,xmax)
        ax[0].hlines(p[0],xmin,xmax, ls = "--", color="lightgreen",label=fr"1 $\sigma$")
        ax[0].hlines(p[1],xmin,xmax, ls = "--", color="green",label=fr"2 $\sigma$")
        ax[0].hlines(p[2],xmin,xmax, ls = "--", color="darkgreen",label=fr"3 $\sigma$")
        ax[0].set_yscale("log")
        ax[0].legend()
        plt.savefig(path +"/Result-sf_" + str(int(sf *100 ))+"%.png",dpi=1000)


if __name__ == "__main__":
    main()
