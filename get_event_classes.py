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


def get_event_classes(bg_mc_root_file_name,signal_mc_root_file_name):
    roothelpers.root_setup()

    # Open the ROOT file and loop over all objects
    # mc_root_file_name = "/disk1/ykaiser/sharing/Lucas/bg.root"
    mc_root_file = ROOT.TFile.Open(bg_mc_root_file_name)
    mc_root_file_signal = ROOT.TFile.Open(signal_mc_root_file_name)

    mc_names = [key.GetName() for key in mc_root_file.GetListOfKeys()]

    #new_mc_names = set()
    new_mc_names = {}
    SF_InvMass = []
    SF_SumPt = []
    SF_MET = []
    #shady_classes = set()

    print(f"Evaluating usefull classes ...")
    for ec_name in tqdm.tqdm(mc_names):
        key_bkg = mc_root_file.GetKey(ec_name)
        key_signal = mc_root_file_signal.GetKey(ec_name)
        event_class_bkg = key_bkg.ReadObj()
        event_class_singal = key_signal.ReadObj()
        # if key.GetClassName() == "TEventClass":
        if (
            "Empty" not in ec_name
            and ("Muon" in ec_name or "Ele" in ec_name)
            and "GammaEE" not in ec_name
#            and "+X" in ec_name
        ):
            
            #Testing Signal

            integral_sum_pt_signal = 0
            integral_mass_signal = 0
            integral_MET_signal = 0
            for _process, histos in event_class_singal.getAllProcHistoMap():
                if histos["SumPt"] and histos["InvMass"]:
                    integral_sum_pt_signal += histos["SumPt"].Integral()
                    integral_mass_signal += histos["InvMass"].Integral()
                if histos["MET"]:
                    integral_MET_signal += histos["MET"].Integral()


            #Testing Background

            integral_sum_pt = 0
            integral_mass = 0
            integral_MET = 0
            for _process, histos in event_class_bkg.getAllProcHistoMap():
                if histos["SumPt"] and histos["InvMass"]:
                    integral_sum_pt += histos["SumPt"].Integral()
                    integral_mass += histos["InvMass"].Integral()
                if histos["MET"]:
                    integral_MET += histos["MET"].Integral()    
            if integral_sum_pt >= 0.1 and integral_mass > 0.1:
                new_mc_names[ec_name]=integral_mass
                SF_InvMass.append(100*((integral_mass_signal/integral_mass) -1))
                SF_SumPt.append(100*((integral_sum_pt_signal/integral_sum_pt) -1))
                # if( (integral_sum_pt <= 1.0) or (integral_mass <= 1.0) ):   
                #     shady_classes.add(ec_name)
            if integral_MET >= 0.1:    
                SF_MET.append(100*( (integral_MET_signal/integral_MET) -1))
                # if((integral_MET <= 1.0)):   
                #     shady_classes.add(ec_name)






    mc_root_file.Close()
    print(f"... done.\nTotal classes: {len(new_mc_names)}")
    #shady_classes = list(shady_classes)
    # for i in range(len(shady_classes)):
    #     print(shady_classes[i]+",")

    new_mc_names = np.array(sorted(new_mc_names.items(), key=lambda x:x[1],reverse = True))[:,0]

    return new_mc_names, SF_InvMass,SF_InvMass,SF_MET


if __name__ == "__main__":
    get_event_classes()
