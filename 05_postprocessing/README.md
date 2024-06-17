# Exercise 5: Postprocessing

As you experienced in the previous parts of the tutorial, the output of HiggsDNA is split in separate `.parquet` files, one for each chunk of data, for each sample in the analysis, and for each object systematic processed.
The amount of files tend to diverge when you run a full blown analysis, but fret not! HiggsDNA is giving you a set of dedicated tools to post-process these files and interface them to the  $H\rightarrow \gamma\gamma$ statistical analysis framework FlashGG_FinalFit.

The dedicated scripts needed to perform these step can be found in `HiggsDNA/scripts/postprocessing`, and are used to takle 3 tasks:
* Merge all the `.parquet` files into one big `.parquet` to rule them all. During this step one can also separate the events into categories. The output of this step consists in one `.parquet` file for each category of each sample of each object systematic variation.
* Convert the `merged.parquet` into ROOT trees. The output of this step consists in one `.root` file for each sample, that will contain different `TTrees` for categories and systematics. 
* Convert the `ROOT` trees into FinalFit compatible `RooWorkspace`s.

All the steps can be performed in one go using a nanny scrip (`prepare_output_file.py`) with a command more or less like this:
```
python3 prepare_output_file.py --input [path to HiggsDNA output dir] --merge --root --ws --syst --cats --varDict [path to variation json] --catDict [path to category json]
```
or the single steps can be performed by running the different modes one by one (`--merge`, `--root`, `--ws`) separately. Let's analyse these steps one by one.

## Merging Step

During this step the main script calls `merge_parquet.py` multiple times. The starting point is the output of HiggsDNA, i.e. `out_dir/sample_n/var/`. 
These directory must contain only `.parquet` files that have to be merged. The script will create a new directory called merged under `out_dir`, and if this directory already exists it will throw an error. When converting the data, that are usually split ine Eras the script will put them in a new directory and then merge again the output in a `.parquet` called `allData.parquet`.

Let's try to do a basic merging without any complication, as for the previous steps of the tutorial you should have a valid `higgs-dna` environment activated. First we copy the input that mimicks what HiggsDNA would give us if we ran the `base_workflow` with a couple of systyematics on the signal MC.
```
cd 05_postprocessing

cp -r /eos/cms/store/group/phys_higgs/cmshgg/tutorials/HiggsDNA_FinalFits_2024/HiggsDNA_part/05_postprocessing/signal/ 05_NTuples
```
Now we have a set of NTuples, if you look in the directory you just copied you'll se that there are some signal MC with different values of the Higgs mass and for each sample there are subdirectories containg the nominal NTuples and the systematically variated ones. 
```
ls -l 05_NTuples
ls -l 05_NTuples/ggh_M-125_preEE
```
Then we move to the postprocessing directory and run the merging.
```
cd ../HiggsDNA/scripts/postprocessing

python3 prepare_output_file.py --input ../../../05_postprocessing/05_NTuples --merge
```
If you now go back to the NTuple directory you will notice that the script has added a `merged` directory containing a single file per process. Feel free to inspect it to check the amount of events inside.
```
cd ../../../05_postprocessing/05_NTuples/merged
```
As mentioned before during this step the events can also be also split into categories according to the boundaries defined in the category json provided. An example of such dictionary is presented in the file `05_postprocessing/configs/category.json`. Have a look at this file and try to understand in which way we're about to categorise the events.

Now, let's try to re-run the previous step with the categorisation.
```
cd .. 
mv merged merged_untagged

cd ../../HiggsDNA/scripts/postprocessing

python3 prepare_output_file.py --input ../../../05_postprocessing/05_NTuples --merge --cats --catDict ../../../05_postprocessing/configs/category.json
```
You can now open the output files and check that the boundaries are correct. If you look in the same place as before you will see now multiple files, one for each category. Look in the `category.json` (if you haven't done it before) and check on which variable we're cutting. Then open one of the files with python:
```
cd ../../../05_postprocessing/05_NTuples/merged

python3 
$ > import awkward as ak
$ > events = ak.from_parquet("ggh_M-125_preEE/EBEB_merged.parquet")
$ > print(f"""boundaries for Id MVA:
         lead min:    {ak.min(events.lead_mvaID)}
         sublead min: {ak.min(events.sublead_mvaID)}
         lead max:    {ak.max(events.lead_mvaID)}
         sublead max: {ak.max(events.sublead_mvaID)}
     """)
$ > print(f"""boundaries for SC eta:
        lead eta min:    {ak.min(events.lead_superclusterEta)}
        sublead eta min: {ak.min(events.sublead_superclusterEta)}
        lead eta max:    {ak.max(events.lead_superclusterEta)}
        sublead eta max: {ak.max(events.sublead_superclusterEta)}
    """)
$ > exit()
```

Now try to reiterate the process splitting the eta categories according also to the lead and sublead photon `r9`: 
* split `EBEB` in `EBEB_highR9highR9`, `EBEB_highR9lowR9` and `EBEB_lowR9highR9` (bounds lead and sublead [0.5, 0.85]),
* split `EBEE` in `EBEE_highR9highR9`, `EBEE_highR9lowR9` and `EBEE_lowR9highR9` (bounds lead [0.5, 0.85], bounds sublead [0.5, 0.9]),
* split `EEEB` in `EEEB_highR9highR9`, `EEEB_highR9lowR9` and `EEEB_lowR9highR9` (bounds lead [0.5, 0.85], bounds sublead [0.5, 0.9]),
* rename `EEEE` in `EEEE_incl`, without changing the boundaries.

During this step we can also include the treatment of the systematic variations. As you probably noticed before, in each process directory there are multiple subdirs: `nominal`, `Scale_down`, `Scale_up` etc. The `nominal` directory contains the NTuples with the central values of the corrections and the weight systematics variation branches, the other directories instead contain NTuples with variations of the object systematics. This second type of systematics applies correction and variations directly to some object in the analysis (e.g. $p_T$ of the photons) resulting in a different set of events passing the selection. Therefore in this case we end up with a different NTuple altogether.

To treat all the variations properly you have to activate the `--syst` option of the merging script and provide a `.json` containing the naming scheme for the object systematics. Have a look at the example `variation.json` file provided in this section of the tutorial and then let's run the merging step one last time.

```
cd ..
rm -r merged

cd ../../HiggsDNA/scripts/postprocessing

python3 prepare_output_file.py --input ../../../05_postprocessing/05_NTuples --merge --cats --syst --catDict ../../../05_postprocessing/configs/category.json --varDict ../../../05_postprocessing/configs/variation.json
```

Another feature of the merging step worth noting is the normalisation of the weights of the events. HiggsDNA saves some metaconditions containing the sum of the generator weights of the full sample in the output, these are necesary to normalise the events to the value of `efficiancy x acceptance` of the selection for each process. FlashggFinalFit takes care afterwards of adding the values of $\sigma$, luminosity and $BR$. This feature can be deactivate rnning the same commands as above with the additional option `--skip-normalisation`.

## Root Step

The next step toward porting our HiggsDNA NTuples with FlashggFinalFit is to convert our freshly made `.parquet` trees into ROOT `TTrees`. To do so we run again the same script with the `--root` option. In this way we will call the other auxiliary script `convert_parquet_to_root.py` in a much similar way to what we did before with `merge_parquet.py`. 

The treatment of category and systematics works in the same way as for the merging, one has to use the `--syst` and `--cats` arguments building on the output of the previous step. A few furter technicalities has to be taken into account: in the `convert_parquet_to_root.py` script there is a dictionary called `outfiles` that contains the name of the output root file that will be created according to the process type which, if the postprocessing workflow is run using the main script, is defined according to what is contained in the `process_dict` of `prepare_output_file.py`.

An example of both is shown here:
```
# from prepare_output_file.py line 159

process_dict = {
    "GluGluHtoGG": "ggh",
    "VBFHtoGG": "vbf",
    "VHtoGG": "vh",
    "ttHtoGG": "tth",
    "GluGluHtoGG_M-120_preEE": "ggh_120",
    "GluGluHtoGG_M-120_postEE": "ggh_120",
    "GluGluHtoGG_M-125_preEE": "ggh_125",
    "GluGluHtoGG_M-125_postEE": "ggh_125",
    "GluGluHtoGG_M-130_preEE": "ggh_130",
    "GluGluHtoGG_M-130_postEE": "ggh_130",
    "VBFHtoGG_M-120_preEE": "vbf_120",
    "VBFHtoGG_M-120_postEE": "vbf_120",
    "VBFHtoGG_M-125_preEE": "vbf_125",
    "VBFHtoGG_M-125_postEE": "vbf_125",
    "VBFHtoGG_M-130_preEE": "vbf_130",
    "VBFHtoGG_M-130_postEE": "vbf_130"
    .
    .
    .
}

# from conver_parquet_to_root.py line 69

outfiles = {
    .
    .
    .
    "ggh_125": target_path.replace(
        "merged.root", "output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8.root"
    ),
    "ggh_120": target_path.replace(
        "merged.root", "output_GluGluHToGG_M120_13TeV_amcatnloFXFX_pythia8.root"
    ),
    "ggh_130": target_path.replace(
        "merged.root", "output_GluGluHToGG_M130_13TeV_amcatnloFXFX_pythia8.root"
    ),
    "vbf": target_path.replace(
        "merged.root", "output_VBFHToGG_M125_13TeV_amcatnlo_pythia8.root"
    ),
    "vbf_125": target_path.replace(
        "merged.root", "output_VBFHToGG_M125_13TeV_amcatnlo_pythia8.root"
    ),
    "vbf_120": target_path.replace(
        "merged.root", "output_VBFHToGG_M120_13TeV_amcatnlo_pythia8.root"
    ),
    "vbf_130": target_path.replace(
        "merged.root", "output_VBFHToGG_M130_13TeV_amcatnlo_pythia8.root"
    ),
    .
    .
    .
}
```

Now, let's try to obtain some ROOT trees by running:
```
python3 prepare_output_file.py --input ../../../05_postprocessing/05_NTuples --root --cats --syst --catDict ../../../05_postprocessing/configs/category.json --varDict ../../../05_postprocessing/configs/variation.json
```

At this point we should have created a new directory next to the one with the merged output called `root` and containing a subdirectory with a ROOT file for each process. All the categories and systematic variations are stored as separate `TBranches` in order to be compatible with the input format of FlashggFinalFit.

We can try to open our output in different formats and perform a couple of checks to familiarise with their content. To do so you can use either the jupyter notebook (`investigations.ipynb`) or the equivalent python script (`investigations.py`). We will check the content of different weight branches, look into the normalisation buisness, and plot some distributions to understand the effect of different kinds of systematics. Make sure to return to the `05_postprocessing` directory after performing the `root` step.

## RooWorkspace creation

The last step to produce FinalFit friendly input is to convert our ROOT trees into a `RooWorkspace` object. This procedure is carried out using two scripts that are contained in FlashggFinalFit: `trees2ws.py` and `trees2ws_data.py`. We won't cover fully this step here because this will be a topic of the finalfits part of the tutorial, but in principle once you've setup a working FlashggFinalFit installation you can do this conversion automatically using the same procedure you've seen for the previous parts. We use the same command as before adding the `--ws` option and giving to the script information about where to find FinalFit (using the `--final_fit` option) and the configuration file that Tree2WS needs to set up the `RooWorkSpace` (using the option `--ws_config`). You can find an exaple configuration file in the Tree2WS part of the FinalFit tutorial.

To run the workspace creation (it will work only if you have already set up FinalFit) use:
```
python3 prepare_output_file.py --input ../../../05_postprocessing/05_NTuples --ws --cats --syst --final_fit <path/to/final_fit> --ws_config ../../../05_postprocessing/configs/tree2ws_config.py
```
