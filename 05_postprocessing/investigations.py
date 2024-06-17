import awkward as ak
import numpy as np
from pathlib import Path
import hist
import uproot
import matplotlib.pyplot as plt

# CMS style

import mplhep as hep

hep.style.use("CMS")
palette = ["#5790fc", "#f89c20", "#e42536", "#964a8b", "#9c9ca1", "#7a21dd"]

# Load the input
# Now that we've produced all our `.parquet` and `.root` trees we can check that everything is in order, again with `awkward` and `numpy`.
# First we load the MC and data samples as we did in the previous steps, starting from the merged `.parquets`.

# Load MC samples
MC = {}
processes = ["ggh_M-120", "ggh_M-125", "ggh_M-130", "vbf_M-120", "vbf_M-125", "vbf_M-130"]
for i, proc in enumerate(processes):
    MC[f'{proc}'] = {}
    MC[f'{proc}']["untagged"] = ak.from_parquet(f'05_NTuples/merged_untagged/{proc}_preEE/NOTAG_merged.parquet')
    for cat in ["EBEB_highR9highR9", "EBEB_highR9lowR9", "EBEB_lowR9highR9"]:
        MC[f'{proc}'][cat] = ak.from_parquet(f'05_NTuples/merged/{proc}_preEE/nominal/{cat}_merged.parquet')

# Understanding the weights
# In the trees there are multiple fields that store different version of the event weights. Let's start having a look at what's available in one of the samples.

print("Available weight fields:")
for f in MC[proc]["EBEB_highR9highR9"].fields:
    if "weight" in f:
        print(f"    {f}")

# From here you can see that all the weight systematics variuations are stored in different branches. Furthermore there are different versions of the nominal weigh:
# * `weight`: weight of the events with corrections applied, after the normalisation to Efficiency x Acceptance made during the merging step.
# * `weight_nominal`: same as the previous field but before the normalisation with respect to the sum of the Generator weight of the full MC sample.
# * `weight_central`: set of weights centered around one, this is needed to plot sistematic variations properly and not consider corrections twice.
# 
# Now we can have a look at the expected number of events for each sample according to theoretical values of cross section and branching fractions.
        
cross_section = {
    "ggh_M-120" : 56110,   # from https://arxiv.org/pdf/2402.09955
    "ggh_M-125" : 52230,
    "ggh_M-130" : 48750,
    "vbf_M-120" : 4078,  # theoretical cross sections are not available for mass values different from 125 for VBF
    "vbf_M-125" : 4078,
    "vbf_M-130" : 4078,
}
eff = {}

lumi = 8.
BF = 0.00227

print()
print("-"*100)
print("Expected Run 3 preEE events:")
print(f"  luminosity: {lumi} /fb")
print(f'  H → \u03b3 \u03b3 BR: {BF}')
for sample in cross_section:
    eff[sample] = ak.sum(MC[sample]["untagged"].weight)
    print(f"    {sample}:")
    print(f"        * produced events: {cross_section[sample] * lumi * BF}")
    print(f"        * expected selected events: {cross_section[sample] * lumi * BF * eff[sample]}")
    print(f"        * efficiency x acceptance: {eff[sample]}")


# And have a look at the structure and sum of the different weight fields.
print()
print("-"*100)
print('sum of weight_central:', ak.sum(MC[proc]["untagged"].weight_central), MC[proc]["untagged"].weight_central[:5].tolist())
print('sum of weight:', ak.sum(MC[proc]["untagged"].weight), MC[proc]["untagged"].weight[:5].tolist())
print('sum of weight_nominal:', ak.sum(MC[proc]["untagged"].weight_nominal), MC[proc]["untagged"].weight_nominal[:5].tolist())
print("-"*100)

# Plot systematics an mass variations

# directory for output plots
plots_dir = './plots'
Path(plots_dir).mkdir(exist_ok=True)

# Define the binning
n_bins = 120
x_low = 90
x_high = 150
binning = np.linspace(x_low, x_high, n_bins + 1)
width = binning[1] - binning[0]
center = (binning[:-1] + binning[1:]) / 2

# Mass plot
# We then create a mass histograms starting from our data and MC arrays

fig, ax0 = plt.subplots(1,1, figsize=(7, 7))

var = "mass"

LeadPhoton_et_ax  = hist.axis.Regular(n_bins, x_low, x_high, flow=False, name="ax")
LeadPhoton_et_cax_ggh = hist.axis.StrCategory([label for label in processes if "ggh" in label], name="c")
LeadPhoton_et_cax_vbf = hist.axis.StrCategory([label for label in processes if "vbf" in label], name="c")

full_hist_ggh = hist.Hist(LeadPhoton_et_ax, LeadPhoton_et_cax_ggh)
full_hist_ggh_err = hist.Hist(LeadPhoton_et_ax, LeadPhoton_et_cax_ggh)
full_hist_vbf = hist.Hist(LeadPhoton_et_ax, LeadPhoton_et_cax_vbf)
full_hist_vbf_err = hist.Hist(LeadPhoton_et_ax, LeadPhoton_et_cax_vbf)

for sample in [*MC]:
    for cat in MC[sample]:
        MC[sample][cat]["weight_norm"] = MC[sample][cat]["weight"] * cross_section[sample] * lumi * BF
        MC[sample][cat]["square_weight"] = MC[sample][cat]["weight_norm"] ** 2

        if cat == "EBEB_highR9highR9":
            if "ggh" in sample:
                full_hist_ggh.fill(ax = MC[sample][cat][var], weight = MC[sample][cat]["weight_norm"], c=sample)
                full_hist_ggh_err.fill(ax = MC[sample][cat][var], weight = MC[sample][cat]["square_weight"], c=sample)
            elif "vbf" in sample:
                full_hist_vbf.fill(ax = MC[sample][cat][var], weight = MC[sample][cat]["weight_norm"], c=sample)
                full_hist_vbf_err.fill(ax = MC[sample][cat][var], weight = MC[sample][cat]["square_weight"], c=sample)

ggh_stack = full_hist_ggh.stack("c")
ggh_stack_err = full_hist_ggh_err.stack("c")

stack = False
ggh_stack[::-1].plot(ax=ax0, stack=stack, histtype="step")

mc = {}
mc["bins"] = {}
mc["errs"] = {}
mc["edges"] = {}

# this is useful to manipulate bin content better when doing ratios and error plotting
for sample in [*full_hist_ggh.axes[1]]:
    mc["bins"][sample], mc["edges"][sample] = full_hist_ggh[:,sample].to_numpy()
    half_bin = np.abs((mc["edges"][sample][1] - mc["edges"][sample][0])) / 2
    mc["edges"][sample] = mc["edges"][sample] + half_bin
    mc["errs"][sample] = np.sqrt(full_hist_ggh[:,sample].to_numpy()[0])

ydn = {}
yup = {}
#create up and down edges to plot shaded area for each bin
for sample in [*full_hist_ggh.axes[1]]:
    ydn[sample] = [mc["bins"][sample][i] - x for i, x in enumerate(mc["errs"][sample])]
    yup[sample] = [mc["bins"][sample][i] + x for i, x in enumerate(mc["errs"][sample])]

# plot shaded area for MC errors
for j, sample in enumerate([*full_hist_ggh.axes[1]]):
    if stack: break
    for i, x in enumerate(mc["edges"][sample][:-1]):
        if i == 0:
            ax0.fill_between([x - half_bin, x + half_bin], [ydn[sample][i], ydn[sample][i]], [yup[sample][i], yup[sample][i]], facecolor=palette[2::-1][j], alpha=0.5, edgecolor=palette[2::-1][j], label=f"{sample} stat unc.") # we want just one entry in the legend
        else:
            ax0.fill_between([x - half_bin, x + half_bin], [ydn[sample][i], ydn[sample][i]], [yup[sample][i], yup[sample][i]], facecolor=palette[2::-1][j], alpha=0.5, edgecolor=palette[2::-1][j], label="")

# cosmetics
ax0.set_ylabel('Events', fontsize=14)
ax0.set_xlabel('', fontsize=1)
ax0.set_title(r'$ggH \;\rightarrow \gamma\gamma$ Mass', fontsize=14)
ax0.tick_params(axis='x', labelsize=10)
ax0.tick_params(axis='y', labelsize=10)
ax0.grid(color='grey', linestyle='--', alpha=0.5)

# Style
handles, labels = ax0.get_legend_handles_labels()
ax0.legend(handles[::-1], labels[::-1], prop={'size': 14})
# hep.cms.label()

ax0.set_xlim([x_low, x_high])
ax0.set_xlabel('Mass [GeV]', fontsize=14)
plt.tight_layout()
    
plt.plot()
plt.savefig(f'{plots_dir}/ggh_masses.png')

# Weight systematic 
# We can now have a look at the effect of the weight systematics, we plot the Photon ID one, what is the effect of this systematic?

fig, ax0 = plt.subplots(1,1, figsize=(7, 7))

var = "mass"
n_bins = 30

LeadPhoton_et_ax  = hist.axis.Regular(n_bins, x_low, x_high, flow=False, name="ax")
LeadPhoton_et_cax_ggh = hist.axis.StrCategory(["nominal", "PhotonID_Up", "PhotonID_Down"], name="c")

full_hist_ggh = hist.Hist(LeadPhoton_et_ax, LeadPhoton_et_cax_ggh)

sample = "ggh_M-125"
cat == "EBEB_highR9highR9"
full_hist_ggh.fill(ax = MC[sample][cat][var], weight = MC[sample][cat]["weight_central"], c="nominal")
full_hist_ggh.fill(ax = MC[sample][cat][var], weight = MC[sample][cat]["weight_SF_photon_IDUp"], c="PhotonID_Up")
full_hist_ggh.fill(ax = MC[sample][cat][var], weight = MC[sample][cat]["weight_SF_photon_IDDown"], c="PhotonID_Down")

ggh_stack = full_hist_ggh.stack("c")

stack = False
ggh_stack[::-1].plot(ax=ax0, stack=stack, histtype="step")

# cosmetics
ax0.set_ylabel('A.U.', fontsize=14)
ax0.set_xlabel('', fontsize=1)
ax0.set_title(r'$ggH \;\rightarrow \gamma\gamma$ Mass - effect of weight systematics', fontsize=14)
ax0.tick_params(axis='x', labelsize=10)
ax0.tick_params(axis='y', labelsize=10)

# plot error bars
# ax0.errorbar(edges_data, mc["bins"]["tot"], yerr=mc["errs"]["tot"] , color="gray", marker="_", linestyle="")
# ax0.legend( prop={'size': 14})
ax0.grid(color='grey', linestyle='--', alpha=0.5)

# Style
handles, labels = ax0.get_legend_handles_labels()
ax0.legend(handles[::-1], labels[::-1], prop={'size': 14})
# hep.cms.label()

ax0.set_xlim([x_low, x_high])
ax0.set_xlabel('Mass [GeV]', fontsize=14)
plt.tight_layout()
    
plt.plot()
plt.savefig(f'{plots_dir}/ggh_weight_syst.png')

# Object systematic
# Let's look at object systematics now, to do so we have to load the variated events from different `.parquet`. What is the difference between the effect of the Scale systematic and the Photon Id one?

# Load MC samples
MC_variations = {}
proc = "ggh_M-120"
for var in ["nominal", "Scale_up", "Scale_down", "Smearing_up", "Smearing_down"]:
    MC_variations[f'{var}'] = {}
    for cat in ["EBEB_highR9highR9", "EBEB_highR9lowR9", "EBEB_lowR9highR9"]:
        MC_variations[f'{var}'][cat] = ak.from_parquet(f'05_NTuples/merged/{proc}_preEE/{var}/{cat}_merged.parquet')

fig, ax0 = plt.subplots(1,1, figsize=(7, 7))

var = "mass"
n_bins = 30
LeadPhoton_et_ax  = hist.axis.Regular(n_bins, x_low, x_high, flow=False, name="ax")
LeadPhoton_et_cax_ggh = hist.axis.StrCategory(["nominal", "Scale_up", "Scale_down"], name="c")

full_hist_ggh = hist.Hist(LeadPhoton_et_ax, LeadPhoton_et_cax_ggh)

cat == "EBEB_highR9highR9"
for variation in ["nominal", "Scale_up", "Scale_down"]:
    full_hist_ggh.fill(ax = MC_variations[variation][cat][var], weight = MC_variations[variation][cat]["weight"], c=variation)

ggh_stack = full_hist_ggh.stack("c")

stack = False
ggh_stack[::-1].plot(ax=ax0, stack=stack, histtype="step")

# cosmetics
ax0.set_ylabel('Eff x Acc', fontsize=14)
ax0.set_xlabel('', fontsize=1)
ax0.set_title(r'$ggH \;\rightarrow \gamma\gamma$ Mass - effect of Scale systematic', fontsize=14)
ax0.tick_params(axis='x', labelsize=10)
ax0.tick_params(axis='y', labelsize=10)
ax0.grid(color='grey', linestyle='--', alpha=0.5)

# Style
handles, labels = ax0.get_legend_handles_labels()
ax0.legend(handles[::-1], labels[::-1], prop={'size': 14})
# hep.cms.label()

ax0.set_xlim([x_low, x_high])
ax0.set_xlabel('Mass [GeV]', fontsize=14)
plt.tight_layout()
    
plt.plot()
plt.savefig(f'{plots_dir}/ggh_object_sys.png')

# ROOT trees
# Now we can also check the ROOT version of the same quantities by looking at the files obtaine after the `--root` step of the postprocessing.
# We start loading the files with `uproot`. From the structure of the directory in the root file you can see that in this case all the variation and categories are included in a single file.

file = uproot.open('05_NTuples/root/ggh_M-125_preEE/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8.root')

file.keys()

# Here we look at what is inside one of the category `TBranch`.

tree = file['DiphotonTree/ggh_125_13TeV_EBEB_highR9highR9']
ggh_125_EBEB = tree.arrays()
ggh_125_EBEB.fields

# Hands on!
# Now Try to plot something from the ROOT files and check that the expected number of events has not changed after the conversion.

