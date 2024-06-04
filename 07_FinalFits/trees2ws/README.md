# Trees2WS
In this section, we will learn how to convert the HiggsDNA output into RooWorkspace files ready for Final Fits. Move to the Trees2WS directory:
```
cd $CMSSW_BASE/src/flashggFinalFit/Trees2WS
```

## Exploring the ROOT TTrees
The input trees are stored in:
```
/eos/cms/store/group/phys_higgs/cmshgg/tutorials/HiggsDNA_FinalFits_2024/FinalFits_tutorial/inputs
```
The $H \rightarrow \gamma\gamma$ Monte-Carlo (MC) trees used for the signal modeling are stored under `signal_2022preEE`, and the data trees used for the background modeling are stored under `data`. Please copy the files under the same directory structure to a local eos space:
```
# For example (change to your own!)
LOCAL_EOS_AREA=/eos/user/j/jlangfor/icrf/hgg/FinalFitsTutorial/higgsdna_finalfits_tutorial_24

cp -rp /eos/cms/store/group/phys_higgs/cmshgg/tutorials/HiggsDNA_FinalFits_2024/FinalFits_tutorial/inputs $LOCAL_EOS_AREA
```

Let's begin by taking a look at the structure of the ROOT files. In `inputs/signal_2022preEE` you will see that we have six files which correspond to ggH and VBF production, each at three different mass points: 120, 125 and 130 GeV. Open up the `python3` interpreter and check the contents:
```
$ python3
>>> import ROOT
>>> f = ROOT.TFile("output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8.root")
>>> f.ls()
TFile**		output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8.root	
 TFile*		output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8.root	
  KEY: TDirectoryFile	DiphotonTree;1	DiphotonTree
>>> f.cd("DiphotonTree")
>>> f.ls()
```
You will see there are a number of trees with the naming structure: `{prod}_{mass}_13TeV_{cat}`. Ignore the 13 TeV, these are indeed Run 3 samples and this should be updated to 13p6TeV. The `{cat}` suffix identifies the analysis category. So we have one nominal tree for each production mode times category combination. In this tutorial example we have ten analysis categories which are defined by the eta and R9 of the lead/sublead photon:
```
EBEB_highR9highR9,EBEB_highR9lowR9,EBEB_lowR9highR9,EBEE_highR9highR9,EBEE_highR9lowR9,EBEE_lowR9highR9,EEEB_highR9highR9,EEEB_highR9lowR9,EEEB_lowR9highR9,EEEE_incl
```
You can check the contents of one of the trees by printing out the values for the first entry e.g.:
```
>>> t = f.Get("DiphotonTree/ggh_125_13TeV_EBEB_highR9highR9")
>>> t.Show(0)
```
These trees contain a lot of information about the events, most of which we do not need for Final Fits. In the Trees2WS step we will skim everything from the trees except the reconstructed mass (`CMS_hgg_mass`), the difference in the z-coordinate between the reconstructed and true vertex, the event weight (`weight`), and the systematic-varied weights e.g. `weight_AlphaSUp/weight_AlphaSDown`.

You will also see there are a number of trees with the naming structure: `{prod}_{mass}_13TeV_{cat}_{syst}Up01Sigma` and `{prod}_{mass}_13TeV_{cat}_{syst}Down01Sigma`, which correspond to the systematic-varied datasets e.g. after applying the scale and smearing systematic uncertainty variations. As the events in these cases can shift around categories then we require separate trees.

## Converting to RooWorkspace files (signal)
Final Fits (in its current state) takes RooWorkspaces as input into the signal modeling, background modeling and datacard creation steps. Therefore we must convert the TTree files into RooWorkspaces.

The `trees2ws.py` script is used to convert the signal MC files. Each nominal TTree is converted into a `RooDataSet`, whilst the systematics-shifted TTrees are saved as a `RooDataHist`. The options for the converter are steered by an input `config.py` file, e.g. in `config_tutorial.py`:
```
# Input config file for running trees2ws

trees2wsCfg = {

  # Name of RooDirectory storing input tree
  'inputTreeDir':'DiphotonTree',

  # Variables to be added to dataframe: use wildcard * for common strings
  'mainVars':["CMS_hgg_mass","weight","dZ","weight_*"], # Var for the nominal RooDataSets
  'dataVars':["CMS_hgg_mass","weight"], # Vars to be added for data
  'stxsVar':'',
  'systematicsVars':["CMS_hgg_mass","weight"], # Variables to add to sytematic RooDataHists
  'theoryWeightContainers':{},

  # List of systematics: use string YEAR for year-dependent systematics
  'systematics':["Scale","Smearing"],

  # Analysis categories: python list of cats or use 'auto' to extract from input tree
  'cats':'auto'

}
```
Each variable specified in the `Vars` containers must be a separate branch in the input ROOT TTree. This config has specified to save the `CMS_hgg_mass`, `dZ`, nominal `weight` and all systematic-varied weights (using the `weight_*` wildcard) from the nominal signal datasets, whilst only the `CMS_hgg_mass` and nominal `weight` are stored for the systematic-varied trees. The analysis categories are extracted automatically using `'cats':'auto'`, but can be specified manually if needed. You can ignore the other fields for now.

Let's run the `trees2ws.py script over one of the files using this configuration:
```
PATH_TO_INPUTS="Add path to inputs here"

python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile $PATH_TO_INPUTS/signal_2022preEE/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8.root --inputMass 125 --productionMode ggh --year 2022preEE --doSystematics
```
This will convert the HiggsDNA ROOT TTrees into Final Fits compatible RooWorkspaces. The nominal trees are converted into `RooDataSets` with variables defined by the `mainVars` container, whilst the systematic-shifted trees are saved as `RooDataHists` with variables defined by the `systematicsVars` container. The input trees must abide by the naming structure described above for this step to work.

For multiple input files, we can submit the jobs to condor using the `RunWSScripts.py` job configuration script:
```
python3 RunWSScripts.py --inputDir $PATH_TO_INPUTS/signal_2022preEE --inputConfig config_tutorial.py --year 2022preEE --mode trees2ws --modeOpts "--doSystematics" --batch condor --queue espresso --printOnly
```
The job submission files are stored in `outdir_test/trees2ws/jobs`. Remove the `--printOnly` option to submit the jobs. The output workspaces files will be stored in `$PATH_TO_INPUTS/signal_2022preEE/ws_{PROC}`.

## Converting to RooWorkspace files (data)
We also need to convert the data TTree to a RooWorkspace. We only have one file here so there is no need to submit to the batch system. You can run the folling command:
```
python3 trees2ws_data.py --inputConfig config_tutorial.py --inputTreeFile ${PATH_TO_INPUTS}/data/allData_2022preEE.root --applyMassCut --massCutRange 100,180
```
The output will be stored in `$PATH_TO_INPUTS/data/ws`. The last two options apply a cut on the diphoton mass to be between 100 and 180 GeV, as this was not applied upstream in HiggsDNA. 

## Exploring the RooWorkspaces
A lot of people think RooWorkspaces are black boxes... this is not the case. Let's first move the output of this section to a new directory:
```
cd ${PATH_TO_INPUTS}
mkdir -p workspaces/data workspaces/signal_2022preEE

mv signal_2022preEE/ws_*/*.root workspaces/signal_2022preEE/
mv data/ws/*.root workspaces/data/

ls -Rf workspaces
```
We can open a workspace in the python interpreter and look around:
```
$ python3
>>> import ROOT
>>> f = ROOT.TFile("workspaces/signal_2022preEE/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8_GG2H.root")
>>> f.ls()
>>> f.cd("tagsDumper")
>>> f.ls()
>>> w = f.Get("tagsDumper/cms_hgg_13TeV")

# Print workspace contents
>>> w.Print()

# Print list of variables in the workspace
>>> w.allVars().Print()
>>> w.allVars().selectByName("weight_*").Print()

# Print variable information
>>> w.var("weight_PreselSFUp").Print()

# Print dataset information
>>> w.data("ggh_125_13TeV_EBEB_highR9highR9").Print()
# And in verbose setting
>>> w.data("ggh_125_13TeV_EBEB_highR9highR9").Print("v")

# Get event from dataset
>>> p = w.data("ggh_125_13TeV_EBEB_highR9highR9").get(123)
# Extract mass value
>>> p.getRealValue("CMS_hgg_mass")
# Event weight
>>> w.data("ggh_125_13TeV_EBEB_highR9highR9").weight()
```
There's plenty more commands to explore the RooWorkspace which are described in the [ROOT docs](https://root.cern.ch/doc/master/classRooWorkspace.html). This can be a very useful tool for debugging the fits if something doesn't look right. 



