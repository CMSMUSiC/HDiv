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
from parallelbar import progress_imap,progress_map
import sys
from multiprocessing import Pool
import tqdm 
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep
import subprocess

hep.style.use(hep.style.ROOT)
mpl.use("Agg")


# Not allowing JSON nans because rapidjson (C++) cannot handle them.
JSON_DEFAULTS = dict(allow_nan=False, indent=2)

# Create a container class for the MCBin.
MCBin = collections.namedtuple(
    "MCBin",
    (
        "mcEventsPerProcessGroup",
        "lowerEdge",
        "width",
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
    # When the warning is shown, somebody should implement a handler here!
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


def _hists2bins( mc_hists, uncertainty_hists, unweighted_hists, scan_key=""):
    assert len(mc_hists) > 0

    bins = []
    Nbins = list(mc_hists.values())[0].GetNbinsX()

    for ibin in range(1, Nbins + 1):
        # Obtain lowerEdge and width from 'some' contribution (doesn't matter which)
        lowerEdge = list(mc_hists.values())[0].GetBinLowEdge(ibin)
        width = list(mc_hists.values())[0].GetBinWidth(ibin)

        mcEventsPerProcessGroup = collections.OrderedDict()
        mcStatUncertPerProcessGroup = collections.OrderedDict()
        mcEventsPerProcessGroup = 0
        for process_name, process_hist in mc_hists.items():
            assert process_hist.GetBinLowEdge(ibin) == lowerEdge
            assert process_hist.GetBinWidth(ibin) == width
            mcEventsPerProcessGroup = mcEventsPerProcessGroup +process_hist.GetBinContent(ibin)
            mcStatUncertPerProcessGroup[process_name] = process_hist.GetBinError(ibin)
        if "ReduceAllSyst" in scan_key:
            logger.info("Reducing all systs to 50%")
        mcSysUncerts = collections.OrderedDict()
        # Add uncertainties.
        for systematic_name, systematic_hist in uncertainty_hists.items():
            assert systematic_hist.GetBinLowEdge(ibin) == lowerEdge
            assert systematic_hist.GetBinWidth(ibin) == width

        unweightedEvents = collections.OrderedDict()
        # Add unweighted event numbers and cross sections.
        for process_name, unweighted_hist in unweighted_hists.items():
            assert unweighted_hist["hist"].GetBinLowEdge(ibin) == lowerEdge
            assert unweighted_hist["hist"].GetBinWidth(ibin) == width
            unweightedEvents[process_name] = unweighted_hist["hist"].GetBinContent(ibin)

        bins.append(
            MCBin(
                mcEventsPerProcessGroup=mcEventsPerProcessGroup,
                lowerEdge=lowerEdge,
                width=width,
            )
        )

    return bins






def main():
    logger = logging.getLogger("main")
    roothelpers.root_setup()

    mc_root_file_name = "Build_Stage2/Lucas/bg.root"
    signal_file_name = "Build_Stage2/Lucas/bg_2000.root"
    mc_root_file = ROOT.TFile.Open(mc_root_file_name)
    signal_file = ROOT.TFile.Open(signal_file_name)
    
    n_rounds = 1  # Number of signal to Average
    n_toys = 1             #Number of Toys
    

    
    inputs_signal = []
    inputs_background = []
    mc_name = "Rec_2Ele_1bJet_1MET"
    ec_name = mc_name
    inputs_signal.append((ec_name,n_rounds,mc_root_file_name,signal_file_name,True))
    inputs_background.append((ec_name,n_toys,mc_root_file_name,signal_file_name,False))

    distribution = "InvMass"

    minRegionWidth = 1

    #First data:


        # if(not IS_SIGNAL):   
        #    systematics = collect_systematics([ec_name], mc_root_file, signal_file=None)

    mc_ec = ecroot.read_ec_object(mc_root_file, ec_name)
    signal_ec = ecroot.read_ec_object(signal_file, ec_name)


    MCBINS = _flatten(
            _extract_mc_bins(
                mc_ec, distribution=distribution, filter_systematics=None, scan_key=""
            )
        )    


    SignalBins = _flatten(
                _extract_mc_bins(
                signal_ec, distribution, filter_systematics=None, scan_key=""
                )
                )
   
    bins = []
    Values = []
    for i in range(len(MCBINS)):
        bins.append(MCBINS[i]["lowerEdge"])
        Values.append(MCBINS[i]["mcEventsPerProcessGroup"])

    bins.append(bins[-1]+MCBINS[-1]["width"])
    plt.hist(bins[:-1], bins, weights=Values,alpha = 0.5)
    plt.xlim(0,3000)
    print(bins)
    print(Values)
    plt.ylim(0.001,np.max(np.array(Values)) * 1.1)
    bins_data = []
    Values = []
    for i in range(len(SignalBins)):
        bins_data.append(bins[i]+0.5*MCBINS[i]["width"])
        Values.append(SignalBins[i]["mcEventsPerProcessGroup"])

    plt.scatter(bins_data,Values,color="black",s=6)
    plt.xlim(1,10000)
    
    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel("Energy [GEV]")
    plt.ylabel("Number of Events")
    plt.legend(["Signal","Background"])
    plt.savefig("DEBUG/" + ec_name +"_distibution.png")
    print(Values)

            
if __name__ == "__main__":
    main()
