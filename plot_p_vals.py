#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import csv
import numpy as np
import ROOT
from math import log10
from tqdm import tqdm
import matplotlib.patches as patches
from scipy.special import erf
import matplotlib

import mplhep as hep
hep.style.use(hep.style.ROOT)
# mpl.use("Agg")

#from event_classes import event_classes
from puplication_eventclasses import  event_classes
from puplication_eventclasses import  SF_InvMass
from puplication_eventclasses import  SF_SumPt
from puplication_eventclasses import  SF_MET

linestyle_tuple = [
     ('loosely dotted',        (0, (1, 10))),
     ('dotted',                (0, (1, 1))),
     ('densely dotted',        (0, (1, 1))),
     ('long dash with offset', (5, (10, 3))),
     ('loosely dashed',        (0, (5, 10))),
     ('dashed',                (0, (5, 5))),
     ('densely dashed',        (0, (5, 1))),

     ('loosely dashdotted',    (0, (3, 10, 1, 10))),
     ('dashdotted',            (0, (3, 5, 1, 5))),
     ('densely dashdotted',    (0, (3, 1, 1, 1))),

     ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),
     ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),
     ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))]

def read_outputs(file_path):
    scores = []
    with open(file_path, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            #if( isinstance(row["score"], float) or isinstance(row["score"], int) ):  
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
            #if( isinstance(row["js_distance"], float) or isinstance(row["js_distance"], int) ):  
            scores.append(float(row["js_distance"]))
    return scores

import re

def find_numbers_before_string(larger_string, specific_string):
    pattern = r"(\d+)\s*" + re.escape(specific_string)
    match = re.search(pattern, larger_string)

    if match:
        numbers = int(match.group(1))
        return numbers
    else:
        return 0

def Boxplot(Eventclass,distribution="InvMass",Method="music"):
    results = []
    results_JS = []
    X_ticks = []
    for ec_name in Eventclass:
        dist = distribution
        path_signal = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_signal/{ec_name}_{dist}_output.csv"
        path_bkg = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_bkg/{ec_name}_{dist}_output.csv"
        if os.path.isfile(path_signal) and os.path.isfile(path_bkg):
            
            if(True):
                p_signal = np.array(read_outputs(path_signal))
                p_toys = np.array(read_outputs(path_bkg))

                p_vals = []
                for signal in p_signal:
                        p_vals.append( max(
                            1.0 / float(len(p_toys)),
                        np.sum(p_toys <= signal) / float(len(p_toys)),
                        ))
                results.append(p_vals)
                #X_ticks.append("$"+ec_name[4:].replace("_","+").replace("Muon","\mu").replace("Ele","e")+"$")
            if(True):
                p_signal = np.array(read_outputs_js(path_signal))
                p_toys = np.array(read_outputs_js(path_bkg))

                p_vals = []
                for signal in p_signal:
                        p_vals.append( max(
                            1.0 / float(len(p_toys)),
                        np.sum(p_toys >= signal) / float(len(p_toys)),
                        ))
                results_JS.append(p_vals)
                X_ticks.append("$"+ec_name[4:].replace("_","+").replace("Muon","\mu").replace("Ele","e")+"$")

    
    
    fig = plt.figure(figsize=(16, 10))     
    plt.yscale("log")
    offset = 0.4
    positions = np.arange(1, (len(results_JS))*2,2) - offset
    plt.boxplot(results, positions=positions)
    positions = np.arange(1, (len(results_JS))*2,2) + offset
    plt.boxplot(results_JS, positions= positions)
    plt.xticks(np.arange(1, (len(results_JS) )*2,2),X_ticks,rotation=90,fontsize=8)



def Boxplot_New(Eventclass,distribution="InvMass"):
    results = []
    results_JS = []
    X_ticks = []
    for ec_name in Eventclass:
        dist = distribution
        path_signal = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_signal/{ec_name}_{dist}_output.csv"
        path_bkg = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_bkg/{ec_name}_{dist}_output.csv"
        if os.path.isfile(path_signal) and os.path.isfile(path_bkg):
            
            p_signal = np.array(read_outputs(path_signal))
            p_toys = np.array(read_outputs(path_bkg))
            p_vals = []
            for signal in p_signal:
                    p_vals.append( max(
                        1.0 / float(len(p_toys)),
                    np.sum(p_toys <= signal) / float(len(p_toys)),
                    ))
            results.append(p_vals)

            p_signal_JS = np.array(read_outputs_js(path_signal))
            p_toys_JS = np.array(read_outputs_js(path_bkg))
            p_vals_JS = []
            for signal in p_signal_JS:
                    p_vals_JS.append( max(
                        1.0 / float(len(p_toys_JS)),
                    np.sum(p_toys_JS >= signal) / float(len(p_toys_JS)),
                    ))
            results_JS.append(p_vals_JS)
            X_ticks.append("$"+ec_name[4:].replace("_","+").replace("Muon","\mu").replace("Ele","e")+"$")

    

    MUSiC_Median = []
    MUSiC_err_1sig = []
    MUSiC_err_2sig = []

    JS_Median = []
    JS_err_1sig = []
    JS_err_2sig = []

    for i in range(len(results)):
        MUSiC_Median.append(np.median(results[i]))
        MUSiC_err_1sig.append(np.percentile(results[i],68) - np.median(results[i]))
        MUSiC_err_2sig.append(np.percentile(results[i],95.4) - np.median(results[i]))

        JS_Median.append(np.median(results_JS[i]))
        JS_err_1sig.append(np.percentile(results_JS[i],68) - np.median(results_JS[i]))
        JS_err_2sig.append(np.percentile(results_JS[i],95.4) - np.median(results_JS[i]))





    fig = plt.figure(figsize=(16, 12))     
    plt.yscale("log")


    offset = 0.15
    binwitdh = 0.6
    for i in range(len(results_JS)):
        rect = patches.Rectangle((np.arange(1, (len(results_JS) )*2,2)[i] -offset - binwitdh  + binwitdh/4, MUSiC_Median[i] - MUSiC_err_2sig[i]), binwitdh*.5,  MUSiC_err_2sig[i] - MUSiC_err_1sig[i], linewidth=1, edgecolor='cyan', facecolor='cyan', alpha=0.8,label = r"SM expectation ± 2 $\sigma$")
        plt.gca().add_patch(rect)
        rect = patches.Rectangle((np.arange(1, (len(results_JS) )*2,2)[i] -offset - binwitdh  + binwitdh/4, MUSiC_Median[i] + MUSiC_err_1sig[i]), binwitdh*.5,  MUSiC_err_2sig[i] - MUSiC_err_1sig[i], linewidth=1, edgecolor='cyan', facecolor='cyan', alpha=0.8,label = r"SM expectation ± 2 $\sigma$")
        plt.gca().add_patch(rect)
        rect = patches.Rectangle((np.arange(1, (len(results_JS) )*2,2)[i] -offset - binwitdh , MUSiC_Median[i] - MUSiC_err_1sig[i]), binwitdh, 2 * MUSiC_err_1sig[i], linewidth=1, edgecolor='Blue', facecolor='Blue', alpha=0.3,label = r"SM expectation ± 1 $\sigma$")
        plt.gca().add_patch(rect)     


    plt.errorbar(np.arange(1, (len(results_JS) )*2,2) -offset - binwitdh +binwitdh/2 , MUSiC_Median,xerr = binwitdh/2+0.05, fmt='+', markersize=0,linewidth = 1, capsize=0, color='orange')

    for i in range(len(results_JS)):
        rect = patches.Rectangle((np.arange(1, (len(results_JS) )*2,2)[i] + offset + binwitdh/4, JS_Median[i] - JS_err_2sig[i]), binwitdh*.5, (JS_err_2sig[i] - JS_err_1sig[i])  , linewidth=1, edgecolor='springgreen', facecolor='springgreen', alpha=0.8,label = r"SM expectation ± 2 $\sigma$")
        plt.gca().add_patch(rect)
        rect = patches.Rectangle((np.arange(1, (len(results_JS) )*2,2)[i] + offset  + binwitdh/4, JS_Median[i] + JS_err_1sig[i]), binwitdh*.5,(JS_err_2sig[i] - JS_err_1sig[i]) , linewidth=1, edgecolor='springgreen', facecolor='springgreen', alpha=0.8,label = r"SM expectation ± 2 $\sigma$")
        plt.gca().add_patch(rect)
        rect = patches.Rectangle((np.arange(1, (len(results_JS) )*2,2)[i] + offset , JS_Median[i] - JS_err_1sig[i]), binwitdh, 2 * JS_err_1sig[i], linewidth=1, edgecolor='green', facecolor='green', alpha=0.4,label = r"SM expectation ± 1 $\sigma$")
        plt.gca().add_patch(rect)

    plt.errorbar(np.arange(1, (len(results_JS))*2,2) + offset+binwitdh/2, JS_Median,xerr = binwitdh/2+0.1, fmt='+', markersize=0,linewidth = 1, capsize=0, color='purple')



    plt.yscale("log")
    plt.xlim(-0.09,np.max((np.arange(1, (len(results_JS) )*2,2)))+1 )
    plt.ylim(1/2200,1.09)
    plt.title("Music - " + str(dist))
    plt.ylabel("Number of Eventclasses")

    #plt.legend(loc='upper center', bbox_to_anchor=(0.65, 1))
    plt.xticks(np.arange(1, (len(results_JS) )*2,2),X_ticks,rotation=90,fontsize=8)
    plt.tight_layout()
    plt.savefig("Boxplot-" + distribution +".jpg",dpi=1000)  
    plt.show()  	






def lep_jet_heatmap(Eventclass,distribution="InvMass",Method="music"):
    Pvals = {}
    for i in range(7):
        for j in range(7):
            Pvals[str(i)+"Lep/"+str(j)+"Jet"] = []
    for ec_name in Eventclass:
        dist = distribution
        path_signal = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_signal/{ec_name}_{dist}_output.csv"
        path_bkg = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_bkg/{ec_name}_{dist}_output.csv"
        if os.path.isfile(path_signal) and os.path.isfile(path_bkg):
            p_signal = np.array(read_outputs(path_signal))
            p_signal_js = np.array(read_outputs_js(path_signal))
            p_toys = np.array(read_outputs(path_bkg))
            p_toys_js = np.array(read_outputs_js(path_bkg))


            p_vals = []
            for signal in p_signal:
                    p_vals.append( max(
                        1.0 / float(len(p_toys)),
                    np.sum(p_toys <= signal) / float(len(p_toys)),
                    ))
            lep = find_numbers_before_string(ec_name, "Ele")  + find_numbers_before_string(ec_name, "Muon")       
            jet = find_numbers_before_string(ec_name, "Jet")  + find_numbers_before_string(ec_name, "bJet")   
            Pvals[str(lep) + "Lep/"+ str(jet)+"Jet"].append(np.median(p_vals))    

    P_Matrix = np.ones((7,7))  
    for i in range(7):
        for j in range(7):
            P_Matrix[j,i]= np.median(Pvals[str(i) + "Lep/"+ str(j)+"Jet"])

    fig = plt.figure(figsize=(7, 7))
    x = np.arange(8)
    y = np.arange(8)
    plt.xticks(range(1,7))

    # Create the plot
    plt.pcolor(x, y, P_Matrix, cmap='viridis')
    #plt.imshow(P_Matrix, origin='lower', cmap = "Blues",norm=matplotlib.colors.LogNorm())
    plt.colorbar(mappable=None, cax=None, ax=None)
    plt.xlabel("#Leptonen",fontsize = 16)
    plt.ylabel("#Jets",fontsize = 16)
    plt.savefig("Test_Heatmap.jpg",dpi=1000)
    plt.show()




sig_fractions = []
P_music = {}
JS = {}
distributions = ["InvMass", "SumPt","MET"]


p_js = []
p = []
idx = 0
max_p = -log10(1 / 10000)
binwitdh = max_p / 9
bins = []
for i in range(10):
    bins.append(i*binwitdh)
#event_classes = list(event_classes.keys())
#event_classes = ["Rec_2Muon_1Jet+X"]
for dist in distributions:
    d = 0
    EVENTS = {}
    print("-> Calculating P for: " + str(dist))
    for ec_name in tqdm(event_classes):
        path_signal = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_signal/{ec_name}_{dist}_output.csv"
        path_bkg = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_bkg/{ec_name}_{dist}_output.csv"
        if os.path.isfile(path_signal) and os.path.isfile(path_bkg):

            p_signal = np.array(read_outputs(path_signal))
            p_signal_js = np.array(read_outputs_js(path_signal))
            p_toys = np.array(read_outputs(path_bkg))
            p_toys_js = np.array(read_outputs_js(path_bkg))
            results = []

            for signal in p_signal:
                results.append( max(
                    1.0 / float(len(p_toys)),
                np.sum(p_toys <= signal) / float(len(p_toys)),
                ))
            result = np.median(results)  
            p.append(result)
           
            results_js = []
            
            for signal in p_signal_js:
                results_js.append( max(
                    1.0 / float(len(p_toys_js)),
                np.sum(p_toys_js >= signal) / float(len(p_toys_js)),
                ))
            result_js = np.median(results_js)  
            p_js.append(result_js)
            EVENTS[ec_name] = result_js

            if(dist == "InvMass"):
                sig_fractions.append(SF_InvMass[d])
            if(dist == "SumPt"):
                sig_fractions.append(SF_SumPt[d])
            if(dist == "MET"):
                sig_fractions.append(SF_MET[d])                                
            d = d + 1    
                #sig_fractions.append(event_classes[ec_name]*100)


    EVENTS = np.array(sorted(EVENTS.items(), key=lambda x:x[1],reverse = False))[:,0]
    Boxplot_New(EVENTS[0:30],distribution=dist)

            # p_dist.append(-log10(result))    
            # p_js_dist.append(-log10(result_js))    
            # pt_toys_res.append(-log10(np.median(pt_toys)))
            # pt_toys_js_res.append(-log10(np.median(pt_toys_js)))


            # add signal fraction


# plt.xscale("log")
# 

# plt.ylim(0,0.7)
fig = plt.figure(figsize=(12, 12)) 

gs = fig.add_gridspec(3, 2,  width_ratios=(4, 1), height_ratios=(1, 4, 0.3),
                      left=0.1, right=0.9, bottom=0.1, top=0.9,
                      wspace=0.05, hspace=0.3)

ax = fig.add_subplot(gs[1, 0])
ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)



# no labels
ax_histx.tick_params(axis="x", labelbottom=False)
ax_histy.tick_params(axis="y", labelleft=False)

# the scatter plot:
# cmap = mpl.cm.cool
# cmap='Blues'
# sct_plot = ax.scatter(p,p_js,alpha = 0.4, s=100, c=sig_fractions, cmap=cmap, edgecolor = None)
sct_plot = ax.scatter(p,p_js,alpha = 0.3, s=100, c=sig_fractions, edgecolor = None)

ax_histx.hist(p, bins=30, color = "tab:cyan")
ax_histy.hist(p_js, bins=30, orientation='horizontal', color = "tab:cyan")
ax_histx.set_yscale('log')
ax_histy.set_xscale('log')

norm = mpl.colors.Normalize(vmin=5, vmax=10)
color_ax = fig.add_subplot(gs[2, 0])
fig.colorbar(sct_plot, cax=color_ax, orientation='horizontal', label='Signal Fraction [%]')

ax.set_xlabel("MUSiC $\widetilde{p}$")
ax.set_ylabel("Fast $p$-value")



ax.grid()
ax.plot([0.001,1],[0.001,1],color="black")
os.system("rm -rf Music_alt_comparison*")

plt.savefig("Music_alt_comparison.jpg")
plt.savefig("Music_alt_comparison.pdf")


ax.set_yscale('log')
ax.set_xscale('log')

plt.savefig("Music_alt_comparison_log_scale.jpg")
plt.savefig("Music_alt_comparison_log_scale.pdf")



#Plotting Histogramms - MUSiC


toys = 10000
rounds = 500

toys_dict = {}
data_dict = {}
for dist in distributions:
    toys_dict[dist] = {}
    data_dict[dist] = {}
    for ec_name in event_classes:
        path_bkg = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_bkg/{ec_name}_{dist}_output.csv"
        path_signal = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_signal/{ec_name}_{dist}_output.csv"
        if os.path.isfile(path_signal) and os.path.isfile(path_bkg):
            toys_dict[dist][ec_name] = np.array(read_outputs(path_bkg))  
            data_dict[dist][ec_name] = np.array(read_outputs(path_signal))  


for dist in distributions:
    p_toys_histo = []
    print("-> Calculating Histogramm for: " + str(dist))
    for round in tqdm(range(toys)):
        P_vals = []
        for ec_name in event_classes:
            path_bkg = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_bkg/{ec_name}_{dist}_output.csv"
            path_signal = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_signal/{ec_name}_{dist}_output.csv"
            if os.path.isfile(path_signal) and os.path.isfile(path_bkg):
                p_toys = toys_dict[dist][ec_name] #np.array(read_outputs(path_bkg))   #Mögliche Quelle für langsame rechnung!
                if round < len(p_toys):
                    P_vals.append(
                        -log10(
                            max(
                                1.0 / float(len(p_toys)),
                                np.sum(np.array(p_toys) <= p_toys[round]) / float(len(p_toys))
                            )    
                        )
                    )    
        counts, bin_edges = np.histogram(P_vals,bins)
        p_toys_histo.append(counts)
    p_toys_histo = np.array(p_toys_histo)    




    p_histo = []
    print("-> Calculating Data for: " + str(dist))
    for round in tqdm(range(rounds)):
        P_vals = []
        for ec_name in event_classes:
                path_bkg = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_bkg/{ec_name}_{dist}_output.csv"
                path_signal = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_signal/{ec_name}_{dist}_output.csv"
                if os.path.isfile(path_signal) and os.path.isfile(path_bkg):
                    #p_toys = np.array(read_outputs(path_bkg))   #Mögliche Quelle für langsame rechnung!
                    #p_signal = np.array(read_outputs(path_signal))   #Mögliche Quelle für langsame rechnung!
                    p_toys = toys_dict[dist][ec_name]
                    p_signal = data_dict[dist][ec_name]
                    if round < len(p_toys):
                        P_vals.append(
                            -log10(
                                max(
                                    1.0 / float(len(p_toys)),
                                    np.sum(np.array(p_toys) <= p_signal[round]) / float(len(p_toys))
                                )    
                            )
                        )    
        counts, bin_edges = np.histogram(P_vals,bins)
        p_histo.append(counts)
    p_histo = np.array(p_histo)     
    
    weights = []
    bkg_err_1sig = []
    bkg_err_2sig = []
    signal_weights = []
    signal_err = []
    for i in range(len(bins)-1):
        weights.append(np.median(p_toys_histo[:,i]))
        bkg_err_1sig.append(np.percentile(p_toys_histo[:,i],68) - np.median(p_toys_histo[:,i]))
        bkg_err_2sig.append(np.percentile(p_toys_histo[:,i],95.4) - np.median(p_toys_histo[:,i]))
        signal_weights.append(np.median(p_histo[:,i]))
        signal_err.append(np.percentile(p_histo[:,i],68) - np.median(p_histo[:,i]))




    fig, ax = plt.subplots(figsize = (15,10))


    plt.hist(bins[:-1], bins, weights=weights, color = "black", histtype = "step", label = "Median - SM", linewidth=2,linestyle= (0, (3, 1, 1, 1, 1, 1)) )

    #plt.bar(bins[:-1], upper_bounds,width = 0.5, align='edge', alpha=0.2, color='red', yerr=[lower_bounds, upper_bounds], error_kw={'ecolor': 'black', 'capsize': 4})

    for i in range(len(weights)):
        if(i == 0):
            rect = patches.Rectangle((bins[i], weights[i] - bkg_err_1sig[i]), binwitdh, 2 * bkg_err_1sig[i], linewidth=1, edgecolor='Blue', facecolor='Blue', alpha=0.3,label = r"SM expectation ± 1 $\sigma$")
            plt.gca().add_patch(rect)
            rect = patches.Rectangle((bins[i], weights[i] - bkg_err_2sig[i]), binwitdh, 2 * bkg_err_2sig[i], linewidth=1, edgecolor='cyan', facecolor='cyan', alpha=0.3,label = r"SM expectation ± 2 $\sigma$")
            plt.gca().add_patch(rect) 
            continue
        rect = patches.Rectangle((bins[i], weights[i] - bkg_err_2sig[i]), binwitdh, 2 * bkg_err_2sig[i], linewidth=1, edgecolor='cyan', facecolor='cyan', alpha=0.3)
        plt.gca().add_patch(rect)
        rect = patches.Rectangle((bins[i], weights[i] - bkg_err_1sig[i]), binwitdh, 2 * bkg_err_1sig[i], linewidth=1, edgecolor='Blue', facecolor='Blue', alpha=0.3)
        plt.gca().add_patch(rect)     

    #counts, bin_edges = np.histogram(P_signal[dist],bins)
    #plt.scatter(np.array(bins[:-1])+0.25,counts, color = "black", s = 50)
    plt.errorbar(np.array(bins[:-1])+binwitdh/2, signal_weights, yerr=signal_err,xerr = binwitdh/2, fmt='+', markersize=0,linewidth = 2, capsize=0, color='red', label = "Observed Deviation")


    sigs = 0.5 * (1-erf([1,2,3]/np.sqrt(2)))
    ymin = min([abs(y) for y in ax.get_ylim()])
    ymax = max([abs(y) for y in ax.get_ylim()])
    ax.vlines(-log10(sigs[0]),0.1,ymax, ls = ":",linewidth = 2, color="chocolate",label=fr"1 $\sigma$")
    ax.vlines(-log10(sigs[1]),0.1,ymax, ls = "-.",linewidth = 2, color="orange",label=fr"2 $\sigma$")
    ax.vlines(-log10(sigs[2]),0.1,ymax, ls = "--",linewidth = 2, color="gold",label=fr"3 $\sigma$")





    plt.yscale("log")
    plt.xlim(0)
    plt.ylim(0.1)
    plt.title("Music - " + str(dist))
    plt.xlabel(r"$-log_{10}(\widetilde{p})$")
    plt.ylabel("Number of Eventclasses")

    plt.yscale("log")
    plt.legend(loc='upper center', bbox_to_anchor=(0.65, 1))
    plt.savefig("P_histo_MUSiC_" + str(dist))
    plt.show()  	


#Plotting Histogramms JS



toys_dict = {}
data_dict = {}
for dist in distributions:
    toys_dict[dist] = {}
    data_dict[dist] = {}
    for ec_name in event_classes:
        path_bkg = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_bkg/{ec_name}_{dist}_output.csv"
        path_signal = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_signal/{ec_name}_{dist}_output.csv"
        if os.path.isfile(path_signal) and os.path.isfile(path_bkg):
            toys_dict[dist][ec_name] = np.array(read_outputs_js(path_bkg))  
            data_dict[dist][ec_name] = np.array(read_outputs_js(path_signal))  




for dist in distributions:
    p_toys_histo = []
    print("-> Calculating Histogramm for: " + str(dist))
    for round in tqdm(range(toys)):
        P_vals = []
        for ec_name in event_classes:
            path_bkg = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_bkg/{ec_name}_{dist}_output.csv"
            path_signal = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_signal/{ec_name}_{dist}_output.csv"
            if os.path.isfile(path_signal) and os.path.isfile(path_bkg):
                    #p_toys = np.array(read_outputs_js(path_bkg))   #Mögliche Quelle für langsame rechnung!
                p_toys = toys_dict[dist][ec_name]
                if round < len(p_toys):
                    P_vals.append(
                        -log10(
                            max(
                                1.0 / float(len(p_toys)),
                                np.sum(np.array(p_toys) >= p_toys[round]) / float(len(p_toys))
                            )    
                        )
                    )    
        counts, bin_edges = np.histogram(P_vals,bins)
        p_toys_histo.append(counts)
    p_toys_histo = np.array(p_toys_histo)    




    p_histo = []
    print("-> Calculating Data for: " + str(dist))
    for round in tqdm(range(rounds)):
        P_vals = []
        for ec_name in event_classes:
            path_bkg = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_bkg/{ec_name}_{dist}_output.csv"
            path_signal = f"/user/scratch/karwatzki/JS_integration/{dist}/{ec_name}_signal/{ec_name}_{dist}_output.csv"
            if os.path.isfile(path_signal) and os.path.isfile(path_bkg):
                #p_toys = np.array(read_outputs_js(path_bkg))   #Mögliche Quelle für langsame rechnung!
                #p_signal = np.array(read_outputs_js(path_signal))   #Mögliche Quelle für langsame rechnung!
                p_toys = toys_dict[dist][ec_name]
                p_signal = data_dict[dist][ec_name]

                if round < len(p_toys):
                    P_vals.append(
                        -log10(
                            max(
                                1.0 / float(len(p_toys)),
                                np.sum(np.array(p_toys) >= p_signal[round]) / float(len(p_toys))
                            )    
                        )
                    )    
        counts, bin_edges = np.histogram(P_vals,bins)
        p_histo.append(counts)
    p_histo = np.array(p_histo)     
    
    weights = []
    bkg_err_1sig = []
    bkg_err_2sig = []
    signal_weights = []
    signal_err = []
    for i in range(len(bins)-1):
        weights.append(np.median(p_toys_histo[:,i]))
        bkg_err_1sig.append(np.percentile(p_toys_histo[:,i],68) - np.median(p_toys_histo[:,i]))
        bkg_err_2sig.append(np.percentile(p_toys_histo[:,i],95.4) - np.median(p_toys_histo[:,i]))
        signal_weights.append(np.median(p_histo[:,i]))
        signal_err.append(np.percentile(p_histo[:,i],68) - np.median(p_histo[:,i]))




    fig, ax = plt.subplots(figsize = (15,10))


    plt.hist(bins[:-1], bins, weights=weights, color = "black", histtype = "step", label = "Median - SM", linewidth=2,linestyle= (0, (3, 1, 1, 1, 1, 1)) )

    #plt.bar(bins[:-1], upper_bounds,width = 0.5, align='edge', alpha=0.2, color='red', yerr=[lower_bounds, upper_bounds], error_kw={'ecolor': 'black', 'capsize': 4})

    for i in range(len(weights)):
        if(i == 0):
            rect = patches.Rectangle((bins[i], weights[i] - bkg_err_2sig[i]), binwitdh, 2 * bkg_err_2sig[i], linewidth=1, edgecolor='springgreen', facecolor='springgreen', alpha=0.4,label = r"SM expectation ± 2 $\sigma$")
            plt.gca().add_patch(rect)
            rect = patches.Rectangle((bins[i], weights[i] - bkg_err_1sig[i]), binwitdh, 2 * bkg_err_1sig[i], linewidth=1, edgecolor='green', facecolor='green', alpha=0.4,label = r"SM expectation ± 1 $\sigma$")
            plt.gca().add_patch(rect) 
            continue
        rect = patches.Rectangle((bins[i], weights[i] - bkg_err_2sig[i]), binwitdh, 2 * bkg_err_2sig[i], linewidth=1, edgecolor='springgreen', facecolor='springgreen', alpha=0.4)
        plt.gca().add_patch(rect)
        rect = patches.Rectangle((bins[i], weights[i] - bkg_err_1sig[i]), binwitdh, 2 * bkg_err_1sig[i], linewidth=1, edgecolor='green', facecolor='green', alpha=0.4)
        plt.gca().add_patch(rect)     

    #counts, bin_edges = np.histogram(P_signal[dist],bins)
    #plt.scatter(np.array(bins[:-1])+0.25,counts, color = "black", s = 50)
    plt.errorbar(np.array(bins[:-1])+binwitdh/2, signal_weights, yerr=signal_err,xerr = binwitdh/2, fmt='+', markersize=0,linewidth = 2, capsize=0, color='red', label = "Observed Deviation")


    sigs = 0.5 * (1-erf([1,2,3]/np.sqrt(2)))
    ymin = min([abs(y) for y in ax.get_ylim()])
    ymax = max([abs(y) for y in ax.get_ylim()])
    ax.vlines(-log10(sigs[0]),0.1,ymax, ls = ":",linewidth = 2, color="chocolate",label=fr"1 $\sigma$")
    ax.vlines(-log10(sigs[1]),0.1,ymax, ls = "-.",linewidth = 2, color="orange",label=fr"2 $\sigma$")
    ax.vlines(-log10(sigs[2]),0.1,ymax, ls = "--",linewidth = 2, color="gold",label=fr"3 $\sigma$")





    plt.yscale("log")
    plt.xlim(0)
    plt.ylim(0.1)
    plt.title("JS - " + str(dist))
    plt.xlabel(r"$-log_{10}(\widetilde{p})$")
    plt.ylabel("Number of Eventclasses")

    plt.yscale("log")
    plt.legend(loc='upper center', bbox_to_anchor=(0.65, 1))
    plt.savefig("P_histo_JS_" + str(dist))
    plt.show()  	