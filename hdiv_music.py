#!/usr/bin/env python3

import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep
import os
import numpy as np
from multiprocessing import Pool
from pprint import pprint

hep.style.use(hep.style.ROOT)
mpl.use("Agg")

from data_models import Model
from hdiv import single_test_hdiv, get_js_pvalue
from music import single_test_music, get_music_pvalue


def prepare_outputs():
    print("Starting ...")

    print("Preparing output directory ...")
    os.system("rm -rf outputs ; mkdir outputs")
    os.system("mkdir -p outputs/music")
    os.system("mkdir -p outputs/music/temp")
    os.system("mkdir -p outputs/music/toys")
    os.system("mkdir -p outputs/hdiv")


def run_js_experiments(ss, sf, number_of_toys):
    ref_model = Model(is_data=False, size=ss, sample_size=number_of_toys)
    data_model = ref_model.get_data_sample(signal_size=int(ss * sf))
    return get_js_pvalue(ref_model, data_model)


def run_music_experiments(ss, sf, number_of_toys):
    ref_model = Model(is_data=False, size=ss, sample_size=number_of_toys)
    data_model = ref_model.get_data_sample(signal_size=int(ss * sf))
    return get_music_pvalue(ref_model, data_model)


def main():
    prepare_outputs()
    total_data = 2_000
    signal_size = int(total_data * 0.02)
    # signal_size = 70

    ref_model = Model(is_data=False, size=total_data)
    data_model = ref_model.get_data_sample(signal_size=signal_size)

    # run a hdiv single test and produce plots
    # single_test_hdiv(total_data, signal_size, ref_model, data_model)

    # run a MUSiC single test and produce plots
    single_test_music(total_data, signal_size, ref_model, data_model)

    sample_sizes = [100, 300, 500, 700, 1000, 1500, 2000, 3000, 5000]
    signal_fractions = [0.015, 0.03, 0.05]
    # sample_sizes = [
    #     # int(1e2),
    #     500,
    # ]
    # signal_fractions = [0.03]
    rounds = 2000

    #############################################
    ## JS Experiments
    #############################################
    js_results = {}
    with Pool(120) as pool:
        for sf in signal_fractions:
            js_results[sf] = {}
            js_results[sf]["sample_size"] = []
            js_results[sf]["mean"] = []
            js_results[sf]["std"] = []
            print(
                "--------------------------------------------------------------------------------"
            )
            for ss in sample_sizes:
                js_results[sf]["sample_size"].append(ss)
                js_p_values = []
                print(f"\n--> JS - Signal fraction: {sf} - Sample size: {ss}")
                adaptative_rounds = rounds
                if ss <= 700:
                    adaptative_rounds = 4000
                js_p_values = list(
                    pool.starmap(
                        run_js_experiments, [(ss, sf, 2000)] * adaptative_rounds
                    )
                )
                js_results[sf]["mean"].append(np.mean(js_p_values))
                js_results[sf]["std"].append(np.std(js_p_values))
                print(js_results[sf]["mean"][-1])

    # pprint(js_results, indent=4)

    #############################################
    ## MUSiC Experiments
    #############################################
    rounds = 300
    music_results = {}
    with Pool(120) as pool:
        for sf in signal_fractions:
            music_results[sf] = {}
            music_results[sf]["sample_size"] = []
            music_results[sf]["mean"] = []
            music_results[sf]["std"] = []
            print(
                "--------------------------------------------------------------------------------"
            )
            for ss in sample_sizes:
                music_results[sf]["sample_size"].append(ss)
                music_p_values = []
                print(f"\n--> MUSiC - Signal fraction: {sf} - Sample size: {ss}")
                adaptative_rounds = rounds
                if ss <= 700:
                    adaptative_rounds = 500
                music_p_values = list(
                    pool.starmap(
                        run_music_experiments, [(ss, sf, 1000)] * adaptative_rounds
                    )
                )
                music_results[sf]["mean"].append(np.mean(music_p_values))
                music_results[sf]["std"].append(np.std(music_p_values))
                print(music_results[sf]["mean"][-1])

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
