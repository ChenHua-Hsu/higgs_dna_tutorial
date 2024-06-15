# Exercise 6: Own processor

In this part of the exercise, you will create your own processor to save additional information about the dijet system formed by the two leading-pT jets.

## Getting the sample JSON for remote files

For this part of the tutorial, we will again access the files remotely. To begin, execute the command below to set up your grid proxy:

```
voms-proxy-init --rfc --voms cms -valid 192:00
```

Please also check the file `configs/samples.txt` to see which samples we will use.
These are the same samples you used in the 4th exercise of the tutorial on the base processor.
We will use the `HiggsDNA/higgs_dna/samples/fetch.py` script as a helper to set up our sample JSON. 

> **Note:** If you have already produced the file using `fetch.py` in exercise 4, you can skip the below step and move on to `setting up your own processor part`. Just copy the `samples.json` into `configs` directory of this exercise and change the name of the file to `06_samples.json`.

Hoping you are already familiarized with `fetch.py` script from previous exercises, lets start directly by producing the `samples.json` file.
Execute the script, supplying the `txt` file:

```
cd configs
fetch.py --input 06_samples.txt --w Yolo
```
Verify that `configs/samples.json` has been created in this directory and that its contents are correct.
You should be able to understand what the `configs/samples.json` should contain.



## Setting up your own processor

Notice that you have an `own_processor.py` file in the main directory of this exercise.
Copy this file to the `HiggsDNA/higgs_dna/workflow`. 
This is where you would add a new processor if you ever need to design a workflow for your analysis.
You can copy the file by executing the command:

```
cp ../own_processor.py ../../HiggsDNA/higgs_dna/workflows/
```

Take some time to understand the structure of `own_processor.py`. 
The `OwnProcessor` class inherits from the `HggBaseProcessor` class, which is imported from `higgs_dna.workflows.base.py`.
By inheriting the `HggBaseProcessor` class, you also inherit its attributes and methods.
So you do not have to redefine them unless you need to make changes for your analysis.
In this exercise, you will be modifying the `process` function of `OwnProcessor` class to save information on the dijet system formed by the two leading-pT jets.
Note that the skeleton of this `process` function provided in the exercise is simplified and does not contain some parts that are not necessary for this exercise.
If, in the future, you are building a processor for your own analysis involving diphotons, it is essential to follow the skeleton of the `process` function from `HggBaseProcessor` to include all necessary components for your analysis. 
You only need to add extra code lines in the `process` function as required by your analysis at the appropriate places.

The jet selection has already been completed, as is also present in the base workflow.
To add information on the dijet system, first create the dijet combination and convert it into a `PtEtaPhiCandidate` in the same way it is done for diphotons in the `process` function.
Next, calculate a few variables for the dijet system, such as $|\Delta \eta_{jj}|$, $|\Delta \phi_{jj}|$.
Select the dijet combination formed by the two leading-pT jets if it exists; otherwise, pad with -999.0. 
Add these variables to the diphoton collection, which will be saved in the parquet files later.
Note that a helper function, `choose_nth_object_variable`, is already defined in `OwnProcessor` class to help you select and pad the variables of the required dijet combination.
The code lines for selecting the dijet combination and adding the information to the diphoton collection are provided to you in commented lines from 448-489.
Please understand how this is done and remove the comments from these lines.

Before testing your new processor, it is important to add the new workflow in the `HiggsDNA/higgs_dna/workflow/__init__.py` file, just like the other workflows.
This step ensures that the new processor is added into the existing workflows and recognized as part of the Python package.
You can try to add this manually yourself.
If you are unable to figure it out, you can use a helper bash script provided to you. To use this, execute the following command:

```
bash initialize_processor.sh
```
The above bash script adds the following two lines to `HiggsDNA/higgs_dna/workflow/__init__.py`:
```
from higgs_dna.workflows.own_processor import OwnProcessor
workflows["ownprocessor"] = OwnProcessor
```


## Ntuplising signal and data

Hoping you are already familiarized with the contents of `configs/runner.json` at this point. 
We are not including any corrections or systematics in this exercise.
With the ingredient of the sample json, you are ready to NTuplise both data and signal MC in one go. 
This is the command you have already run previously. 
Please execute the following command:

```
run_analysis.py --json-analysis runner.json --dump ../NTuples --skipCQR --executor futures --limit 15 --skipbadfiles
```

Note that the `--limit` options restricts the number of files to process.
To get a decent looking plot, we recommend using at least ten files.
Of course, the more the better.


Errors like "ModuleNotFoundError: Install XRootD python bindings with:" sometimes occur, apparently not even deterministically.
The origin is also not clear to us.
If it also happens for you, you can just try again.
If it keeps crashing with remote files or you have problems with this in general, you can again fall back to a handful of local files that we put on `eos` for you.
They are available at `/eos/cms/store/group/phys_higgs/cmshgg/tutorials/HiggsDNA_FinalFits_2024/HiggsDNA_part/04_base_processor/` and the corresponding sample JSON is provided in this directory as `config/06_samples_local.json`.
If you want to NTuplise the files from `eos`, make sure to change the path to the sample JSON in `config/runner.json`.
Again, if it takes too long for you, we recommend adjusting the number in the `--limit` argument.


## Plotting

For plotting, you can move to the main directory of this exercise.
We also provide a `events_selection.py` script, which selects the events according to the VBF-enriched phase space. 
The selection for the VBF-enriched region is designed with loose cut-based kinematic criteria.
Go through this script and try to understand how the events are selected.
You can cusult [CMS-HIG-19-016](https://cds.cern.ch/record/2825355/files/CMS-HIG-19-016-arXiv.pdf) for more details.


Next, you can now use your freshly produced NTuples and plot some of the variables such as $p_{\mathrm{T}}^{\\gamma\\gamma}$, $p_{\mathrm{T}}^{j_2}$, $|\\Delta\\phi_{j_1,j_2}|$, etc.
For this, we provide a `plotter.py` script which you can find in the main directory of this exercise.
Please read through this script and make sure you roughly understand what is happening.
Also check `configs/plotter_configs.json`. This configuration file contains the settings for the plots and variables you will be plotting.
Then, execute the script with the following command:
```
python plotter.py ./configs/plotter_configs.json ./NTuples ./plots
```
In case the Ntuplising did not work for you, you can use samples we provide in `/eos/cms/store/group/phys_higgs/cmshgg/tutorials/HiggsDNA_FinalFits_2024/HiggsDNA_part/06_own_processor/NTuples/` instead. In that case, you need to change the input path when calling the plotter.
You might encounter some warnings while running the plotting script, but you can ignore them.

Now, check the newly created plots. 
In the plots, the MC is normalised to data and then multiplies by the relative cross section of the processes.
Do they make sense to you?


