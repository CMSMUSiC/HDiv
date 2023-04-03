import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep
from scipy.spatial import distance
from scipy import stats
from data_models import Model


def single_test_hdiv(total_data, signal_size, ref_model: Model, data_model: Model):
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
        label=f"Test model (Signal fraction: {float(signal_size)/float(total_data)*100:.2f}%)",
    )

    ax.legend()
    ax.set_yscale("log")
    fig.savefig(f"outputs/hdiv/input_data.png")

    # sample multiple ref_toys
    toys = ref_model.sample()
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
        if i < 10:
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
    fig.savefig(f"outputs/hdiv/toy_data.png")

    # js_data = distance.jensenshannon(
    #     ref_model.values / np.sum(ref_model.values),
    #     data_model.values / np.sum(data_model.values),
    #     2.0,
    # )
    js_data = distance.jensenshannon(
        ref_model.values,
        data_model.values,
        2.0,
    )
    toys = ref_model.sample()
    js_toys = []
    for t in toys:
        js_toys.append(
            # distance.jensenshannon(
            #     ref_model.values / np.sum(ref_model.values),
            #     t / np.sum(t),
            #     2.0,
            # )
            distance.jensenshannon(
                ref_model.values,
                t,
                2.0,
            )
        )

    fig = plt.figure()
    ax = plt.axes()
    vals, bins, _ = ax.hist(js_toys, bins=40, label="JS Trials")
    js_pvalue = np.sum(np.array(js_toys) >= js_data) / len(js_toys)
    ax.vlines(js_data, 0, np.max(vals), color="red", label=f"p-value: {js_pvalue}")
    ax.legend()
    fig.savefig(f"outputs/hdiv/js_dist.png")

    print(f"JS p-value: {js_pvalue}")


def get_js_pvalue(ref_model, data_model):
    js_data = distance.jensenshannon(
        ref_model.values,
        data_model.values,
        2.0,
    )
    toys = ref_model.sample()
    js_toys = []
    for t in toys:
        js_toys.append(
            distance.jensenshannon(
                ref_model.values,
                t,
                2.0,
            )
        )

    result = np.sum(np.array(js_toys) >= js_data) / len(js_toys)
    # return -1 * np.log(max(result, 1e-8))
    return result
