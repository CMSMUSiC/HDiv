#!/usr/bin/env python3
import roothelpers

from ectools.register import ecroot
from ectools.misc import rremove
import ROOT
import collections
import json
import numpy as np
import os
import logging
import time
import resource as rs
from parallelbar import progress_imap, progress_map
import sys
from multiprocessing import Pool
import tqdm
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep
import subprocess

import time
import random

from event_classes import event_classes
from get_event_classes import get_event_classes

hep.style.use(hep.style.ROOT)
mpl.use("Agg")


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


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


logger = logging.getLogger("scan-submitter")

# Not allowing JSON nans because rapidjson (C++) cannot handle them.
JSON_DEFAULTS = dict(allow_nan=False, indent=2)

# Create a container class for the MCBin.
MCBin = collections.namedtuple(
    "MCBin",
    (
        "mcEventsPerProcessGroup",
        "mcStatUncertPerProcessGroup",
        "lowerEdge",
        "width",
        "mcSysUncerts",
        "unweightedEvents",
    ),
)


def collect_systematics(ec_names, mc_file, signal_file=None):
    systematic_names = set()
    for ec_name in ec_names:
        for file in (mc_file, signal_file):
            if not file:
                continue
            key = file.GetKey(ec_name)
            event_class = key.ReadObj()
            ec_systematic_names = event_class.getSystematicNames()

            for ec_systematic_name in ec_systematic_names:
                ec_systematic_name = rremove(ec_systematic_name, "Up")
                ec_systematic_name = rremove(ec_systematic_name, "Down")
                systematic_names.add(ec_systematic_name)

            event_class.Delete()

    return systematic_names


def create_systematic_shifts(systematic_names, count=1):
    shifts = np.random.normal(loc=0.0, scale=1.0, size=(len(systematic_names), count))
    dictionary = dict(zip(systematic_names, shifts))
    return dictionary


def _flatten(item):
    """Returns a serializable type from the given item."""

    # Namedtuples have the member _asdict.
    if hasattr(item, "_asdict"):
        return _flatten(dict(item._asdict()))

    # Numpy types
    elif isinstance(item, np.ndarray):
        return _flatten(item.tolist())

    # Primitive types
    elif isinstance(item, (int, float, str)):
        return item

    # Different kind of primitive containers.
    elif isinstance(item, dict):
        return {k: _flatten(v) for k, v in item.items()}
    elif isinstance(item, list):
        return list(_flatten(x) for x in item)
    elif isinstance(item, tuple):
        return tuple(_flatten(x) for x in item)

    # Fallback solution.
    # When the warning is closen, somebody should implement a handler here!
    else:
        logging.getLogger().warning("Item '%r' might not be JSON-serializable.", item)
        return item


def _extract_mc_bins(event_class, distribution, filter_systematics=None, scan_key=""):
    if filter_systematics is None:
        filter_systematics = []
    mc_hists = ecroot.event_yield_by_process_group(
        event_class, distribution, aggregation_level="none"
    )
    uncertainty_hists = ecroot.combined_uncertainty_by_systematic_name(
        event_class,
        distribution,
        symmetrize=False,
        filter_systematics=filter_systematics,
    )
    unweighted_hists = _extract_histograms(event_class, distribution)
    retval = _hists2bins(mc_hists, uncertainty_hists, unweighted_hists, scan_key)
    # for hist in mc_hists.values():
    #     hist.Delete()
    # for hist in uncertainty_hists.values():
    #     hist.Delete()
    # for hists in unweighted_hists.values():
    #     hists["hist"].Delete()
    return retval


def _extract_histograms(event_class, distribution):
    """Read histogram and corresponding error histograms."""

    # Initalize dict for unweighted number of events.
    # Is filled with dicts { 'hist': unweighted histogram, 'xs': crossection }
    # for each process_group.
    unweighted_hists = {}

    # Add up hists and errors for all processes
    for process_name in list(event_class.getProcessList()):
        unweighted_hists[process_name] = {
            "hist": event_class.getHistoPointerUnweighted(
                process_name, distribution
            ).Clone(),
            "xs": event_class.getCrossSection(process_name),
        }

    return unweighted_hists


def _hists2bins(mc_hists, uncertainty_hists, unweighted_hists, scan_key=""):
    assert len(mc_hists) > 0

    bins = []
    Nbins = list(mc_hists.values())[0].GetNbinsX()

    for ibin in range(1, Nbins + 1):
        # Obtain lowerEdge and width from 'some' contribution (doesn't matter which)
        lowerEdge = list(mc_hists.values())[0].GetBinLowEdge(ibin)
        width = list(mc_hists.values())[0].GetBinWidth(ibin)

        mcEventsPerProcessGroup = collections.OrderedDict()
        mcStatUncertPerProcessGroup = collections.OrderedDict()
        for process_name, process_hist in mc_hists.items():
            assert process_hist.GetBinLowEdge(ibin) == lowerEdge
            assert process_hist.GetBinWidth(ibin) == width
            mcEventsPerProcessGroup[process_name] = process_hist.GetBinContent(ibin)
            mcStatUncertPerProcessGroup[process_name] = process_hist.GetBinError(ibin)
        if "ReduceAllSyst" in scan_key:
            logger.info("Reducing all systs to 50%")
        mcSysUncerts = collections.OrderedDict()
        # Add uncertainties.
        for systematic_name, systematic_hist in uncertainty_hists.items():
            assert systematic_hist.GetBinLowEdge(ibin) == lowerEdge
            assert systematic_hist.GetBinWidth(ibin) == width
            if "Jet_systScale" in systematic_name and (
                "reduceJetScale" in scan_key or "reduceJetUncerts" in scan_key
            ):
                logger.info("Reducing jet scale by 0.5")
                mcSysUncerts[systematic_name] = (
                    systematic_hist.GetBinContent(ibin) * 0.5
                )
            elif "Jet_systResolution" in systematic_name and (
                "reduceJetRes" in scan_key or "reduceJetUncerts" in scan_key
            ):
                logger.info("Reducing jet res by 0.5")
                mcSysUncerts[systematic_name] = (
                    systematic_hist.GetBinContent(ibin) * 0.5
                )
            elif "reduceAllSyst" in scan_key:
                mcSysUncerts[systematic_name] = (
                    systematic_hist.GetBinContent(ibin) * 0.5
                )
            elif "reduceLOXS" in scan_key and systematic_name.endswith("LO"):
                mcSysUncerts[systematic_name] = (
                    systematic_hist.GetBinContent(ibin) * 0.5
                )
            elif (
                "reduceMETuncert" in scan_key
                and "slimmedMETs_systScale" in systematic_name
            ):
                mcSysUncerts[systematic_name] = (
                    systematic_hist.GetBinContent(ibin) * 0.5
                )
            elif "reduceQCDWeight" in scan_key and systematic_name.startswith(
                "qcdWeight"
            ):
                mcSysUncerts[systematic_name] = (
                    systematic_hist.GetBinContent(ibin) * 0.5
                )
            elif "reducePDFuncert" in scan_key and systematic_name.endswith(
                "pdfuponly"
            ):
                mcSysUncerts[systematic_name] = (
                    systematic_hist.GetBinContent(ibin) * 0.5
                )
            elif "reduceFakeUncert" in scan_key and "fake" in systematic_name:
                mcSysUncerts[systematic_name] = (
                    systematic_hist.GetBinContent(ibin) * 0.5
                )
            elif "reduceAllScaleUncerts" in scan_key and "systScale" in systematic_name:
                mcSysUncerts[systematic_name] = (
                    systematic_hist.GetBinContent(ibin) * 0.5
                )
            else:
                mcSysUncerts[systematic_name] = systematic_hist.GetBinContent(ibin)

        unweightedEvents = collections.OrderedDict()
        # Add unweighted event numbers and cross sections.
        for process_name, unweighted_hist in unweighted_hists.items():
            assert unweighted_hist["hist"].GetBinLowEdge(ibin) == lowerEdge
            assert unweighted_hist["hist"].GetBinWidth(ibin) == width
            unweightedEvents[process_name] = {
                "Nevents": unweighted_hist["hist"].GetBinContent(ibin),
                "xs": unweighted_hist["xs"],
            }

        bins.append(
            MCBin(
                mcEventsPerProcessGroup=mcEventsPerProcessGroup,
                mcStatUncertPerProcessGroup=mcStatUncertPerProcessGroup,
                lowerEdge=lowerEdge,
                width=width,
                mcSysUncerts=mcSysUncerts,
                unweightedEvents=unweightedEvents,
            )
        )

    return bins


def calculation(
    ec_name, n_rounds, mc_root_file_name, signal_file_name, IS_SIGNAL=False
):

    # Sleep for a while in order to not overlaod ROOT global states and memory access
    # (I have no clue at all if it makes any sense ...)
    # print(f"Sleeping [{ec_name}] ...")
    # time.sleep(random.uniform(0, 10))

    mc_root_file = ROOT.TFile.Open(mc_root_file_name)

    key = mc_root_file.GetKey(ec_name)
    event_class = key.ReadObj()
    Kin_distribution = event_class.getDistTypes()

    #########################################
    #########################################
    #########################################
    # Kin_distribution = ["InvMass", "SumPt"]
    Kin_distribution = ["SumPt"]
    # Kin_distribution = ["InvMass"]
    #########################################
    #########################################
    #########################################

    for distribution in Kin_distribution:
        distribution = str(distribution)
        # create shifts.json
        shifts_json = (
            "Build_Stage2/JS_scannfiles/"
            + distribution
            + "/shifts-"
            + ec_name
            + ".json"
        )  # Change  Later/ One shift file

        if IS_SIGNAL:
            signal_file = ROOT.TFile.Open(signal_file_name)
            systematics = collect_systematics([ec_name], mc_root_file, signal_file)

        if not IS_SIGNAL:
            systematics = collect_systematics([ec_name], mc_root_file, signal_file=None)

        shifts = create_systematic_shifts(systematics, n_rounds)
        os.system("rm -rf " + shifts_json + ">> /dev/null")
        with open(shifts_json, "w") as file:
            json.dump(_flatten(shifts), file, **JSON_DEFAULTS)

        minRegionWidth = 3
        if distribution == "InvMass":
            minRegionWidth = 1
        # Make Scan JSON
        d = {
            "gridpack_name": "Dummy_gridpack_name",
            "minRegionWidth": minRegionWidth,  # Just used for invariant Mass / change later
            "coverageThreshold": 0.0,  # Same for all
            "regionYieldThreshold": 1e-06,  # Same for all
            "sigmaThreshold": 0.6,  # Same for all
            "integralScan": False,  # Same for all
            "skipLookupTable": False,  # Same for all
            "noLowStatsTreatment": False,  # Same for all
            "widthLowStatsRegions": 4,  # Same for all
            "thresholdLowStatsDominant": 0.9,  # Same for all
            "mcStatUncertScaleFactor": 1.0,  # Same for all
            "dicedMCUncertScaleFactor": 1.0,  # Same for all
            "dicedSignalUncertScaleFactor": 1.0,  # Same for all
            "hash": "Dummy_hash",  # Create Hash later
            "name": ec_name,
            "distribution": distribution,
        }

        mc_ec = ecroot.read_ec_object(mc_root_file, ec_name)
        #      print(f"systematics: {mc_ec.getSystematicNames()}")

        d["MCBins"] = _flatten(
            _extract_mc_bins(
                mc_ec,
                distribution=d["distribution"],
                filter_systematics=None,
                scan_key="",
            )
        )

        # Comment out if not Data
        data_dir = (
            "Build_Stage2/JS_integration/" + distribution + "/" + ec_name + "_bkg"
        )
        if IS_SIGNAL:
            signal_ec = ecroot.read_ec_object(signal_file, ec_name)
            d["SignalBins"] = _flatten(
                _extract_mc_bins(
                    signal_ec, d["distribution"], filter_systematics=None, scan_key=""
                )
            )
            data_dir = (
                "Build_Stage2/JS_integration/"
                + distribution
                + "/"
                + ec_name
                + "_signal"
            )
            # print(d["MCBins"])
            # print(d["SignalBins"])
        d["FirstRound"] = 0
        d["NumRounds"] = n_rounds
        os.system(
            "rm -rf Build_Stage2/JS_scannfiles/"
            + distribution
            + "/"
            + ec_name
            + ".json >> /dev/null"
        )
        with open(
            "Build_Stage2/JS_scannfiles/" + distribution + "/" + ec_name + ".json", "w"
        ) as jf:
            json.dump(d, jf, indent=2)
        os.system(f"mkdir " + data_dir)
        command = (
            "scanClass  --lut ../bin/lookuptable.bin -j Build_Stage2/JS_scannfiles/"
            + distribution
            + "/"
            + ec_name
            + ".json -s  "
            + shifts_json
            + " -l 0 -n "
            + str(n_rounds)
            + " -o "
            + data_dir
            + f" > logs/output_{ec_name}_{distribution}_{int(IS_SIGNAL)}.txt 2>&1"
        )
        # print(command)
        # exit()
        subprocess.run([command], shell=True, capture_output=True)
        # subprocess.run(["scanClass","--lut","bin/lookuptable.bin","-j","Build_Stage2/JS_scannfiles/",distribution,"/",ec_name,
        #                 ".json -s  ",shifts_json," -l 0 -n ",str(n_rounds)," -o ",data_dir])
        # print("DEBUG")
        # os.system(command)
        # os.system(f"scanClass  --lut bin/lookuptable.bin -j Build_Stage2/JS_scannfiles/"+distribution +"/" + ec_name +
        # ".json -s  "+ shifts_json +" -l 0 -n "+str(n_rounds)+" -o "+ data_dir)

    # os.system(f"scanClass --lut bin/lookuptable.bin -j scann.json -s shifts.json -l 0 -n "+str(n_rounds)+" -o js_test_integration")


def calculation_star(args):
    return calculation(*args)


def main():
    logger = logging.getLogger("main")
    roothelpers.root_setup()
    os.system("rm -rf Build_Stage2/JS_scannfiles ; mkdir Build_Stage2/JS_scannfiles")
    os.system("rm -rf Build_Stage2/JS_integration ; mkdir Build_Stage2/JS_integration")

    os.system("mkdir Build_Stage2/JS_scannfiles/InvMass")
    os.system("mkdir Build_Stage2/JS_integration/InvMass")

    os.system("mkdir Build_Stage2/JS_scannfiles/SumPt")
    os.system("mkdir Build_Stage2/JS_integration/SumPt")

    os.system("rm -rf DEBUG/*")

    os.system("rm -rf logs ; mkdir logs")

    n_toys = 2  # Number of Toys
    n_rounds = 2  # Number of signal to Average

    # Open the ROOT file and loop over all objects
    mc_root_file_name = "/disk1/ykaiser/sharing/Lucas/bg.root"
    mc_root_file = ROOT.TFile.Open(mc_root_file_name)

    # signal_file_name = "/disk1/ykaiser/sharing/Lucas/bg.root"
    # signal_file_name = "/disk1/ykaiser/sharing/Lucas/bg_2000.root"
    # signal_file_name = "/disk1/ykaiser/sharing/Lucas/bg_5000.root"
    signal_file_name = "/disk1/ykaiser/sharing/Lucas/bg_sphaleron_005_inc.root"
    signal_file = ROOT.TFile.Open(signal_file_name)

    signal_names = [key.GetName() for key in signal_file.GetListOfKeys()]
    # mc_names = [key.GetName() for key in mc_root_file.GetListOfKeys()]
    mc_names = get_event_classes(mc_root_file_name)

    # Checking allready included
    for mc_name in mc_names:
        if not mc_name in signal_names:
            err_msg = f"Class {mc_name} only in mc file but missing in signal file."
            raise RuntimeError(err_msg)

    ################################
    ################################
    ################################
    # mc_names = [
    #     "Rec_1Ele_1MET+X",
    #     "Rec_1Ele_1MET",
    #     # "Rec_1Muon_1MET+X",
    #     # "Rec_1Muon_1MET",
    #     # "Rec_1Ele_1bJet_1MET",
    #     # "Rec_1Ele_1bJet_1MET+X",
    #     "Rec_1Ele_2Muon",
    # ]

    # mc_names = list(event_classes.keys())
    # mc_names = get_event_classes(mc_root_file_name)

    # mc_names = ["Rec_1Muon_1MET"]
    ################################
    ################################
    ################################

    mc_root_file.Close()
    signal_file.Close()

    inputs_signal = []
    inputs_background = []
    # mc_names = ["Rec_2Ele_1bJet_1MET"]
    for ec_name in mc_names:
        inputs_background.append(
            (ec_name, n_toys, mc_root_file_name, signal_file_name, False)
        )
        inputs_signal.append(
            (ec_name, n_rounds, mc_root_file_name, signal_file_name, True)
        )

    print("\n\n--> Launching scan jobs ...")

    all_inputs = inputs_background + inputs_signal
    progress_map(
        calculation_star,
        all_inputs,
        initargs=(100,),
        n_cpu=min(100, len(all_inputs)),
        error_behavior="coerce",
        #                         set_error_value=("nan","nan"),
    )

    # print("\n\n--> Starting background ...")
    # progress_map(
    #     calculation_star,
    #     inputs_background,
    #     initargs=(100,),
    #     n_cpu=min(100, len(inputs_background)),
    #     error_behavior="coerce",
    #     #                         set_error_value=("nan","nan"),
    # )

    # print("\n\n--> Starting signal ...")
    # progress_map(
    #     calculation_star,
    #     inputs_signal,
    #     initargs=(100,),
    #     n_cpu=min(100, len(inputs_signal)),
    #     error_behavior="coerce",
    #     #                         set_error_value=("nan","nan"),
    # )

    # P_music = {}
    # JS = {}
    # distributions = ["InvMass", "SumPt"]
    # # distributions = ["InvMass"]
    # i = 0
    # for ec_name in mc_names:
    #     for dist in distributions:
    #         print("----     " + dist + "    ----")
    #         path_signal = f"Build_Stage2/JS_integration/{dist}/{ec_name}_signal/{ec_name}_{dist}_output.csv"
    #         path_bkg = f"Build_Stage2/JS_integration/{dist}/{ec_name}_bkg/{ec_name}_{dist}_output.csv"

    #         if os.path.isfile(path_signal) and os.path.isfile(path_bkg):
    #             p_signal = np.median(np.array(read_outputs(path_signal)))
    #             p_signal_js = np.median(np.array(read_outputs_js(path_signal)))

    #             p_toys = np.array(read_outputs(path_bkg))
    #             p_toys_js = np.array(read_outputs_js(path_bkg))

    #             print(f"Median of P (Signal) (MUSiC/JS):  {p_signal} / {p_signal_js}")
    #             print(
    #                 f"Median of P (Toys) (MUSiC/JS): {np.median(p_toys)} / {np.median(p_toys_js)}"
    #             )

    #             result = max(
    #                 1.0 / float(len(p_toys)),
    #                 np.sum(p_toys <= p_signal) / float(len(p_toys)),
    #             )
    #             result_js = max(
    #                 1.0 / float(len(p_toys_js)),
    #                 np.sum(np.array(p_toys_js) >= p_signal_js) / float(len(p_toys_js)),
    #             )
    #             print(str(ec_name) + ", " + str(dist) + ", MUSiC: " + str(result))
    #             print(str(ec_name) + ", " + str(dist) + ", JS: " + str(result_js))

    #             plt.figure()
    #             counts, bins = np.histogram(
    #                 np.array(read_outputs_js(path_signal)), bins=30, range=(0, 1)
    #             )
    #             plt.hist(np.array(read_outputs_js(path_signal)), bins=30)
    #             plt.vlines(
    #                 p_signal_js, 0, max(counts), color="red", ls=":", linewidth=4.0
    #             )
    #             plt.legend(["Median-Signal-JSD", "Signal-JSD"])
    #             plt.xlabel("JSD")
    #             plt.ylabel("Number of Events")
    #             plt.savefig("DEBUG/" + dist + "_" + ec_name + "js_signal.jpg")
    #             plt.close()

    #             plt.figure()
    #             counts, bins = np.histogram(p_toys_js, bins=30, range=(0, 1))
    #             plt.hist(p_toys_js, bins=30)
    #             plt.vlines(
    #                 p_signal_js, 0, max(counts), color="red", ls=":", linewidth=4.0
    #             )
    #             plt.xlabel("JSD")
    #             plt.ylabel("Number of Events")
    #             plt.legend(["Median-Signal-JSD", "toy-JSD"])
    #             plt.savefig("DEBUG/" + dist + "_" + ec_name + "js_toys.jpg")
    #             plt.close()

    #             plt.figure()
    #             counts, bins = np.histogram(
    #                 np.array(read_outputs(path_signal)), bins=30, range=(0, 0.05)
    #             )
    #             plt.hist(np.array(read_outputs(path_signal)), bins=30)
    #             plt.vlines(p_signal, 0, max(counts), color="red", ls=":", linewidth=4.0)
    #             plt.legend(["Median-Signal-MUSiC", "Signal-MUSiC"])
    #             plt.xlabel("MUSiC-P-Value")
    #             plt.ylabel("Number of Events")
    #             plt.savefig("DEBUG/" + dist + "_" + ec_name + "MUSiC_signal.jpg")
    #             plt.close()

    #             plt.figure()
    #             counts, bins = np.histogram(p_toys, bins=30, range=(0, 0.05))
    #             plt.hist(p_toys, bins=30)
    #             plt.vlines(p_signal, 0, max(counts), color="red", ls=":", linewidth=4.0)
    #             plt.xlabel("MUSiC-P-Value")
    #             plt.ylabel("Number of Events")
    #             plt.legend(["Median-Signal-MUSiC", "toy-MUSiC"])
    #             plt.savefig("DEBUG/" + dist + "_" + ec_name + "MUSiC_toys.jpg")
    #             plt.close()

    #     if i == 10:
    #         # break
    #         pass
    #     i = i + 1


if __name__ == "__main__":
    main()
