#!/usr/bin/env python3

import matplotlib.pyplot as plt
import mplhep as hep
import matplotlib as mpl
import os
import csv
import numpy as np
import ROOT

hep.style.use(hep.style.ROOT)
# mpl.use("Agg")

from event_classes import event_classes


def read_outputs(file_path):
    scores = []
    with open(file_path, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            scores.append(float(row["score"]))
    return scores


def read_outputs_js(file_path):
    scores = []
    with open(file_path, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            scores.append(float(row["js_distance"]))
    return scores


# norm = plt.Normalize(np.min(np.array(sf)), np.max(np.array(sf)))
sig_fractions = []
P_music = {}
JS = {}
distributions = ["InvMass", "SumPt"]

# cmap = 'brg'
# cmap = 'cubehelix'


p_js = []
p = []
idx = 0
for ec_name in event_classes.keys():
    for dist in distributions:
        path_signal = f"Build_Stage2/JS_integration/{dist}/{ec_name}_signal/{ec_name}_{dist}_output.csv"
        path_bkg = f"Build_Stage2/JS_integration/{dist}/{ec_name}_bkg/{ec_name}_{dist}_output.csv"

        if os.path.isfile(path_signal) and os.path.isfile(path_bkg):
            # print(f"--> [{idx}] {ec_name}: {dist}")
            idx += 1

            p_signal = np.median(np.array(read_outputs(path_signal)))
            p_signal_js = np.median(np.array(read_outputs_js(path_signal)))
            p_toys = np.array(read_outputs(path_bkg))
            p_toys_js = np.array(read_outputs_js(path_bkg))

            # music p-tilde
            result = max(
                1.0 / float(len(p_toys)),
                np.sum(p_toys <= p_signal) / float(len(p_toys)),
            )
            p.append(result)

            # alt p-value
            result_js = max(
                1.0 / float(len(p_toys_js)),
                np.sum(np.array(p_toys_js) >= p_signal_js) / float(len(p_toys_js)),
            )
            p_js.append(result_js)

            # add signal fraction
            sig_fractions.append(event_classes[ec_name])


# plt.xscale("log")
# plt.yscale("log")

# plt.ylim(0,0.7)
fig = plt.figure(figsize=(12, 12))

gs = fig.add_gridspec(
    3,
    2,
    width_ratios=(4, 1),
    height_ratios=(1, 4, 0.3),
    left=0.1,
    right=0.9,
    bottom=0.1,
    top=0.9,
    wspace=0.05,
    hspace=0.3,
)

ax = fig.add_subplot(gs[1, 0])
ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)


# no labels
ax_histx.tick_params(axis="x", labelbottom=False)
ax_histy.tick_params(axis="y", labelleft=False)

# the scatter plot:
# cmap = mpl.cm.cool
# cmap='Blues'
# sct_plot = ax.scatter(p,p_js,alpha = 0.4, s=100, c=sig_fractions, cmap=cmap, edgecolor = None)
sct_plot = ax.scatter(p, p_js, alpha=0.3, s=100, c=sig_fractions, edgecolor=None)
# sct_plot = ax.scatter(p, p_js, alpha=0.3, s=100, c="blue", edgecolor=None)

ax_histx.hist(p, bins=30, color="tab:cyan")
ax_histy.hist(p_js, bins=30, orientation="horizontal", color="tab:cyan")
ax_histx.set_yscale("log")
ax_histy.set_xscale("log")

norm = mpl.colors.Normalize(vmin=5, vmax=10)
color_ax = fig.add_subplot(gs[2, 0])
fig.colorbar(sct_plot, cax=color_ax, orientation="horizontal", label="Signal Fraction")

ax.set_xlabel("MUSiC $\widetilde{p}$")
ax.set_ylabel("Fast $p$-value")


ax.grid()
ax.plot([0.001, 1], [0.001, 1], color="black")
os.system("rm -rf Music_alt_comparison*")

plt.savefig("Music_alt_comparison.png")
plt.savefig("Music_alt_comparison.pdf")

ax.set_yscale("log")
ax.set_xscale("log")

plt.savefig("Music_alt_comparison_log_scale.jpg")
plt.savefig("Music_alt_comparison_log_scale.pdf")
