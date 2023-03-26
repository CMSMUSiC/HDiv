#!/usr/bin/env python3

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import hist
import mplhep as hep
import os
from tqdm import tqdm
from scipy.spatial import distance

hep.style.use(hep.style.ROOT)
mpl.use("Agg")

from data_models import Model


def prepare_outputs():
    os.system("rm -rf outputs ; mkdir outputs")


def main():
    prepare_outputs()
    total_data = 10_000
    sig_frac = 0.0
    ref_model = Model(is_data=False, size=total_data, signal_fraction=0.0)
    data_model = Model(
        is_data=True, size=int(total_data / (1 - sig_frac)), signal_fraction=sig_frac
    )

    # plot input data
    fig = plt.figure()
    ax = plt.axes()
    # reference model
    hep.histplot(
        ref_model.values,
        bins=ref_model.bins,
        yerr=ref_model.total_uncert,
        ax=ax,
        label="Ref Model (Uncert.)",
    )
    # data
    hep.histplot(
        data_model.values,
        bins=data_model.bins,
        yerr=data_model.stats_uncert,
        histtype="errorbar",
        ax=ax,
        color="black",
        label=f"Test model (Signal fraction: {sig_frac*100:.2f}%)",
    )

    ax.legend()
    ax.set_yscale("log")
    fig.savefig(f"outputs/input_data.png")

    # sample multiple ref_toys
    toys = ref_model.sample(10)
    fig = plt.figure()
    ax = plt.axes()
    # reference model
    hep.histplot(
        ref_model.values,
        bins=ref_model.bins,
        yerr=ref_model.total_uncert,
        ax=ax,
        label="Ref Model (Uncert.)",
    )
    for i, t in enumerate(toys):
        # toy data
        hep.histplot(
            t,
            bins=data_model.bins,
            histtype="errorbar",
            ax=ax,
            # label=f"Toy data - {i}",
        )

    ax.legend()
    ax.set_yscale("log")
    fig.savefig(f"outputs/toy_data.png")

    js_data = distance.jensenshannon(
        ref_model.values / np.sum(ref_model.values),
        data_model.values / np.sum(data_model.values),
        2.0,
    )
    toys = ref_model.sample(10_000)
    js_toys = []
    for t in tqdm(toys):
        js_toys.append(
            distance.jensenshannon(
                ref_model.values / np.sum(ref_model.values),
                t / np.sum(t),
                2.0,
            )
        )

    fig = plt.figure()
    ax = plt.axes()
    vals, bins, _ = ax.hist(js_toys, bins=40, label="JS Trials")
    js_pvalue = np.sum(np.array(js_toys) >= js_data) / len(js_toys)
    ax.vlines(js_data, 0, np.max(vals), color="red", label=f"p-value: {js_pvalue}")
    ax.legend()
    fig.savefig(f"outputs/js_dist.png")


if __name__ == "__main__":
    main()
