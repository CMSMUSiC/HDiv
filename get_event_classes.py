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

hep.style.use(hep.style.ROOT)
mpl.use("Agg")


def get_event_classes(bg_mc_root_file_name):
    roothelpers.root_setup()

    # Open the ROOT file and loop over all objects
    # mc_root_file_name = "/disk1/ykaiser/sharing/Lucas/bg.root"
    mc_root_file = ROOT.TFile.Open(bg_mc_root_file_name)

    mc_names = [key.GetName() for key in mc_root_file.GetListOfKeys()]

    new_mc_names = set()
    print(f"Evaluating usefull classes ...")
    for ec_name in tqdm.tqdm(mc_names):
        key = mc_root_file.GetKey(ec_name)
        event_class = key.ReadObj()
        # if key.GetClassName() == "TEventClass":
        if (
            "Empty" not in ec_name
            and ("Muon" in ec_name or "Ele" in ec_name)
            and "GammaEE" not in ec_name
            and "+X" in ec_name
        ):
            integral_sum_pt = 0
            integral_mass = 0
            for _process, histos in event_class.getAllProcHistoMap():
                if histos["SumPt"] and histos["InvMass"]:
                    integral_sum_pt += histos["SumPt"].Integral()
                    integral_mass += histos["InvMass"].Integral()
            if integral_sum_pt >= 0.1 and integral_mass > 0.1:
                new_mc_names.add(ec_name)
                # print(ec_name)

    mc_root_file.Close()
    print(f"... done.\nTotal classes: {len(new_mc_names)}")

    return new_mc_names


if __name__ == "__main__":
    get_event_classes()
