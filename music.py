from tqdm import tqdm
import tempfile
import subprocess
import csv
import json
from data_models import Model
import numpy as np
import random, string
import os


def randomword(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


class NpEncoder(json.JSONEncoder):
    """Custom Numpy to JSON Encoder"""

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


base_input_json = r"""
  {
    "MCBins": [],
    "DataBins": [],
    "NumRounds": 0,
    "mcStatUncertScaleFactor": 1.0,
    "hash": "abc",
    "skipLookupTable": false,
    "gridpack_name": "dummy_gridPack.tar.gz",
    "dicedSignalUncertScaleFactor": 1.0,
    "FirstRound": 0,
    "widthLowStatsRegions": 1,
    "regionYieldThreshold": 1e-06,
    "distribution": "InvMass",
    "dicedMCUncertScaleFactor": 1.0,
    "integralScan": false,
    "coverageThreshold": 0.0,
    "minRegionWidth": 1,
    "thresholdLowStatsDominant": 0.9,
    "sigmaThreshold": 0.6,
    "noLowStatsTreatment": false,
    "name": "Dummy"
  }
  """

base_mc_bin = r"""
      {
        "mcSysUncerts": {
          "syst_1": 3
        },
        "mcStatUncertPerProcessGroup": {
          "process_1": 10
        },
        "width": 10.0,
        "mcEventsPerProcessGroup": {
          "process_1": 100
        },
        "lowerEdge": 0.0
      }
"""


def make_bins(input_mc, input_mc_syst, input_mc_stats, input_bins):
    bins = []
    for index, (value, stats) in enumerate(zip(input_mc, input_mc_stats)):
        bin = json.loads(base_mc_bin)
        bin["mcEventsPerProcessGroup"]["process_1"] = value
        bin["mcStatUncertPerProcessGroup"]["process_1"] = stats
        for idx_syst, syst in enumerate(input_mc_syst):
            bin["mcSysUncerts"][f"syst_{idx_syst}"] = syst[index]
        bin["lowerEdge"] = input_bins[index]
        bin["width"] = input_bins[index + 1] - input_bins[index]
        bins.append(bin)
    return bins


def make_input_json(
    input_data, input_mc, input_mc_syst, input_mc_stats, input_bins, verbose=True
):
    input_json = json.loads(base_input_json)
    input_json["DataBins"] = list(input_data)
    input_json["MCBins"] = make_bins(
        input_mc, input_mc_syst, input_mc_stats, input_bins
    )
    input_json_file = ""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        if verbose:
            print(f"Input JSON: {tmp.name}")
        json.dump(input_json, tmp, ensure_ascii=False, indent=4, cls=NpEncoder)
        input_json_file = tmp.name

    return input_json_file


def make_input_json_for_toys(
    input_mc, input_mc_syst, input_mc_stats, input_bins, verbose=True
):
    input_json = json.loads(base_input_json)
    input_json.pop("DataBins", None)
    input_json["MCBins"] = make_bins(
        input_mc, input_mc_syst, input_mc_stats, input_bins
    )
    input_json_file = ""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        if verbose:
            print(f"Input JSON (toys): {tmp.name}")
        json.dump(input_json, tmp, ensure_ascii=False, indent=4, cls=NpEncoder)
        input_json_file = tmp.name

    return input_json_file


def make_input_json_sifts(normalized_shifts, verbose=True):
    input_json = {}
    for idx_syst, normalized_syst in enumerate(normalized_shifts):
        input_json[f"syst_{idx_syst}"] = normalized_syst.flatten()
    input_json_file = ""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        if verbose:
            print(f"Shifts JSON: {tmp.name}")
        json.dump(input_json, tmp, ensure_ascii=False, indent=4, cls=NpEncoder)
        input_json_file = tmp.name

    return input_json_file


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


def single_test_music(total_data, signal_size, ref_model: Model, data_model: Model):
    if (
        subprocess.run(
            ["ninja"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        ).returncode
        != 0
    ):
        raise Exception(f"ERROR: Could not compile C++ code.")

    if (
        subprocess.run(
            ["ninja", "lut"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        ).returncode
        != 0
    ):
        raise Exception(f"ERROR: Could not generate LUT.")

    # calculate p-data
    scan_process = subprocess.run(
        [
            "MUSiC-RoIScanner/scanClass",
            "--lut",
            "../bin/lookuptable.bin",
            "-j",
            make_input_json(
                data_model.values,
                ref_model.values,
                ref_model.syst_uncert,
                ref_model.stats_uncert,
                ref_model.bins,
            ),
            "-o",
            "outputs/music",
        ],
        text=True,
        capture_output=True,
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.STDOUT,
    )

    if scan_process.returncode != 0:
        print(f"MUSiC output: {scan_process.stdout}")
        raise Exception(f"ERROR: Could not run MUSiC Scan.")

    # print(f"MUSiC output: {scan_process.stdout}")

    p_data = read_outputs("outputs/music/Dummy_InvMass_output.csv")[0]

    # calculate p-tilde
    scan_process = subprocess.run(
        # .bin -s ../test/from_yannik/shiftsaf9c4cbf601ea1ea31a42949941716d56a2999e6.json -l 0 -n 300
        [
            "MUSiC-RoIScanner/scanClass",
            "--lut",
            "../bin/lookuptable.bin",
            "-j",
            make_input_json_for_toys(
                ref_model.values,
                ref_model.syst_uncert,
                ref_model.stats_uncert,
                ref_model.bins,
            ),
            "-s",
            make_input_json_sifts(ref_model.normalized_syst_variations),
            "-l",
            "0",
            "-n",
            str(ref_model.sample_size),
            "-o",
            "outputs/music/toys",
        ],
        text=True,
        capture_output=True,
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.STDOUT,
    )

    if scan_process.returncode != 0:
        print(f"MUSiC output: {scan_process.stdout}")
        raise Exception(f"ERROR: Could not run MUSiC Scan on toys.")

    # print(f"MUSiC output: {scan_process.stdout}")

    p_toys = np.array(read_outputs("outputs/music/toys/Dummy_InvMass_output.csv"))

    # print(f"MUSiC p-value (toys): {p_toys}")
    print(f"MUSiC p-value (data): {p_data}")
    print(f"MUSiC p-tilde: {float(np.sum(p_toys<=p_data)/float(p_toys.shape[0]))}")


def get_music_pvalue(ref_model: Model, data_model: Model):
    temp_dir_path = f"outputs/music/temp/{randomword(10)}"
    os.system(f"mkdir -p {temp_dir_path}/toys")

    # calculate p-data
    input_json = make_input_json(
        data_model.values,
        ref_model.values,
        ref_model.syst_uncert,
        ref_model.stats_uncert,
        ref_model.bins,
        verbose=False,
    )
    scan_process = subprocess.run(
        [
            "MUSiC-RoIScanner/scanClass",
            "--lut",
            "../bin/lookuptable.bin",
            "-j",
            input_json,
            "-o",
            temp_dir_path,
        ],
        text=True,
        capture_output=True,
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.STDOUT,
    )
    os.system(f"rm -rf {input_json}")

    if scan_process.returncode != 0:
        print(f"MUSiC output: {scan_process.stdout}")
        raise Exception(f"ERROR: Could not run MUSiC Scan.")

    # print(f"MUSiC output: {scan_process.stdout}")

    p_data = read_outputs(f"{temp_dir_path}/Dummy_InvMass_output.csv")[0]

    # print("BEGIN TOYS")
    # p_toys = []
    # for idx_toy, toy in tqdm(enumerate(ref_model.sample())):
    #     os.system(f"mkdir -p {temp_dir_path}/toy_{idx_toy}")
    #     # calculate p-data
    #     input_toy_json = make_input_json(
    #         toy,
    #         ref_model.values,
    #         ref_model.syst_uncert,
    #         ref_model.stats_uncert,
    #         ref_model.bins,
    #         verbose=False,
    #     )
    #     scan_process = subprocess.run(
    #         [
    #             "MUSiC-RoIScanner/scanClass",
    #             "--lut",
    #             "../bin/lookuptable.bin",
    #             "-j",
    #             input_toy_json,
    #             "-o",
    #             f"{temp_dir_path}/toy_{idx_toy}",
    #         ],
    #         text=True,
    #         capture_output=True,
    #         # stdout=subprocess.DEVNULL,
    #         # stderr=subprocess.STDOUT,
    #     )
    #     os.system(f"rm -rf {input_toy_json}")

    #     if scan_process.returncode != 0:
    #         print(f"MUSiC output: {scan_process.stdout}")
    #         raise Exception(f"ERROR: Could not run MUSiC Scan.")

    #     # print(f"MUSiC output: {scan_process.stdout}")

    #     p_toys.append(
    #         read_outputs(f"{temp_dir_path}/toy_{idx_toy}/Dummy_InvMass_output.csv")[0]
    #     )
    #     os.system(f"rm -rf {temp_dir_path}/toy_{idx_toy}")
    # print("END TOYS")

    # calculate p-tilde
    input_json_toys = make_input_json_for_toys(
        ref_model.values,
        ref_model.syst_uncert,
        ref_model.stats_uncert,
        ref_model.bins,
        verbose=False,
    )
    input_sifts = make_input_json_sifts(
        ref_model.normalized_syst_variations, verbose=False
    )
    scan_process = subprocess.run(
        [
            "MUSiC-RoIScanner/scanClass",
            "--lut",
            "../bin/lookuptable.bin",
            "-j",
            input_json_toys,
            "-s",
            input_sifts,
            "-l",
            "0",
            "-n",
            str(ref_model.sample_size),
            "-o",
            f"{temp_dir_path}/toys",
        ],
        text=True,
        capture_output=True,
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.STDOUT,
    )

    os.system(f"rm -rf {input_json_toys}")
    os.system(f"rm -rf {input_sifts}")

    if scan_process.returncode != 0:
        print(f"MUSiC output: {scan_process.stdout}")
        raise Exception(f"ERROR: Could not run MUSiC Scan on toys.")

    p_toys = np.array(read_outputs(f"{temp_dir_path}/toys/Dummy_InvMass_output.csv"))
    # p_toys = np.array(p_toys)

    os.system(f"rm -rf {temp_dir_path}")

    result = float(np.sum(p_toys <= p_data) / float(p_toys.shape[0]))
    # return -1 * np.log(max(result, 1e-8))
    return result
