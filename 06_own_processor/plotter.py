import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import json
from pathlib import Path
import argparse

from event_selection import select_events_VBF_enriched


def load_parquet_files(NTuples_path):

    # load the data parquet files and select the events in VBF eneriched region
    data_array = select_events_VBF_enriched(f'{NTuples_path}/DataC_2022/nominal')
    print(f'INFO: Loaded and selected VBF enriched events from {NTuples_path}/DataC_2022/nominal')

    # List of MC samples
    MC_samples = ["ggh", "vbf", "vh", "tth"]
    MC_array_dict = {}

    for MC in MC_samples:
        # load the MC parquet files and select the events in VBF eneriched region
        MC_array_dict[MC] = select_events_VBF_enriched(f'{NTuples_path}/{MC}_M-125_preEE/nominal')
        print(f'INFO: Loaded and selected VBF enriched events from {NTuples_path}/{MC}_M-125_preEE/nominal')

    return data_array, MC_array_dict

def plot_variables(config_file, NTuples_path, outpath):

    # define cross-section for the MC
    rel_cross_sections = {
        'ggh': 52.23 / 59.2789,
        'vbf': 4.078 / 59.2789,
        'vh': (1.457 + 0.9439) / 59.2789,
        'tth': 0.57 / 59.2789
    }

    # load the configuration file for variables
    with open(config_file, 'r') as config:
        plot_config = json.load(config)

    vars_config = plot_config["variables"]

    # get data and MC arrays
    data_arr, MC_arr = load_parquet_files(NTuples_path)

    # blind the data in specified range
    #data_arr = np.where((data_arr.mass > plot_config["blind_range"][0]) & (data_arr.mass < plot_config["blind_range"][1]), np.nan, data_arr)
    data_arr = data_arr[(data_arr.mass < plot_config["blind_range"][0]) | (data_arr.mass > plot_config["blind_range"][1])]

    # get the histograms and plot it
    for var in vars_config.keys():
        plt.style.use(hep.style.CMS)

        config = vars_config[var]
        binning = np.linspace(config["hist_range"][0], config["hist_range"][1], config["n_bins"] + 1)
        
        data_hist, data_edges = np.histogram(data_arr[config["name"]], bins=binning)
        data_hist_sum = np.sum(data_hist)

        MC_hists = {}
        MC_edges = {}
        for MC in MC_arr.keys():
            weight = np.asarray(MC_arr[MC].weight)
            MC_hists[MC], MC_edges[MC] = np.histogram(MC_arr[MC][config["name"]], bins=binning, weights=weight)

            MC_hists[MC] *= (data_hist_sum/np.sum(MC_hists[MC])) * rel_cross_sections[MC]

            hep.histplot((MC_hists[MC], MC_edges[MC]), histtype='step', label=MC)
        
        hep.histplot((data_hist, data_edges), histtype='errorbar', yerr=np.sqrt(data_hist), label="Data", color="black")

        # set other plotting configs
        plt.xlabel(config['xlabel'])
        plt.ylabel(config['ylabel'])
        plt.yscale("log")
        plt.legend()
        plt.xlim(config['plot_range'])
        plt.ylim(bottom=0)
        hep.cms.label("Private work", data=True, year="2022", com=13.6)

        # save the histograms
        Path(outpath).mkdir(exist_ok=True)

        plt.savefig(f"{outpath}/{var}_plot.png")
        print(f"INFO: Histogram saved for {var} in {outpath}")
        plt.clf()

if __name__ == "__main__":
    # Set up argument parser for command line arguments
    parser = argparse.ArgumentParser(description="Plotting script")
    parser.add_argument('config_file', type=str, help="Path to the configuration file")
    parser.add_argument('input_dir', type=str, help="Directory containing the input samples")
    parser.add_argument('output_dir', type=str, help="Directory to save the output plots")

    # Parse the command line arguments
    args = parser.parse_args()

    plot_variables(args.config_file, args.input_dir, args.output_dir)
