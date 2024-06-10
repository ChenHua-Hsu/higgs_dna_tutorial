# Datacard creation
In this section we will learn how to build a Higgs Combine datacard defines the signal and background models and includes the impact of systematic uncertainties in the analysis. Move to the Datacard folder:
```
cd $CMSSW_BASE/src/flashggFinalFit/Datacard
```
A datacard is a `.txt` file which effectively packages everything up, and it is the input to Combine to use for the final results extraction. The datacard contains:
* Paths to signal pdfs, background pdfs and datasets for each category.
* Defines the rate of each process. In H $\rightarrow\gamma\gamma$ analyses, the rate for signal processes is specified as the integrated luminosity (in pb). The other parts of the normalisation i.e. $[\sigma\cdot\mathcal{B}]_i$ and $\epsilon_{ij}$ are picked up from the signal model workspaces (`_norm` functions). A value of `1` is defined as the rate for background, as the models are constructed directly from data.
* Systematic uncertainties affecting the yield of each process x category combination. These are specified as `lnN` uncertainties in the datacard, and are split into experimental and theoretical uncertainties. 
* Signal shape nuisance parameters (Scale and Smearing)
* Pdf indices are the discrete nuisance parameters which label the choice of the bkg pdf in each analysis category.

We will use the workspaces built in the Trees2WS section as input. If you ran into problems with the Trees2WS section and have not already copied the output workspaces, they can be found in the `cmshgg` area:
```
PATH_TO_INPUTS="Add path to eos user area"

cp -rp /eos/cms/store/group/phys_higgs/cmshgg/tutorials/HiggsDNA_FinalFits_2024/FinalFits_tutorial/workspaces ${PATH_TO_INPUTS}
```

## Yield calculation
The first step is to calculate the nominal and systematic-varied yields for each signal (proc,cat) combination. To do this, set the `PATH_TO_INPUTS` variable accordingly:
```
PATH_TO_INPUTS=${CMSSW_BASE}/src/flashggFinalFit/Trees2WS/inputs/ # CHANGE TO WHERE YOU SAVED THEM (IF DIFFERENT)
```
and then run this command:
```
python3 RunYields.py --inputWSDirMap 2022preEE=$PATH_TO_INPUTS/workspaces/signal_2022preEE --cats auto --procs auto --ext tutorial --mergeYears --skipCOWCorr --doSystematics --batch condor --queue espresso
```
The yields are calculated from the signal RooWorkspaces generated in the Trees2WS step. The systematic uncertainties to be processed with this script are defined in `systematics.py`. You need to configure this file to match your input workspaces by simply commenting out/adding new systematics to the relevant containers, which are separated into theory yield, experimental yield and signal shape uncertainties.

For yield uncertainties (appearing as `lnN` in the datacard), there are two `'type'`'s which are supported:
* `'type':'constant'`: supports a single value for all processes e.g. `BR_hgg`, or a year-dependent value. Also you can define more complicated mappings of numbers to processes using json inputs e.g. `QCDscale_ggH`.
* `'type':'factory'`: treatment is inferred automatically from the input RooWorkspace. This supports both weights in the nominal `RooDataSet` e.g. `weight_AlphaSUp`, or separate systematic-varied `RooDataHist` e.g. for JEC nuisance parameters. 

Each entry has the option to (de)correlate across years, by setting `'correlateAcrossYears':0`, in which case a separate nuisance parameter will be introduced per year.

The theory uncertainties of `'type':'factory'` have an additional input: `'tiers'` list, which represents the different options for calculating the impact of this uncertainty. If `shape` is used, then the total signal yield of each process across all categories is kept constant i.e. this calculates the migrations of events across analysis categories. This is useful for things like `LHEScaleWeights` and `LHEPDfWeights` where you do not want to consider the effect on the inclusive yield. Note, this approach does not consider events outsider of acceptance i.e. the ones which do not enter any analysis category. For this we need to keep track of the yields throughout the whole HiggsDNA skimming. This functionality will be added to HiggsDNA ASAP. More information for the different tiers is provided in the [ReadME](https://github.com/cms-analysis/flashggFinalFit/tree/higgsdnafinalfit/Datacard#systematics-details).

The output of the yield calculation step are pandas DataFrames stored in `yields_tutorial`. These DataFrame contains all the yield variations, as well as information on the Model workspace files. Let's open one:
```
$ python3
>>> import pickle as pkl
>>> with open("yields_tutorial/EBEB_lowR9highR9.pkl", "rb") as fpkl:
...     data = pkl.load(fpkl)

>>> data
>>> data.iloc[0]
```

<details>
<summary>Output</summary>

```
        year  type procOriginal  ... weight_PS_ISR_down_yield weight_PS_FSR_up_yield weight_PS_FSR_down_yield
0  2022preEE   sig         GG2H  ...                 0.015129               0.015453                 0.015789
1  2022preEE   sig          VBF  ...                  0.01137               0.011185                 0.011862
2     merged   bkg     bkg_mass  ...                        -                      -                        -
3     merged  data     data_obs  ...                        -                      -                        -

[4 rows x 29 columns]

year                                                                        2022preEE
type                                                                              sig
procOriginal                                                                     GG2H
proc                                                                ggH_2022preEE_hgg
proc_s0                                                                           ggh
cat                                                                  EBEB_lowR9highR9
inputWSFile                         /eos/user/j/jlangfor/icrf/hgg/FinalFitsTutoria...
nominalDataName                                        ggh_125_13TeV_EBEB_lowR9highR9
modelWSFile                         ./Models/signal/CMS-HGG_sigfit_packaged_EBEB_l...
model                               wsig_13TeV:hggpdfsmrel_GG2H_2022preEE_EBEB_low...
rate                                                                           8000.0
nominal_yield                                                                0.015526
sumw2                                                                             0.0
weight_Pileup_up_yield                                                       0.015531
weight_Pileup_down_yield                                                     0.015515
weight_TriggerSF_up_yield                                                    0.015574
weight_TriggerSF_down_yield                                                  0.015467
weight_ElectronVetoSF_up_yield                                                0.01562
weight_ElectronVetoSF_down_yield                                             0.015431
weight_PreselSF_up_yield                                                     0.015847
weight_PreselSF_down_yield                                                   0.015207
weight_SF_photon_ID_up_yield                                                 0.015871
weight_SF_photon_ID_down_yield                                               0.015184
weight_AlphaS_up_yield                                                       0.016039
weight_AlphaS_down_yield                                                     0.014959
weight_PS_ISR_up_yield                                                       0.015837
weight_PS_ISR_down_yield                                                     0.015129
weight_PS_FSR_up_yield                                                       0.015453
weight_PS_FSR_down_yield                                                     0.015789
```
</details>

These files contain all the information necessary to build the datacard.

## Datacard creation
We can make the datacard with the following command:
```
python3 makeDatacard.py --ext tutorial --years 2022preEE --prune --doTrueYield --skipCOWCorr --doSystematics --doMCStatUncertainty --saveDataFrame --output Datacard_tutorial
```

The `--prune` option is used to remove signal processes which contribute less than 0.1% of the total yield in a given analysis category. In this tutorial we only consider two signals (ggH and VBF) and so the pruning has little effect. However, for larger analyses with many (proc,cat) combinations e.g. STXS Run 2, the pruning can prove to be very useful, and speed up the fits signficantly. 

The `--doMCStatUncertainty` adds a nuisance parameter which refers to the MC statistical uncertainty in the yield estimation in each analysis category. This was not present in Run 2, but we realised that it should be added.

The output of this command is the Higgs combine datacard (`Datacard_tutorial.txt`) to be used as input in the final results extraction. Open it up and make sure you understand the different lines. If not then it might be useful to return to the Combine [parametric exercise](http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/tutorial2023/parametric_exercise/) which gives a good explanation.