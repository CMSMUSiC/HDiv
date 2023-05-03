from condor_scheduler import CondorScheduler

import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep
import json
import numpy as np
import os
import shutil
from scipy.special import erf
import math




location = "./test_outputs/Binningtest"
#CondorScheduler.harvest(location)

f = open(location + "/job_id_to_args.json")
data = json.load(f)
results = []
music_results = {}
js_results = {}

exp_mean = 10
signal_mean = 35
signal_std = 10  

# Directory
directory = "exp-" + str(exp_mean) + ", sig_mean-" + str(signal_mean) + ", sig_std- " + str(signal_std)
  
# Parent Directory pathw
parent_dir = "./Results/Binningtest"
  
# Path
path = os.path.join(parent_dir, directory)
  
#shutil.rmtree(path)


os.mkdir(path)

signal_fractions = []
sample_size = []
Binsize = []
for id, info in data.items():
             if(info["results"] != "NaN"):
                 if(int(info["args"][1]) not in sample_size):
                         sample_size.append(int(info["args"][1]))
                 if(float(info["args"][2]) not in signal_fractions):
                         signal_fractions.append(float(info["args"][2]))    
                 if(float(info["args"][4]) not in Binsize):
                         Binsize.append(float(info["args"][4]))            
if(len(signal_fractions) > 1):
     raise NameError("More than one signalfractions for binningtests")
print(Binsize)
sf = signal_fractions[0]
for bins in Binsize:
    print("---- " + str(bins) + " ----")
    music_results[bins] = {}
    js_results[bins] = {}
    for ss in sample_size:
        music_results[bins][ss] = {}
        js_results[bins][ss] = {}

        music_results[bins][ss]["Binsize"] = []
        music_results[bins][ss]["mean"] = []
        music_results[bins][ss]["std"] = []


        js_results[bins][ss]["Binsize"] = []
        js_results[bins][ss]["mean"] = []
        js_results[bins][ss]["std"] = []

        js_p = []
        music_p = []

        print("---- " + str(ss) + " ----")

        for id, info in data.items():
            if(info["results"] != "NaN"):
                if(int(info["args"][1]) == ss):
                    if(float(info["args"][4]) == bins):
                        results.append(eval(info["results"])) 
                        js_p.append(eval(info["results"])[1])
                        music_p.append(eval(info["results"])[0])

        print("ss = " , ss)

        if(len(music_p)>0):                
            music_results[bins][ss]["Binsize"] = (bins)
            music_results[bins][ss]["mean"] = (np.mean(music_p))
            music_results[bins][ss]["std"] = np.std(music_p,ddof=1)
            print("MusiC : ", music_results[bins][ss]["mean"])    

        if(len(js_p)>0):                                          
            js_results[bins][ss]["Binsize"] = (bins)
            js_results[bins][ss]["mean"] = (np.mean(js_p))
            js_results[bins][ss]["std"] = (np.std(js_p,ddof=1))
            print("JS : ", js_results[bins][ss]["mean"])
print("Begin Plotting")                                 
f.close()

i= 0
# color_js = ["purple","navy","red"]
# color_music = ["magenta","blue","orangered"]

for ss in sample_size:
    fig = plt.figure()
    ax = plt.axes()
    sf = signal_fractions[0]
    js_mean = []
    js_std = []
    js_ss = []
    music_mean = []
    music_std = []
    music_ss = []
    for bins in Binsize:

        js_mean.append(js_results[bins][ss]["mean"])
        js_std.append(js_results[bins][ss]["std"])
        js_ss.append(js_results[bins][ss]["Binsize"])

        music_mean.append(music_results[bins][ss]["mean"])
        music_std.append(music_results[bins][ss]["std"])
        music_ss.append(music_results[bins][ss]["Binsize"])   
          
    ax.errorbar(
        js_ss,
        js_mean,
        yerr=js_std,
        fmt="o:",
        capsize = 5,
        label=f"JS - Sample size: {int(ss)}",
#        color = color_js[i]
        )

    ax.errorbar(
        music_ss,
        music_mean,
        yerr=music_std,
        fmt="s-",
        capsize = 8,
        label=f"MUSiC - Sample size: {int(ss)}",
#        color = color_music[i]
    )
    ax.grid()
    ax.set_title(r"$\mu$ = " + str(signal_mean) + r", $\sigma$ = " + str(signal_std) + ", Signal Fraction = " + str(sf))
        
    ax.set_xlabel("Number of Bins")
    ax.set_ylabel("Mean p-value")
    fig.tight_layout()
    ax.set_yscale("log")

    p = 0.5 * (1-erf([1,2,3]/np.sqrt(2)))
    xmin = min([abs(x) for x in ax.get_xlim()])
    xmax = max([abs(x) for x in ax.get_xlim()])
    ax.set_xlim(xmin,xmax)
    ax.hlines(p[0],xmin,xmax, ls = "--", color="lightgreen",label=fr"1 $\sigma$")
    ax.hlines(p[1],xmin,xmax, ls = "--", color="green",label=fr"2 $\sigma$")
    ax.hlines(p[2],xmin,xmax, ls = "--", color="darkgreen",label=fr"3 $\sigma$")
    ax.set_yscale("log")
    ax.legend()
    plt.savefig(path +"sf-"+ str(sf)+"ss-"+ str(ss) +".jpg",dpi=1000)
    i = i+1
    if(i == 3): break



