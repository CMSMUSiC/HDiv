#!/usr/bin/env python3
import roothelpers

from ectools.register import ecroot
from ectools.misc import rremove
import ROOT
import collections
import json
import numpy as np

import logging

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
    # When the warning is shown, somebody should implement a handler here!
    else:
        logging.getLogger().warning("Item '%r' might not be JSON-serializable.", item)
        return item


def _extract_mc_bins(
    event_class, distribution, filter_systematics=None, scan_key=""
):
    if filter_systematics is None:
        filter_systematics = []
    print("Debuging -MCBINS - 1")    
    mc_hists = ecroot.event_yield_by_process_group(
        event_class, distribution, aggregation_level="none"
    )
    print("Debuging -MCBINS - 2")    
    uncertainty_hists = ecroot.combined_uncertainty_by_systematic_name(
        event_class,
        distribution,
        symmetrize=False,
        filter_systematics=filter_systematics,
    )
    print("Debuging -MCBINS - 3")    
    unweighted_hists = cls._extract_histograms(event_class, distribution)
    retval = cls._hists2bins(mc_hists, uncertainty_hists, unweighted_hists, scan_key)
    print("Debuging -MCBINS - 4")    
    for hist in mc_hists.values():
        hist.Delete()
    for hist in uncertainty_hists.values():
        hist.Delete()
    for hists in unweighted_hists.values():
        hists["hist"].Delete()
    print("Debuging -MCBINS - 5")    
    return retval


def _extract_histograms(cls, event_class, distribution):
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


def _hists2bins(self, mc_hists, uncertainty_hists, unweighted_hists, scan_key=""):
    assert len(mc_hists) > 0

    bins = []
    Nbins = mc_hists.values()[0].GetNbinsX()

    for ibin in range(1, Nbins + 1):
        # Obtain lowerEdge and width from 'some' contribution (doesn't matter which)
        lowerEdge = mc_hists.values()[0].GetBinLowEdge(ibin)
        width = mc_hists.values()[0].GetBinWidth(ibin)

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


def main():
    logger = logging.getLogger("main")
    roothelpers.root_setup()

    # configs
    ec_names = ["Rec_2Muon+X"]
    n_rounds = 3            #Number of toys

    # Open the ROOT file and loop over all objects
    mc_root_file = ROOT.TFile.Open(
        "/disk1/ykaiser/sharing/Lucas/bg.root"
    )
    

    signal_file = ROOT.TFile.Open("/disk1/ykaiser/sharing/Lucas/bg_2000.root")
    signal_names = [key.GetName() for key in signal_file.GetListOfKeys()]
    mc_names = [key.GetName() for key in mc_root_file.GetListOfKeys()]

    for mc_name in mc_names:
        if not mc_name in signal_names:
            err_msg = "Class %s only in mc file but missing in signal file" % mc_name
            logger.error(err_msg)
            err_msg = "Maybe you forgot to merge background and signal "
            err_msg += "or merged with --filter option ?"
            logger.error(err_msg)

    key = mc_root_file.GetKey(ec_names[0])
    event_class = key.ReadObj()
    print(f"Event classes: {event_class.getDistTypes()}")

    # create shifts.json
    shifts_json = "shifts.json"
    systematics = collect_systematics(ec_names, mc_root_file, signal_file)
    shifts = create_systematic_shifts(systematics, n_rounds)
    with open(shifts_json, "w") as file:
        json.dump(_flatten(shifts), file, **JSON_DEFAULTS)

    # Make Scan JSON
    d = {
        "gridpack_name": "Dummy_gridpack_name",
        "minRegionWidth": 1, # Just used for invariant Mass / change later
        "coverageThreshold": 0.0, #Same for all
        "regionYieldThreshold": 1e-06, #Same for all
        "sigmaThreshold": 0.6, #Same for all
        "integralScan": False, #Same for all
        "skipLookupTable": False, #Same for all
        "noLowStatsTreatment": False, #Same for all
        "widthLowStatsRegions": 4, #Same for all
        "thresholdLowStatsDominant": 0.9, #Same for all
        "mcStatUncertScaleFactor": 1.0, #Same for all
        "dicedMCUncertScaleFactor": 1.0, #Same for all
        "dicedSignalUncertScaleFactor": 1.0, #Same for all
        "hash": "Dummy_hash", #Create Hash later
        "name": ec_names[0],  #Automatize
        "distribution": "InvMass", # automatize ("SumPt")
    }

    mc_ec = ecroot.read_ec_object(mc_root_file, ec_names[0])
    d["MCBins"] = _flatten(
        _extract_mc_bins(
            mc_ec, distribution = d["distribution"], filter_systematics = None, scan_key = ""
        )
    )
    print("Debuging")
    # if self.data:
    #     data_ec = ecroot.read_ec_object(self.data_root_file, self.ec_name)
    #     empty = False
    #     if not data_ec:
    #         data_ec = mc_ec
    #         empty = True
    #     hist = ecroot.total_event_yield(data_ec, self.distribution)
    #     d["DataBins"] = _flatten(
    #         roothelpers.root_map_hist(hist.GetBinContent, hist, empty)
    #    )
    signal_ec = ecroot.read_ec_object(signal_file, ec_names[0])
    # merged_ec = mc_ec.Copy()
    # if signal_ec:
    #    # merge signal and background to build the s+b hypothesis
    #    all_processes = merged_ec.getGlobalProcessList()
    #    # build a root set object to interact with TEventClass object
    #    processesToMerge = r.set( 'string' )()
    #    for proc in all_processes:
    #        processesToMerge.insert( processesToMerge.begin(), str( proc ) )
    #    merged_ec.addEventClass( signal_ec, processesToMerge, False )
    # d['SignalBins'] = _flatten( self._extract_mc_bins( merged_ec,
    #                                                   self.distribution,
    #                                                   self.filter_systematics ))
    d["SignalBins"] = _flatten(
        self._extract_mc_bins(
            signal_ec, d["distribution"], filter_systematics = None ,scan_key = ""
        )
    )
    d["FirstRound"] = 0
    d["NumRounds"] = n_rounds


    with open("scann.json", "wb") as jf:
        json.dump(d, jf, indent=2)


if __name__ == "__main__":
    main()
