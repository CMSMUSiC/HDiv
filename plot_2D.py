import matplotlib.pyplot as plt
import mplhep as hep
import matplotlib as mpl
import os
import csv
import numpy as np
import ROOT
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

# mc_names = [
#         "Rec_1Ele_1MET",
#         "Rec_1Muon_1MET",
#         "Rec_1Ele_1bJet_1MET",
#         "Rec_1Ele_1bJet_1MET+X",
#         "Rec_1Ele_2Muon",
#         # Exclusive Class
#         "Rec_2Muon",
#         "Rec_1Muon",
#         "Rec_1Muon_1Jet",
#         "Rec_2Ele",
#         "Rec_1Muon_2Jet",
#         "Rec_2Muon_1Jet",
#         "Rec_1Ele_1Jet",
#         "Rec_1Ele_2Jet",
#         "Rec_1Muon_1Jet_1MET",
#         "Rec_1Muon_3Jet",
#         "Rec_1Muon_1bJet",
#         "Rec_2Ele_1Jet",
#         "Rec_2Muon_2Jet",
#         "Rec_1Muon_1bJet_1Jet",
#         "Rec_1Muon_2Jet_1MET",
#         "Rec_1Muon_MET",
#         "Rec_1Muon_1bJet_2Jet",
#         "Rec_1Ele"
#         "Rec_1Ele_3Jet"
#         "Rec_1Muon_4Jet"
#         "Rec_1Muon_3Jet_1MET"
#         "Rec_2Ele_2Jet"
#         "Rec_1Muon_1bJet_3Jet"
#         "Rec_2Muon_1bJet"
#         "Rec_1Ele_1Jet_1MET"
#         # Inclusive Class
#         "Rec_2Muon+X",
#         "Rec_1Muon+X",
#         "Rec_1Muon_1Jet+X",
#         "Rec_1Ele+X",
#         "Rec_1Muon_2Jet+X",
#         "Rec_2Ele+X",
#         "Rec_1Ele_1Jet+X",
#         "Rec_2Muon_1Jet+X",
#         "Rec_1Muon_1MET+X",
#         "Rec_1Muon_1bJet+X",
#         "Rec_1Muon_1Jet_1MET+X",
#         "Rec_1Ele_2Jet+X",
#         "Rec_1Muon_3Jet+X",
#         "Rec_1Muon_1bJet_1Jet+X",
#         "Rec_1Muon_2Jet_1MET+X",
#         "Rec_2Ele_1Jet+X",
#         "Rec_2Muon_2Jet+X",
#         "Rec_1Muon_1bJet_2Jet+X",
#         "Rec_1Ele_3Jet+X",
#         "Rec_1Ele_1MET+X",
#         "Rec_1Muon_4Jet+X",
#         "Rec_1Ele_1bJet+X",
#         "Rec_1Muon_3Jet_1MET+X",
#         "Rec_1Muon_1bJet_1MET+X",
#         "Rec_1Ele_1Jet_1MET+X",


#      ]
mc_names =  ['Rec_Empty+X', 'Rec_1Muon+X', 'Rec_1Muon+NJets', 'Rec_1Jet+X', 'Rec_2Muon+X', 'Rec_2Muon+NJets', 'Rec_2Muon', 'Rec_1Muon_1Jet+X', 'Rec_1Muon', 'Rec_1Muon_1Jet+NJets', 'Rec_1Muon_1Jet', 'Rec_2Jet+X', 'Rec_1Ele+X', 'Rec_1Muon_2Jet+X', 'Rec_2Ele+X', 'Rec_2Ele+NJets', 'Rec_1Muon_2Jet+NJets', 'Rec_1Ele_1Jet+X', 'Rec_2Ele', 'Rec_1Muon_2Jet', 'Rec_1Ele+NJets', 'Rec_2Muon_1Jet+X', 'Rec_1Ele_1Jet+NJets', 'Rec_2Muon_1Jet+NJets', 'Rec_1MET+X', 'Rec_1Muon_1MET+X', 'Rec_2Muon_1Jet', 'Rec_3Jet+X', 'Rec_1bJet+X', 'Rec_1Jet_1MET+X', 'Rec_1Muon_1MET+NJets', 'Rec_1Muon_1bJet+X', 'Rec_1Ele_1Jet', 'Rec_1Muon_1Jet_1MET+X', 'Rec_1GammaEB+X', 'Rec_1Muon_3Jet+X', 'Rec_1Ele_2Jet+X', 'Rec_1Muon_1Jet_1MET+NJets', 'Rec_1GammaEB_1Jet+X', 'Rec_1bJet_1Jet+X', 'Rec_1GammaEB+NJets', 'Rec_1GammaEB_1Jet+NJets', 'Rec_1Muon_1bJet+NJets', 'Rec_1Muon_1bJet_1Jet+X', 'Rec_1Ele_2Jet+NJets', 'Rec_2Jet_1MET+X', 'Rec_1Muon_3Jet+NJets', 'Rec_1Muon_2Jet_1MET+X', 'Rec_1Muon_1Jet_1MET', 'Rec_1Muon_1bJet_1Jet+NJets', 'Rec_1Ele_2Jet', 'Rec_1GammaEB_2Jet+X', 'Rec_1Muon_3Jet', 'Rec_1GammaEB_2Jet+NJets', 'Rec_1Muon_2Jet_1MET+NJets', 'Rec_1bJet_2Jet+X', 'Rec_1GammaEB_1Jet', 'Rec_2Ele_1Jet+X', 'Rec_1Muon_1bJet_2Jet+X', 'Rec_2Muon_2Jet+X', 'Rec_4Jet+X', 'Rec_2Ele_1Jet+NJets', 'Rec_2Muon_2Jet+NJets', 'Rec_1GammaEB_2Jet', 'Rec_1Muon_1bJet', 'Rec_1Muon_2Jet_1MET', 'Rec_1Muon_1MET', 'Rec_1Ele_3Jet+X', 'Rec_2Muon_2Jet', 'Rec_2Ele_1Jet', 'Rec_1Muon_1bJet_1Jet', 'Rec_1Jet+NJets', 'Rec_1Muon_1bJet_2Jet+NJets', 'Rec_3Jet_1MET+X', 'Rec_1Ele_1MET+X', 'Rec_1Muon_4Jet+X', 'Rec_1bJet_1MET+X', 'Rec_1Ele_3Jet+NJets', 'Rec_1Muon_3Jet_1MET+X', 'Rec_1Ele_1bJet+X', 'Rec_1Ele_1Jet_1MET+X', 'Rec_1Muon_1bJet_1MET+X', 'Rec_1Ele_1MET+NJets', 'Rec_1bJet_1Jet_1MET+X', 'Rec_1Muon_1bJet_2Jet', 'Rec_1bJet_3Jet+X', 'Rec_1Muon_3Jet_1MET+NJets', 'Rec_1Ele_3Jet', 'Rec_1Muon_1bJet_1Jet_1MET+X', 'Rec_1Jet', 'Rec_1Muon_1bJet_1MET+NJets', 'Rec_1GammaEB_3Jet+X', 'Rec_1Ele_1Jet_1MET+NJets', 'Rec_1Muon_4Jet+NJets', 'Rec_2Jet+NJets', 'Rec_2bJet+X', 'Rec_1Ele', 'Rec_1Ele_1bJet_1Jet+X', 'Rec_1Muon_1bJet_3Jet+X', 'Rec_1GammaEB_3Jet+NJets', 'Rec_2Muon_1bJet+X', 'Rec_1Ele_1Muon+X', 'Rec_1Muon_1bJet_1Jet_1MET+NJets', 'Rec_1Muon_2bJet+X', 'Rec_1Muon_3Jet_1MET', 'Rec_1Muon_4Jet', 'Rec_1Ele_2Jet_1MET+X', 'Rec_2Muon_1bJet+NJets', 'Rec_1bJet_2Jet_1MET+X', 'Rec_1Ele_1bJet+NJets', 'Rec_2Ele_2Jet+X', 'Rec_1GammaEB_3Jet', 'Rec_2Jet', 'Rec_2bJet_1Jet+X', 'Rec_5Jet+X', 'Rec_1Muon_1bJet_3Jet+NJets', 'Rec_2Ele_2Jet+NJets', 'Rec_1Muon_1bJet_2Jet_1MET+X', 'Rec_1Muon_2bJet+NJets', 'Rec_1Muon_1GammaEB+X', 'Rec_1Ele_2Jet_1MET+NJets', 'Rec_4Jet_1MET+X', 'Rec_1Ele_1Muon_1Jet+X', 'Rec_1Ele_4Jet+X', 'Rec_1Muon_2bJet_1Jet+X', 'Rec_1GammaEB_1MET+X', 'Rec_1Muon_1bJet_2Jet_1MET+NJets', 'Rec_1Ele_1bJet_1Jet+NJets', 'Rec_2Muon_3Jet+X', 'Rec_1GammaEB_1Jet_1MET+X', 'Rec_2Ele_2Jet', 'Rec_1Ele_1bJet_2Jet+X', 'Rec_1Ele_1Muon+NJets', 'Rec_2Muon_1bJet', 'Rec_1Muon_1bJet_3Jet', 'Rec_1Ele_1Jet_1MET', 'Rec_2Muon_1MET+X', 'Rec_1GammaEB_1MET+NJets', 'Rec_1Muon_4Jet_1MET+X', 'Rec_1GammaEB_1Jet_1MET+NJets', 'Rec_2Muon_3Jet+NJets', 'Rec_1Muon_1GammaEB+NJets', 'Rec_1Muon_2bJet_1Jet+NJets', 'Rec_1Muon_5Jet+X', 'Rec_1Ele_4Jet+NJets', 'Rec_2Muon_1bJet_1Jet+X', 'Rec_2Muon_3Jet', 'Rec_1Muon_1bJet_1Jet_1MET', 'Rec_1Muon_4Jet_1MET+NJets', 'Rec_1bJet_4Jet+X', 'Rec_3Jet+NJets', 'Rec_1Ele_2Jet_1MET', 'Rec_2Muon_1MET+NJets', 'Rec_1Ele_3Jet_1MET+X', 'Rec_1GammaEB_2Jet_1MET+X', 'Rec_1GammaEB_4Jet+X', 'Rec_1bJet_3Jet_1MET+X', 'Rec_1Ele_1Muon_1bJet+X', 'Rec_1GammaEB_2Jet_1MET+NJets', 'Rec_1Ele_4Jet', 'Rec_1Ele_1Muon_1Jet+NJets', 'Rec_2Muon_1bJet_1Jet+NJets', 'Rec_1Muon_1bJet_2Jet_1MET', 'Rec_1Muon_1GammaEB_1Jet+X', 'Rec_1GammaEB_4Jet+NJets', 'Rec_1Ele_1MET', 'Rec_2bJet_2Jet+X', 'Rec_1Ele_1bJet_2Jet+NJets', 'Rec_1Ele_1bJet_1MET+X', 'Rec_1Muon_1bJet_4Jet+X', 'Rec_2Muon_1Jet_1MET+X', 'Rec_1GammaEB_2Jet_1MET', 'Rec_1Muon_4Jet_1MET', 'Rec_1Muon_1bJet_3Jet_1MET+X', 'Rec_1Muon_2bJet_1Jet', 'Rec_1Ele_3Jet_1MET+NJets', 'Rec_3Jet', 'Rec_1Muon_2bJet_2Jet+X', 'Rec_1Muon_1GammaEB', 'Rec_1Ele_1bJet_1Jet', 'Rec_1Muon_5Jet+NJets', 'Rec_1Ele_1Muon_2Jet+X', 'Rec_2Muon_1bJet_1Jet', 'Rec_1Muon_1bJet_3Jet_1MET+NJets', 'Rec_1GammaEB_4Jet', 'Rec_1Ele_1bJet_1Jet_1MET+X', 'Rec_1Ele_1Muon_1MET+X', 'Rec_2Ele_1bJet+X', 'Rec_1Muon_1GammaEB_1Jet+NJets', 'Rec_1GammaEB_1bJet+X', 'Rec_2Muon_1Jet_1MET+NJets', 'Rec_1Ele_1Muon_1bJet+NJets', 'Rec_1Muon_1bJet_1MET', 'Rec_1Ele_1bJet_3Jet+X', 'Rec_1Muon_2bJet', 'Rec_2bJet_1MET+X', 'Rec_1Ele_1Muon', 'Rec_1Ele_1Muon_1Jet', 'Rec_1Muon_5Jet', 'Rec_1Ele_1bJet', 'Rec_1Muon_1bJet_4Jet+NJets', 'Rec_1Muon_2bJet_2Jet+NJets', 'Rec_1Ele_1bJet_2Jet', 'Rec_1Ele_1Muon_1bJet_1Jet+X', 'Rec_2Ele_1bJet+NJets', 'Rec_1Ele_3Jet_1MET', 'Rec_5Jet_1MET+X', 'Rec_1Muon_2bJet_1MET+X', 'Rec_1GammaEB_1bJet+NJets', 'Rec_1Ele_1Muon_1Jet_1MET+X', 'Rec_1GammaEB_1Jet_1MET', 'Rec_6Jet+X', 'Rec_1Ele_1bJet_1MET+NJets', 'Rec_1GammaEB_1bJet_1Jet+X', 'Rec_1Muon_1bJet_3Jet_1MET', 'Rec_1Muon_1GammaEB_1Jet', 'Rec_2Ele_3Jet+X', 'Rec_1Ele_2bJet+X', 'Rec_2Muon_1MET', 'Rec_1Ele_5Jet+X', 'Rec_2bJet_1Jet_1MET+X', 'Rec_1Ele_1Muon_1MET+NJets', 'Rec_1Muon_1bJet_4Jet', 'Rec_1Muon_2bJet_1MET+NJets', 'Rec_1Ele_1bJet_1Jet_1MET+NJets', 'Rec_2Ele_3Jet+NJets', 'Rec_1GammaEB', 'Rec_1Ele_1bJet_2Jet_1MET+X', 'Rec_1Muon_5Jet_1MET+X', 'Rec_1Muon_2bJet_2Jet', 'Rec_2Muon_1bJet_1MET+X', 'Rec_2Muon_2Jet_1MET+X', 'Rec_2Muon_1Jet_1MET', 'Rec_1Ele_1Muon_2Jet+NJets', 'Rec_1GammaEB_1bJet_1Jet+NJets', 'Rec_1Muon_2bJet_1Jet_1MET+X', 'Rec_1Ele_1bJet_3Jet+NJets', 'Rec_1Ele_1Muon_1bJet_1Jet+NJets', 'Rec_1Ele_4Jet_1MET+X', 'Rec_Empty', 'Rec_2Ele_1MET+X', 'Rec_4Jet+NJets', 'Rec_2Ele_3Jet', 'Rec_2Muon_1bJet_2Jet+X', 'Rec_2Muon_1bJet_1MET+NJets', 'Rec_1Ele_1Muon_1Jet_1MET+NJets', 'Rec_1bJet_4Jet_1MET+X', 'Rec_1Muon_2bJet_1Jet_1MET+NJets', 'Rec_2Muon_1GammaEB+X', 'Rec_2Ele_1bJet_1Jet+X', 'Rec_2Ele_1bJet', 'Rec_1Muon_5Jet_1MET+NJets', 'Rec_1Muon_1GammaEB_2Jet+X', 'Rec_2Muon_1GammaEB+NJets', 'Rec_2Muon_4Jet+X', 'Rec_1Muon_6Jet+X', 'Rec_1bJet_5Jet+X', 'Rec_2bJet_3Jet+X', 'Rec_1Ele_1Muon_1bJet', 'Rec_2Muon_2Jet_1MET+NJets', 'Rec_1Ele_1bJet_2Jet_1MET+NJets', 'Rec_1Ele_2bJet_1Jet+X', 'Rec_1Ele_1GammaEB+X', 'Rec_1Ele_5Jet+NJets', 'Rec_1Ele_1Muon_2Jet', 'Rec_1Muon_1bJet_4Jet_1MET+X', 'Rec_1Ele_4Jet_1MET+NJets', 'Rec_4Jet', 'Rec_1GammaEB_5Jet+X', 'Rec_1Ele_1Muon_1bJet_1Jet', 'Rec_2Ele_1MET+NJets', 'Rec_2Muon_4Jet+NJets', 'Rec_1Ele_1bJet_3Jet', 'Rec_1Ele_1Muon_1bJet_1MET+X', 'Rec_1GammaEB_1bJet_2Jet+X', 'Rec_2Muon_1bJet_2Jet+NJets', 'Rec_1Muon_2bJet_3Jet+X', 'Rec_1Muon_1bJet_4Jet_1MET+NJets', 'Rec_2Ele_1bJet_1Jet+NJets', 'Rec_2Ele_1Jet_1MET+X', 'Rec_1Ele_1Muon_2Jet_1MET+X', 'Rec_1Muon_5Jet_1MET', 'Rec_2bJet_2Jet_1MET+X', 'Rec_2Muon_2bJet+X', 'Rec_2Muon_1bJet_1Jet_1MET+X', 'Rec_1GammaEB_5Jet+NJets', 'Rec_1Muon_1bJet_5Jet+X', 'Rec_2Muon_1GammaEB', 'Rec_1Ele_1GammaEB_1Jet+X', 'Rec_1Ele_1Muon_1bJet_1MET+NJets', 'Rec_1Ele_5Jet', 'Rec_1Ele_1Muon_3Jet+X', 'Rec_2Muon_4Jet', 'Rec_2Muon_1bJet_1Jet_1MET+NJets', 'Rec_1Muon_1GammaEB_2Jet+NJets', 'Rec_1Ele_2bJet+NJets', 'Rec_1Ele_1bJet_4Jet+X', 'Rec_2Muon_1bJet_2Jet', 'Rec_1Ele_1GammaEB+NJets', 'Rec_2Muon_2Jet_1MET', 'Rec_1Ele_4Jet_1MET', 'Rec_1Muon_2bJet_2Jet_1MET+X', 'Rec_1GammaEB_1bJet_2Jet+NJets', 'Rec_1GammaEB_1bJet_1Jet', 'Rec_1Ele_1bJet_3Jet_1MET+X', 'Rec_2Muon_2bJet+NJets', 'Rec_1Ele_1Muon_1bJet_2Jet+X', 'Rec_1Ele_1Muon_1Jet_1MET', 'Rec_1GammaEB_5Jet', 'Rec_1Muon_2bJet_2Jet_1MET+NJets', 'Rec_1bJet+NJets', 'Rec_2Ele_1bJet_1Jet', 'Rec_2Ele_1Jet_1MET+NJets', 'Rec_1Muon_1bJet_4Jet_1MET', 'Rec_1Ele_1Muon_2Jet_1MET+NJets', 'Rec_1Muon_2bJet_3Jet+NJets', 'Rec_1Ele_1GammaEB_1Jet+NJets', 'Rec_1Ele_2bJet_1Jet+NJets', 'Rec_1Muon_6Jet+NJets', 'Rec_1Muon_2bJet_1Jet_1MET', 'Rec_1Ele_1Muon_1bJet_1Jet_1MET+X', 'Rec_1Ele_1bJet_2Jet_1MET', 'Rec_1Muon_1GammaEB_2Jet', 'Rec_1GammaEB_1bJet', 'Rec_1GammaEB_3Jet_1MET+X', 'Rec_1Muon_1GammaEB_1MET+X', 'Rec_1Ele_1bJet_3Jet_1MET+NJets', 'Rec_1Ele_1bJet_1Jet_1MET', 'Rec_2Muon_1bJet_1MET', 'Rec_1Ele_2bJet_2Jet+X', 'Rec_6Jet_1MET+X', 'Rec_1MET+NJets', 'Rec_1Muon_1bJet_5Jet+NJets', 'Rec_1Ele_1Muon_1bJet_1Jet_1MET+NJets', 'Rec_2Muon_1bJet_1Jet_1MET', 'Rec_1Jet_1MET+NJets', 'Rec_2Muon_3Jet_1MET+X', 'Rec_2Muon_2bJet', 'Rec_1bJet_1Jet+NJets', 'Rec_1Muon_6Jet', 'Rec_1Muon_2bJet_3Jet', 'Rec_1Ele_1Muon_2bJet+X', 'Rec_1Ele_1bJet_4Jet+NJets', 'Rec_1Muon_1GammaEB_1MET+NJets', 'Rec_2GammaEB+X', 'Rec_1GammaEB_1bJet_2Jet', 'Rec_1Muon_1GammaEB_1Jet_1MET+X', 'Rec_1Ele_1Muon_2Jet_1MET', 'Rec_1Ele_1Muon_1bJet_2Jet+NJets', 'Rec_1Muon_2bJet_2Jet_1MET', 'Rec_1Ele_2bJet_1MET+X', 'Rec_1Ele_5Jet_1MET+X', 'Rec_1GammaEB_3Jet_1MET+NJets', 'Rec_1Muon_1bJet_5Jet', 'Rec_1Ele_6Jet+X', 'Rec_1Muon_2bJet_1MET', 'Rec_2Ele_2Jet_1MET+X', 'Rec_1GammaEB_1bJet_3Jet+X', 'Rec_1bJet_5Jet_1MET+X', 'Rec_1Muon_6Jet_1MET+X', 'Rec_2Muon_3Jet_1MET+NJets', 'Rec_2GammaEB+NJets', 'Rec_1Ele_1Muon_3Jet+NJets', 'Rec_2Ele_1bJet_1MET+X', 'Rec_1Ele_1Muon_1MET', 'Rec_1Ele_1GammaEB_2Jet+X', 'Rec_2GammaEB_1Jet+X', 'Rec_1Muon_1GammaEB_1bJet+X', 'Rec_1Ele_1GammaEB_1Jet', 'Rec_1Muon_1GammaEB_3Jet+X', 'Rec_2Ele_1bJet_2Jet+X', 'Rec_2Muon_1GammaEB_1Jet+X', 'Rec_1Ele_1Muon_2bJet+NJets', 'Rec_1Muon_1GammaEB_1Jet_1MET+NJets', 'Rec_2Ele_1Jet_1MET', 'Rec_1Ele_1bJet_3Jet_1MET', 'Rec_1Ele_1bJet_4Jet', 'Rec_2GammaEB_1Jet+NJets', 'Rec_2Ele_1bJet_1MET+NJets', 'Rec_2Muon_1GammaEB_1Jet+NJets', 'Rec_2Muon_1bJet_2Jet_1MET+X', 'Rec_2bJet_3Jet_1MET+X', 'Rec_2Ele_1MET', 'Rec_5Jet+NJets', 'Rec_2Ele_4Jet+X', 'Rec_2Muon_1bJet_3Jet+X', 'Rec_1Ele_1Muon_1bJet_1MET', 'Rec_1Ele_2bJet_2Jet+NJets', 'Rec_1Ele_1Muon_1bJet_2Jet', 'Rec_2bJet_4Jet+X', 'Rec_1Ele_1Muon_1bJet_1Jet_1MET', 'Rec_1Ele_5Jet_1MET+NJets', 'Rec_2Ele_2Jet_1MET+NJets', 'Rec_1Ele_1Muon_3Jet_1MET+X', 'Rec_1Muon_1bJet_5Jet_1MET+X', 'Rec_2Muon_1bJet_2Jet_1MET+NJets', 'Rec_1Ele_2bJet_1Jet', 'Rec_1Muon_6Jet_1MET+NJets', 'Rec_2Muon_2bJet_1Jet+X', 'Rec_1Ele_1Muon_3Jet', 'Rec_1GammaEB_1bJet_3Jet+NJets', 'Rec_1Ele_2bJet_1Jet_1MET+X', 'Rec_2Jet_1MET+NJets', 'Rec_2Muon_3Jet_1MET', 'Rec_2Ele_4Jet+NJets', 'Rec_1Muon_2bJet_3Jet_1MET+X', 'Rec_1Muon_1bJet_5Jet_1MET+NJets', 'Rec_1Ele_1GammaEB_2Jet+NJets', 'Rec_1Ele_6Jet+NJets', 'Rec_1GammaEB_6Jet+X', 'Rec_1Muon_2bJet_4Jet+X', 'Rec_1Ele_1bJet_4Jet_1MET+X', 'Rec_2Muon_1GammaEB_1Jet', 'Rec_1Ele_2bJet_1MET+NJets', 'Rec_5Jet', 'Rec_2Ele_1bJet_2Jet+NJets', 'Rec_1bJet_2Jet+NJets', 'Rec_1Muon_2bJet_3Jet_1MET+NJets', 'Rec_1Muon_1GammaEB_1bJet_1Jet+X', 'Rec_1GammaEB_3Jet_1MET', 'Rec_1Ele_1Muon_2bJet', 'Rec_1bJet_1Jet', 'Rec_3Muon+X', 'Rec_1Ele_1bJet_1MET', 'Rec_1Muon_1GammaEB_1bJet+NJets', 'Rec_1Ele_1Muon_1bJet_2Jet_1MET+X', 'Rec_2Ele_1bJet_1Jet_1MET+X', 'Rec_1Ele_1Muon_3Jet_1MET+NJets', 'Rec_1Muon_6Jet_1MET', 'Rec_1Ele_5Jet_1MET', 'Rec_1Muon_1GammaEB_3Jet+NJets', 'Rec_1GammaEB_4Jet_1MET+X', 'Rec_2Ele_4Jet', 'Rec_1Muon_1GammaEB_2Jet_1MET+X', 'Rec_2Muon_2bJet_1Jet+NJets', 'Rec_1GammaEB_6Jet+NJets', 'Rec_2Ele_2bJet+X', 'Rec_1Ele_1Muon_1bJet_2Jet_1MET+NJets', 'Rec_1Ele_2bJet_2Jet', 'Rec_1Ele_1bJet_5Jet+X', 'Rec_2Muon_5Jet+X', 'Rec_2Ele_1bJet_1Jet_1MET+NJets', 'Rec_1Jet_1MET', 'Rec_1Ele_2bJet_1Jet_1MET+NJets', 'Rec_2Muon_1bJet_3Jet+NJets', 'Rec_2Muon_1bJet_2Jet_1MET', 'Rec_1Ele_1Muon_4Jet+X', 'Rec_1Ele_2Muon+X', 'Rec_1Ele_1bJet_4Jet_1MET+NJets', 'Rec_2Ele_2Jet_1MET', 'Rec_1Muon_1bJet_5Jet_1MET', 'Rec_2GammaEB_2Jet+X', 'Rec_1GammaEB_1bJet_1MET+X', 'Rec_3Muon+NJets', 'Rec_1GammaEB_1bJet_3Jet', 'Rec_1Ele_2bJet_3Jet+X', 'Rec_2Ele_1bJet_2Jet', 'Rec_1Ele_1Muon_1bJet_3Jet+X', 'Rec_2GammaEB_2Jet+NJets', 'Rec_1Ele_6Jet', 'Rec_1bJet', 'Rec_1Ele_1GammaEB_2Jet', 'Rec_1Muon_1GammaEB_1Jet_1MET', 'Rec_2Muon_2bJet_1MET+X', 'Rec_1Muon_1GammaEB_2Jet_1MET+NJets', 'Rec_2Muon_2bJet_1MET+NJets', 'Rec_1Ele_1Muon_2bJet_1Jet+X', 'Rec_1GammaEB_4Jet_1MET+NJets', 'Rec_1GammaEB_6Jet', 'Rec_1Ele_2bJet', 'Rec_1Muon_2bJet_3Jet_1MET', 'Rec_1Muon_1GammaEB_3Jet', 'Rec_1Ele_2Muon+NJets', 'Rec_3bJet+X', 'Rec_2Muon_2bJet_1Jet', 'Rec_2Ele_2bJet+NJets', 'Rec_2Muon_5Jet+NJets', 'Rec_1Ele_1Muon_3Jet_1MET', 'Rec_1Muon_2bJet_4Jet+NJets', 'Rec_2Muon_1bJet_3Jet', 'Rec_1Ele_2bJet_2Jet_1MET+X', 'Rec_2Jet_1MET', 'Rec_1Muon_1GammaEB_1bJet_1Jet+NJets', 'Rec_2Ele_1GammaEB+X', 'Rec_1GammaEB_1bJet_1Jet_1MET+X', 'Rec_2GammaEB_1Jet', 'Rec_1GammaEB_2bJet+X', 'Rec_2Ele_1GammaEB+NJets', 'Rec_1bJet_2Jet', 'Rec_1Ele_1Muon_1bJet_2Jet_1MET', 'Rec_2Muon_4Jet_1MET+X', 'Rec_2Ele_3Jet_1MET+X', 'Rec_2Muon_5Jet', 'Rec_1GammaEB_1bJet_4Jet+X', 'Rec_1Ele_1bJet_4Jet_1MET', 'Rec_1Muon_3bJet+X', 'Rec_1Ele_1GammaEB_1MET+X', 'Rec_3Jet_1MET+NJets', 'Rec_3Muon', 'Rec_1Ele_2bJet_2Jet_1MET+NJets']

i = 0     
sf = [1.50882088e-04, 8.56680905e-05, 1.94961280e-06, 1.60187857e-04,
       4.40334389e-08, 0.00000000e+00, 0.00000000e+00, 9.79716779e-05,
       2.72468363e-06, 1.04752105e-06, 1.00865101e-06, 1.64193835e-04,
       7.93587991e-04, 1.13288243e-04, 1.98163657e-06, 2.02258594e-08,
       1.20662712e-06, 6.38521231e-04, 0.00000000e+00, 1.11843223e-06,
       6.19230187e-06, 0.00000000e+00, 4.90547076e-06, 0.00000000e+00,
       5.10208300e-03, 3.03605748e-03, 0.00000000e+00, 1.39917002e-04,
       5.13354069e-05, 2.49561357e-03, 3.56117031e-03, 2.77576900e-05,
       5.12130417e-06, 1.51952448e-03, 1.98931134e-04, 9.44144951e-05,
       4.57864979e-04, 1.77280695e-03, 7.87424707e-05, 3.89986604e-05,
       0.00000000e+00, 0.00000000e+00, 2.61798758e-07, 1.99326030e-05,
       4.55692165e-06, 1.34044595e-03, 1.50652913e-06, 8.32100976e-04,
       2.42430940e-03, 0.00000000e+00, 4.00672664e-06, 3.58053953e-05,
       1.29328138e-06, 0.00000000e+00, 9.96652153e-04, 2.84323889e-05,
       0.00000000e+00, 5.89889152e-06, 1.65210486e-05, 0.00000000e+00,
       1.15165195e-04, 1.62933052e-07, 0.00000000e+00, 0.00000000e+00,
       7.35842981e-07, 1.22416630e-03, 9.61037863e-03, 3.72339338e-04,
       0.00000000e+00, 2.10408565e-07, 0.00000000e+00, 2.07591292e-06,
       0.00000000e+00, 8.27465629e-04, 1.81924440e-02, 9.11147241e-05,
       3.38602946e-04, 5.98042049e-06, 4.75072128e-04, 1.91808186e-04,
       8.78696739e-03, 1.83283458e-04, 2.44727612e-02, 2.13826360e-04,
       0.00000000e+00, 1.63205593e-05, 5.77896563e-04, 7.97002545e-06,
       1.09178371e-04, 4.00708871e-06, 2.32068097e-04, 3.82730891e-05,
       1.16341647e-02, 2.29491238e-06, 0.00000000e+00, 1.99486799e-05,
       2.51728030e-05, 1.46675782e-04, 1.26566796e-05, 0.00000000e+00,
       0.00000000e+00, 3.85463219e-05, 1.31566784e-04, 6.05091347e-06,
       6.33672042e-04, 2.92563966e-06, 4.26573415e-03, 0.00000000e+00,
       1.30222183e-04, 0.00000000e+00, 3.49130743e-06, 0.00000000e+00,
       0.00000000e+00, 1.09754265e-05, 6.58168840e-05, 0.00000000e+00,
       0.00000000e+00, 7.55493022e-05, 0.00000000e+00, 8.97588669e-04,
       5.60564649e-03, 5.41876890e-04, 2.68054739e-05, 2.58281171e-04,
       0.00000000e+00, 3.02800514e-03, 9.04323002e-05, 0.00000000e+00,
       0.00000000e+00, 1.15868176e-03, 0.00000000e+00, 8.45440511e-05,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.92466721e-02,
       1.46758351e-05, 1.14414219e-03, 3.53339745e-04, 4.28945210e-04,
       0.00000000e+00, 1.03453246e-05, 0.00000000e+00, 5.76202352e-05,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.90762134e-04,
       4.45466002e-04, 2.02713947e-07, 0.00000000e+00, 7.39195094e-03,
       1.33948726e-05, 2.40670800e-03, 4.29649438e-04, 4.52180113e-05,
       6.30270353e-05, 0.00000000e+00, 1.37092186e-04, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 1.15855503e-04, 6.43878601e-04,
       0.00000000e+00, 7.22356994e-02, 8.69139745e-06, 0.00000000e+00,
       9.99275717e-04, 2.56859828e-07, 0.00000000e+00, 1.27417024e-04,
       5.14468734e-04, 4.84757874e-05, 0.00000000e+00, 3.13772460e-03,
       0.00000000e+00, 0.00000000e+00, 1.97371351e-05, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 5.62544396e-05,
       0.00000000e+00, 6.70547492e-04, 1.70424030e-04, 0.00000000e+00,
       0.00000000e+00, 9.40658637e-05, 0.00000000e+00, 0.00000000e+00,
       6.72719698e-04, 3.60504076e-05, 0.00000000e+00, 1.06137423e-04,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 3.85204901e-03, 2.51564700e-04, 3.29553812e-05,
       0.00000000e+00, 1.01586700e-04, 1.00797804e-03, 7.94922273e-05,
       1.70939483e-03, 9.82781976e-05, 8.33766726e-05, 0.00000000e+00,
       0.00000000e+00, 9.91308399e-05, 3.32665184e-05, 1.36782699e-04,
       5.36342643e-05, 2.36573659e-04, 0.00000000e+00, 3.96140462e-05,
       1.00655604e-03, 0.00000000e+00, 0.00000000e+00, 3.31002132e-04,
       1.93975539e-04, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 1.30449925e-03, 0.00000000e+00,
       4.08071057e-04, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 1.25825045e-04, 6.89188377e-07, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 2.52247691e-04,
       4.22363230e-04, 0.00000000e+00, 0.00000000e+00, 7.63134779e-05,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       4.42310680e-04, 7.96254163e-05, 5.43398006e-03, 0.00000000e+00,
       0.00000000e+00, 8.59492286e-07, 1.70045679e-03, 0.00000000e+00,
       3.01304412e-05, 0.00000000e+00, 5.73707723e-04, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 6.15592008e-05, 0.00000000e+00,
       0.00000000e+00, 9.83682465e-07, 0.00000000e+00, 2.37802196e-04,
       0.00000000e+00, 2.37635675e-04, 3.52171610e-05, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       2.86003428e-03, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 4.03701039e-05, 0.00000000e+00,
       2.13664447e-03, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       1.23841921e-04, 0.00000000e+00, 0.00000000e+00, 2.46778173e-04,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       3.26463820e-04, 1.38187867e-06, 0.00000000e+00, 0.00000000e+00,
       4.69124930e-05, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 7.07882720e-04, 0.00000000e+00, 0.00000000e+00,
       8.74023382e-04, 1.24274718e-02, 1.61042841e-04, 2.17477778e-03,
       0.00000000e+00, 5.67357996e-05, 2.88824550e-04, 2.10750390e-03,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.16473763e-03,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.48536852e-02,
       5.42022595e-04, 0.00000000e+00, 5.47475496e-03, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 4.18392878e-04, 4.94431266e-04,
       2.16546383e-04, 0.00000000e+00, 1.49444451e-04, 1.63376580e-04,
       7.46605256e-05, 0.00000000e+00, 0.00000000e+00, 2.28016023e-04,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       6.31018812e-04, 1.81576024e-03, 2.11828471e-04, 1.76795570e-04,
       0.00000000e+00, 4.27739370e-04, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 6.34604709e-03, 5.27842780e-04, 2.55277223e-04,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 1.06557485e-03, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 6.63849587e-04,
       9.83895575e-05, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 2.96102645e-04, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 3.03316858e-04, 5.05398700e-04, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.11266440e-04,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 7.01117395e-04, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 2.63415909e-04, 1.21952845e-04,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 6.70273480e-03,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       3.86979553e-04, 6.35675488e-04, 0.00000000e+00, 6.90879200e-04,
       0.00000000e+00, 2.30550788e-03, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 2.07721758e-03, 4.26660332e-04,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.34088280e-04,
       0.00000000e+00, 1.51964429e-04, 0.00000000e+00, 8.57024789e-05,
       1.26089731e-03, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 9.78227312e-03, 0.00000000e+00,
       2.86097603e-03, 0.00000000e+00, 0.00000000e+00, 3.49060031e-04,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       1.90381063e-04, 9.40229182e-04, 0.00000000e+00, 0.00000000e+00,
       1.19857181e-03, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       4.34623998e-02, 0.00000000e+00, 0.00000000e+00, 2.38714209e-04]
#norm = plt.Normalize(np.min(np.array(sf)), np.max(np.array(sf)))
normalized_values = sf
P_music = {}
JS = {}
distributions = ["InvMass", "SumPt","MET"]

cmap = 'brg'

plt.figure()
p_js = []
p = []

#from NEW_EVENTS import  event_classes
#from NEW_EVENTS import  SF_InvMass
#from NEW_EVENTS import  SF_SumPt
#from NEW_EVENTS import  SF_MET
#from event_classes import event_classes
from event_classes import event_classes

mc_names = list(event_classes.keys())

#mc_names = ["Rec_1Ele_1MET"]
for ec_name in mc_names:
    for dist in distributions:
        color_dist ="black"
        path_signal = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_signal/{ec_name}_{dist}_output.csv"
        path_bkg = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_bkg/{ec_name}_{dist}_output.csv"

        
        if os.path.isfile(path_signal) and os.path.isfile(path_bkg):
            p_signal = np.median(np.array(read_outputs(path_signal)))
            p_signal_js = np.median(np.array(read_outputs_js(path_signal)))
            p_toys = np.array(read_outputs(path_bkg))
            p_toys_js = np.array(read_outputs_js(path_bkg))


            result = max(
                1.0 / float(len(p_toys)),
                np.sum(p_toys <= p_signal) / float(len(p_toys)),
            )
            p.append(result)
            result_js = max(
                1.0 / float(len(p_toys_js)),
                np.sum(np.array(p_toys_js) >= p_signal_js) / float(len(p_toys_js)),
            )
            p_js.append(result_js)

            if(result_js < 0.1):
                if(result > 0.2):
                    #print("----     " + dist + "    ----")
                    #print(str(ec_name) + "\t MUSIC / JSD:\t" + str(result) +  " / " + str(result_js))
                    print("----" + dist + "----")
                    print("\""+ec_name + "\"" +",")
                    print("MUSiC / JSD: " + str(result) +" , "  + str(result_js))
            if(dist == "InvMass"):color_dist = "blue"
            if(dist == "SumPt"): color_dist = "red"
            if(dist == "MET"): color_dist = "green"

            plt.scatter(result,result_js,alpha = 0.5,color = color_dist, edgecolor = "black")


plt.xlabel("Music p~")
plt.ylabel("NOISE P")

plt.xscale("log")
plt.yscale("log")
#plt.colorbar()


plt.grid()
plt.plot([0.001,1],[0.001,1],color="black")
plt.savefig(dist + "_" + ec_name + "Music_JS_comparison.jpg")
