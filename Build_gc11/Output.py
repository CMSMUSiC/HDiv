from condor_scheduler import CondorScheduler

import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep
import json
import numpy as np
import os
import shutil
from uncertainties import ufloat
from scipy.special import erf
import math




location = "./test_outputs/outputs_2023_05_08_18_28_09"
print("Begin harvesting")
CondorScheduler.harvest(location)

f = open(location + "/job_id_to_args.json")
data = json.load(f)
results = []
music_results = {}
js_results = {}



exp_mean = 10
signal_mean = 53
signal_std = 1    




# Directory
directory = "Nexp-" + str(exp_mean) + ", sig_mean-" + str(signal_mean) + ", sig_std- " + str(signal_std)
  
# Parent Directory pathw
parent_dir = "./Results/1D_JS"
  
# Path
path = os.path.join(parent_dir, directory)
  
#shutil.rmtree(path)


os.mkdir(path)

signal_fractions = []
sample_size = []
for id, info in data.items():
             if(info["results"] != "NaN"):
                 if(int(info["args"][1]) not in sample_size):
                         sample_size.append(int(info["args"][1]))
                 if(float(info["args"][2]) not in signal_fractions):
                         signal_fractions.append(float(info["args"][2]))     

print("prescan")
print("ss",sample_size)
print("sf",signal_fractions)
for sf in signal_fractions:
    print("---- " + str(sf) + " ----")
    music_results[sf] = {}
    js_results[sf] = {}
    for ss in sample_size:
        music_results[sf][ss] = {}
        js_results[sf][ss] = {}

        music_results[sf][ss]["sample_size"] = []
        music_results[sf][ss]["mean"] = []
        music_results[sf][ss]["std"] = []


        js_results[sf][ss]["sample_size"] = []
        js_results[sf][ss]["mean"] = []
        js_results[sf][ss]["std"] = []

        js_p = []
        music_p = []

        print("---- " + str(ss) + " ----")

        for id, info in data.items():
            if(info["results"] != "NaN"):
                # print("Task:", id)
                # print("ss: ", info["args"][1])
                # print("sf: ", info["args"][2])
                # print("Test 1")
                # print(ss)
                # print(info["args"][1])
                if(int(info["args"][1]) == ss):
                    # print("Test 2")
                    # print(sf)
                    # print(info["args"][2])
                    if(float(info["args"][2]) == sf):
                        results.append(eval(info["results"])) 
                        js_p.append(eval(info["results"])[1])
                        music_p.append(eval(info["results"])[0])
                        # print('results: ', info["results"])

        print("ss = " , ss)

        if(len(music_p)>0):                
            music_results[sf][ss]["sample_size"] = (ss)
            music_results[sf][ss]["mean"] = (np.mean(music_p))
            music_results[sf][ss]["std"] = np.std(music_p,ddof=1)
            print("MusiC : ", music_results[sf][ss]["mean"])    

        if(len(js_p)>0):                                          
            js_results[sf][ss]["sample_size"] = (ss)
            js_results[sf][ss]["mean"] = (np.mean(js_p))
            js_results[sf][ss]["std"] = (np.std(js_p,ddof=1))
            print("JS : ", js_results[sf][ss]["mean"])
# for id, info in data.items():
#                  print("Task:", id)
#                  print("ss: ", info["args"][1])
#                  print("sf: ", info["args"][2])
#                  results.append(eval(info["results"])) 
#                  print('results: ', info["results"])  

#                  results.append(eval(info["results"])) 
#                  js_p.append(eval(info["results"])[1])
#                  music_p.append(eval(info["results"])[0])
                                  
f.close()
for sf in signal_fractions:
    fig, ax = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [5, 2]})
#    fig = plt.figure()
#    ax = plt.axes()
    js_mean = []
    js_std = []
    js_ss = []
    music_mean = []
    music_std = []
    music_ss = []
    for ss in sample_size:

        js_mean.append(js_results[sf][ss]["mean"])
        js_std.append(js_results[sf][ss]["std"])
        js_ss.append(js_results[sf][ss]["sample_size"])

        music_mean.append(music_results[sf][ss]["mean"])
        music_std.append(music_results[sf][ss]["std"])
        music_ss.append(music_results[sf][ss]["sample_size"])   
          
    ax[0].errorbar(
        js_ss,
        js_mean,
        yerr=js_std,
        fmt="o:",
        capsize = 5,
        label=f"JS",
        )

    ax[0].errorbar(
        music_ss,
        music_mean,
        yerr=music_std,
        fmt="s-",
        capsize = 8,
        label=f"MUSiC",
    )
    difference = []
    difference_std = []
    for i in range(len(js_mean)):
        difference.append( ((ufloat(js_mean[i],js_std[i]) - ufloat(music_mean[i],music_std[i]))/ufloat(music_mean[i],music_std[i])).n)
        difference_std.append( ((ufloat(js_mean[i],js_std[i]) - ufloat(music_mean[i],music_std[i]))/ufloat(music_mean[i],music_std[i])).s)
    ax[1].errorbar(
        music_ss,
        difference,
        yerr=difference_std,
        fmt='.', 
        marker='o',
        capsize = 4,
        markersize = 4,
        color = "red"
    )
    ax[0].grid()
    ax[1].grid()

    ax[0].set_title(r"$\mu$ = " + str(signal_mean) + r", $\sigma$ = " + str(signal_std) + ", Signal Fraction = " + str(sf))
    
    ax[1].set_xlabel("Sample size")
    ax[0].set_ylabel("Mean p-value")
    ax[1].set_ylabel("$(P_{js} - P_{music})/ P_{music}$")
    fig.tight_layout()
    ax[1].set_xscale("log")
    ax[0].set_yscale("log")
    #ax[1].set_yscale("symlog")

    ax[1].axhline(y=0., color='black', linestyle='--')
    ymax = max([abs(x) for x in ax[1].get_ylim()])
    ax[1].set_ylim(-ymax, ymax)
    p = 0.5 * (1-erf([1,2,3]/np.sqrt(2)))
    xmin = min([abs(x) for x in ax[0].get_xlim()])
    xmax = max([abs(x) for x in ax[1].get_xlim()])
    ax[0].set_xlim(xmin,xmax)
    ax[0].hlines(p[0],xmin,xmax, ls = "--", color="lightgreen",label=fr"1 $\sigma$")
    ax[0].hlines(p[1],xmin,xmax, ls = "--", color="green",label=fr"2 $\sigma$")
    ax[0].hlines(p[2],xmin,xmax, ls = "--", color="darkgreen",label=fr"3 $\sigma$")
    ax[0].set_yscale("log")
    ax[0].legend()
    plt.savefig(path +"/sf-"+ str(sf) +".jpg",dpi=1000)

