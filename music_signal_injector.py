#!/usr/bin/env python3

import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep
import os
import numpy as np
from multiprocessing import Pool
from pprint import pprint
import ROOT
import collections

# MUSiC-Utils
import roothelpers
from ectools.register import ecroot
from ectools.misc import rremove

hep.style.use(hep.style.ROOT)
mpl.use("Agg")

ROOT.gSystem.Load(f"{os.getenv('SCAN_BASE')}/lib/libTEventClass.so")

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


def main():
    mc_ec = ecroot.read_ec_object(
        ecroot.read_root_file(
            "/net/scratch_cms3a/silva/projects/music/music_data_from_yannki_bachelor/bg.root"
        ),
        "Rec_2Muon+X",
    )


if __name__ == "__main__":
    main()
