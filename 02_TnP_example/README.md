# Exercise 2: Tag and Probe processor

## Tag and Probe concept

For this part of the tutorial, we will focus on the Tag and Probe workflow, which is very useful tool in the context of $H\rightarrow \gamma\gamma$ analysis. 
The T&P is a generic tool developed to measure any user defined object efficiency from data, exploiting di-object resonances like Z or J/Psi. It selects particles of the desired type, and probe the efficiency of a particular selection criterion on those particles. In general the “tag” is an object that passes a set of very tight selection criteria designed to isolate the required particle type (usually an electron or muon, though in principle the method is not strictly limited to these). Tags are often referred to as a “golden” electrons or muons, and the fake rate for passing tag selection criteria should be very small (≪ 1%). A generic set of the desired particle type (i.e. with potentially very loose selection criteria) known as “probes” is selected by pairing these objects with tags such that the invariant mass of the combination is consistent with the mass of the resonance. 

The efficiency itself is measured by counting the number of “probe” particles that pass the desired selection criteria: $\epsilon = P_{pass}/P_{all}$, where $P_{pass}$ is the number of probes passing the selection criteria and $P_{all}$ is the total number of probes counted using the resonance. It is worthwhile to note that in some cases a probe object will also pass the tag selection criteria. In this case it will appear in both the tag and probe lists, and produce a double pairing in the same event. The efficiency formula as written above accounts for these double pairings, but when plotting data/MC agreement of the $Z\rightarrow e^+e^-$ peak for instance one has to take into account that the statistical errors in the plot are off by roughly a factor of $\sqrt 2$.

The selection and pairing of tag and probes for $Z\rightarrow e^+e^-$ events is implemented in HiggsDNA in the `TagAndProbeProcessor`, feel free to have a look at the code that you can find at `HiggsDNA\higgs_dna\workflows\dystudies.py` to familiarise with the method.

Further informations on the method can be found in the Analysis Note [CMS_AN_2009/111](http://cms.cern.ch/iCMS/jsp/openfile.jsp?tp=draft&files=AN2009_111_v1.pdf).

## Perform a Data/MonteCarlo comparison with Drell-Yan events

Now we will run the `TagAndProbeProcessor` on a bunch of `EGamma` data files for `DataC_2022` and some `DY` MC files. The goal is to produce some data/mc comparison plots to check the aggreement between the two.
Some configuration files are available in the `configs` directory:
* `runner.json`: file to specify filenames, metaconditions, systematics and corrections for each sample to HiggsDNA.
* `02_samples_local.json`: a `json` file containing the data and MC files we will run on, the files are split in datasets, which correspond to what you can find in the `runner.json`. Suggested for users on `lxplus`. It is also the default in the `runner.json`, so if you're running from somewhere else you should swap the names there before running HiggsDNA.
* `02_samples.json`: equivalent to `02_samples_local.json` but with `xrootd` paths, this file is here only for completeness, ignore it if you're running on `lxplus` since it will be the topic of later chapters of the tutorial. (In case you need to use this remember to set up a `voms-proxy ` with `voms-proxy-init --rfc --voms cms -valid 192:00`).

You should familiarise with the content of these files before moving on.

Let's produce some NTuples with HiggsDNA!

First activate the environment you should have created in the previous sections of the tutorial, and set up the grid certificate to access files.
```
micromamba activate <path/name-of-your-environment>
```
Now we have to fetch some configuration jsons that are used to select only good lumis from data files. To do that we will move to the `scripts` directory in HiggsDNA and execute `pull_files.py`.
```
cd ../HiggsDNA/scripts/

python pull_files.py --target GoldenJSON
```
Strong of your newly downloaded Golden jsons we can go back to the `configs` directory.
```
cd ../../02_TnP_example/configs/
```
As you probably noticed here there is also a running script that we will use to run the analysis.
Check what command you are running.
```
cat run_HiggsDNA.sh
```
Using this we will run HiggsDNA with the `tagAndProbe` workflow locally on our machine, select the `.*SingleEle.*` trigger path from our data files, and use the metaconditions summarised in the `runner.json` file.
```
source run_HiggsDNA.sh
```
You might get some warnings for missing PhotonID weight files or some `PerformanceWarning` for fragmented dataset issues but you can safely ignore them.

The execution will take a couple of minutes. When you're done you should have created a directory called `02_NTuples` and containing a set of `.parquet` files with the output of our analysis.
These files can easily be checked using python with the `awkward` and `numpy` libraries. 

You will notice that there is a single file for each "chunk" of data that was processed. At this stage one can load each file separatly to have the full statistics while looking at the output, or one can use the post-processing tools that are available in HiggsDNA to merge the output, this latter option has some additional handy features like categorisation and normalisation of the events.

You will be presented these scripts at a later stage of the tutorial, so for now you can load the files directly as they are from the output directory. In case something went wrong in the previous step you can link the output you would get from the merging step from a backup location and go on with the tasks.

Commands to run to link the output.
```
cd ../02_NTuples

mkdir merged

ln -rs /eos/cms/store/group/phys_higgs/cmshgg/tutorials/HiggsDNA_FinalFits_2024/HiggsDNA_part/02_03_TnP/merged_NTuples/DataC_2022 merged/Data_2022
ln -rs /eos/cms/store/group/phys_higgs/cmshgg/tutorials/HiggsDNA_FinalFits_2024/HiggsDNA_part/02_03_TnP/merged_NTuples/DY merged/DY
```

## Plotting

Now that we have the merged output we want to produce some data/mc comparison plots. Two options are available, a notebook (`plotter.ipynb`), and a python script (`plotter.py`).
The two are equivalent, try them out and get experienced with the manipulation of the awkward arrays to make plots.

Tasks:
- Produce Data/MC comparison plot for $Z\rightarrow e^+e^-$ events (mass, $\sigma_m / m$, tag $p_T$).

