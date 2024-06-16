# Exercise 4: Base processor

## Getting the sample JSON for remote files

For this part of the tutorial, we would like you to explore remote file access.
To start with, execute the comamnd below to setup your grid proxy:

```
voms-proxy-init --rfc --voms cms -valid 192:00
```

Please also check the file `configs/samples.txt` to see which samples we will use.
The file contains a set of dataset names and DAS strings per line.
We will use centrally produced v13 nanoAODs from 2022preEE (both DataC and all four main signal modes for MH=125 GeV).

We will use the `HiggsDNA/higgs_dna/samples/fetch.py` script as a helper to set up our sample JSON.
Of course, you could also create it yourself but that would involve copying tens, hundreds, or even thousands of file paths manually from DAS with a high likelihood of human error.
You don't really want to do that.
Execute

```
cd configs
fetch.py --help
```

to check the command-line arguments for the script.
Do you understand why `fetch.py` works even though this script is not available in `configs`?
Then, execute the script, supplying the `txt` file:

```
fetch.py --input samples.txt --yolo
```

Check that `configs/samples.json` has been created in this directory and that it looks sensible.
Notice that the `DataC_2022` key contains a lot of files!
This is completely excepted, that era corresponds to about 5/fb and the EGamma triggers take a large rate portion of the recorded rate of the CMS experiment.
For our illustrative purposes in this tutorial, it is not necessary to NTuplise all 182 files, of course.
Therefore, we will later restrict the number of files to process when running `run_analysis.py`.

Please also check the `configs/runner.json` file and familiarise yourself with the contents.
For this simple demonstration, we only consider the most relevant corrections and no systematics.
In general, most of the content should already be clear to you by this point.
You can check your knowledge by thinking about the following questions:
- What does the `year` entry per sample actually influence?
- Why do we not consider a scale factor for a cut on a photon ID MVA?
- If we wanted to implement `scale` and `smearing` systematics as well, how can we achieve this?

## Ntuplising signal and data

With the ingredient of the sample json, you are ready to NTuplise both data and signal MC in one go.

Before that, we have to make sure that the necessary ingredients are there:
```
python ../HiggsDNA/scripts/pull_files.py --all
```

Please execute

```
run_analysis.py --json-analysis runner.json --dump ../NTuples --fiducialCuts classical --skipCQR --executor futures --limit 15
```

Note that the `--limit` options restricts the number of files to process.
To get a decent looking plot, we recommend using at least three files.
Of course, the more the better.
We found that 10-15 files should still be a reasonable number given the limited computing ressources on lxplus and the limited time during the tutorial.
From our tests, 15 files take about O(10 minutes).
Feel free to try a number in that range and go lower if it takes way too long in your case.

Errors like "ModuleNotFoundError: Install XRootD python bindings with:" sometimes occur, apparently not even deterministically.
The origin is also not clear to us.
If it also happens for you, you can just try again.
If it keeps crashing with remote files or you have problems with this in general, you can always fall back to a handful of local files that we put on `eos` for you.
They are available at `/eos/cms/store/group/phys_higgs/cmshgg/tutorials/HiggsDNA_FinalFits_2024/HiggsDNA_part/04_base_processor` and the corresponding sample JSON is provided in this directory as `config/samples_local.json`.
If you want to NTuplise the files from `eos`, make sure to change the path to the sample JSON in `config/runner.json`.
Again, if it takes too long for you, we recommend adjusting the number in the `--limit` argument.

Questions to check your understanding:
- What does `--fiducialCuts classical` mean in this context?
- What does `--executor futures` mean in this context? When should you change to `iterative`?
- What would happen if we remove `--skipCQR` from this command? Would this be a good idea if we wanted to apply corrections to shower shape and isolation variables?

## Plotting

You can now use your freshly produced NTuples and plot some of the variables.
For this, we provide a `plotter.py` script.
Please read through this script a bit and make sure you roughly understand what is happening.
Also check `configs/plot_settings.json`. This configuration file contains the settings for the plots and variables you will be plotting. Note that we implemented the possibility to plot ratios of variables, in this case for leading photon pT divided by the diphoton mass.
Then, execute the script with
```
python plotter.py ./configs/plot_settings.json ./NTuples ./plots
```
In case the Ntuplising did not work for you, you can use samples we provide in `/eos/cms/store/group/phys_higgs/cmshgg/tutorials/HiggsDNA_FinalFits_2024/HiggsDNA_part/04_base_processor/NTuples` instead. In that case, you need to change the input path when calling the plotter.

Now, check the newly created plots. Do they make sense to you? Also note the difference in the normalisation of the MC histogram between the two created plots.

Questions:
- Try extending the range of the plot of the invariant diphoton mass to values lower than 100 GeV. What do you observe? Can you explain your observation?
- Explain the shape of the `lead_pt/mass` plot. Where does it peak? Why is there a sharp edge around 1/3?
- Only include `tth` in the list of processes. Which differences do you observe? Can you explain them? 
- Choose your own variables and plot them! Just extend the `configs/plot_settings.json` according to your liking. You can identify the stored variables by adding `print(data_arr.fields)` at the start of the plotting variables.
- If you are more interested on the side of accessing remote files, you can try to access them from a specific site by changing the paths in the sample JSON as explained in the presentation. For example, you could specify a site for the data. Check https://cmsweb.cern.ch/das/request?instance=prod/global&input=site+dataset%3D%2FEGamma%2FRun2022C-16Dec2023-v1%2FNANOAOD to find possible sites that hold many of the files of the dataset.

Congratulations, you have finished Exercise 4!