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
The $H \rightarrow \gamma\gamma$ Monte-Carlo (MC) trees used for the signal modeling are stored under `signal_2022preEE`, and the data trees used for the background modeling are stored under `data`. Please copy this directory:
```
cp -rs /eos/cms/store/group/phys_higgs/cmshgg/tutorials/HiggsDNA_FinalFits_2024/FinalFits_tutorial/inputs .
```
The `-s` option in the `cp` command means that we have created symbolic links to the files.

Let's begin by taking a look at the structure of the ROOT files. In `inputs/signal_2022preEE` you will see that we have six files which correspond to ggH and VBF production, each at three different mass points: 120, 125 and 130 GeV. Open up the `python3` interpreter and check the contents:
```
$ python3
>>> import ROOT
>>> f = ROOT.TFile("inputs/signal_2022preEE/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8.root")
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

<details>
<summary>You can also explore the workspace in the ROOT interpreter. Click here to see how.</summary>

```
$ root -b inputs/signal_2022preEE/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8.root 
root [1] .ls
TNetXNGFile**           root://eoscms.cern.ch//eos/cms/store/group/phys_higgs/cmshgg/tutorials/HiggsDNA_FinalFits_2024/FinalFits_tutorial/inputs/signal_2022preEE/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8.root
 TNetXNGFile*           root://eoscms.cern.ch//eos/cms/store/group/phys_higgs/cmshgg/tutorials/HiggsDNA_FinalFits_2024/FinalFits_tutorial/inputs/signal_2022preEE/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8.root
  KEY: TDirectoryFile   DiphotonTree;1  DiphotonTree
root [2] DiphotonTree->cd()
(bool) true
root [3] .ls
...
root [4] ggh_125_13TeV_EBEB_highR9highR9->Show(0)
...
```
</details>

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
python3 trees2ws.py --inputConfig config_tutorial.py --inputTreeFile inputs/signal_2022preEE/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8.root --inputMass 125 --productionMode ggh --year 2022preEE --doSystematics
```
This will convert the HiggsDNA ROOT TTrees into a Final Fits compatible RooWorkspace which can be found here: `inputs/signal_2022preEE/ws_GG2H/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8_GG2H.root`. The nominal trees are converted into `RooDataSets` with variables defined by the `mainVars` container, whilst the systematic-shifted trees are saved as `RooDataHists` with variables defined by the `systematicsVars` container. The input trees must abide by the naming structure described above for this step to work. 

For multiple input files, we can submit the jobs to condor using the `RunWSScripts.py` job configuration script:
```
python3 RunWSScripts.py --inputDir inputs/signal_2022preEE --inputConfig config_tutorial.py --year 2022preEE --mode trees2ws --modeOpts "--doSystematics" --batch condor --queue espresso --printOnly
```
The job submission files are stored in `outdir_test/trees2ws/jobs`. Remove the `--printOnly` option to submit the jobs. The output workspaces files will be stored in `inputs/signal_2022preEE/ws_{PROC}`.

If you'd like, you can instead run the jobs locally with the `--batch local` option:
```
python3 RunWSScripts.py --inputDir inputs/signal_2022preEE --inputConfig config_tutorial.py --year 2022preEE --mode trees2ws --modeOpts "--doSystematics" --batch local
```
The output files will end up in the same place: `inputs/signal_2022preEE/ws_{PROC}`.

## Converting to RooWorkspace files (data)
We also need to convert the data TTree to a RooWorkspace. We only have one file here so there is no need to submit to the batch system. You can run the folling command:
```
python3 trees2ws_data.py --inputConfig config_tutorial.py --inputTreeFile inputs/data/allData_2022preEE.root --applyMassCut --massCutRange 100,180
```
The output will be stored in `inputs/data/ws`. The last two options apply a cut on the diphoton mass to be between 100 and 180 GeV, as this was not applied upstream in HiggsDNA. 

## Exploring the RooWorkspaces
A lot of people think RooWorkspaces are black boxes... this is not the case. Let's first move the output of this section to a new directory:
```
cd inputs
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

<details>
<summary>Once again, we can use the ROOT interpreter if we fancy. Click here to see how.</summary>

```
$ root -b workspaces/signal_2022preEE/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8_GG2H.root 
root [1] .ls
TFile**         workspaces/signal_2022preEE/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8_GG2H.root
 TFile*         workspaces/signal_2022preEE/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8_GG2H.root
  KEY: TDirectoryFile   tagsDumper;1    tagsDumper
  KEY: TProcessID       ProcessID0;1    a8756544-23f6-11ef-9140-020fb9bcbeef
root [2] tagsDumper->cd()
(bool) true
root [3] .ls
TDirectoryFile*         tagsDumper      tagsDumper
 KEY: RooWorkspace      cms_hgg_13TeV;1 cms_hgg_13TeV
root [4] cms_hgg_13TeV->Print()
...
root [5] cms_hgg_13TeV->allVars().Print()
RooArgSet:: = (intLumi,CMS_hgg_mass,weight,dZ,weight_central,weight_PreselSFUp,weight_PS_ISRUp,weight_PileupDown,weight_PS_FSRUp,weight_PS_FSRDown,weight_ElectronVetoSFDown,weight_PreselSFDown,weight_TriggerSFDown,weight_PileupUp,weight_PS_ISRDown,weight_SF_photon_IDUp,weight_TriggerSFUp,weight_SF_photon_IDDown,weight_AlphaSDown,weight_ElectronVetoSFUp,weight_AlphaSUp,weight_nominal)
root [6] cms_hgg_13TeV->allVars().selectByName("weight_*")->Print()
RooArgSet::_selection = (weight_central,weight_PreselSFUp,weight_PS_ISRUp,weight_PileupDown,weight_PS_FSRUp,weight_PS_FSRDown,weight_ElectronVetoSFDown,weight_PreselSFDown,weight_TriggerSFDown,weight_PileupUp,weight_PS_ISRDown,weight_SF_photon_IDUp,weight_TriggerSFUp,weight_SF_photon_IDDown,weight_AlphaSDown,weight_ElectronVetoSFUp,weight_AlphaSUp,weight_nominal)
root [7] cms_hgg_13TeV->var("weight_PreselSFUp")->Print()
RooRealVar::weight_PreselSFUp = 0.631068  L(-999999 - 999999) B(1) 
root [8] cms_hgg_13TeV->data("ggh_125_13TeV_EBEB_highR9highR9")->Print()
RooDataSet::ggh_125_13TeV_EBEB_highR9highR9[CMS_hgg_mass,dZ,weight_central,weight_PreselSFUp,weight_PS_ISRUp,weight_PileupDown,weight_PS_FSRUp,weight_PS_FSRDown,weight_ElectronVetoSFDown,weight_PreselSFDown,weight_TriggerSFDown,weight_PileupUp,weight_PS_ISRDown,weight_SF_photon_IDUp,weight_TriggerSFUp,weight_SF_photon_IDDown,weight_AlphaSDown,weight_ElectronVetoSFUp,weight_AlphaSUp,weight_nominal,weight:weight] = 177149 entries (0.192413 weighted)
root [9] cms_hgg_13TeV->data("ggh_125_13TeV_EBEB_highR9highR9")->Print("v")
DataStore ggh_125_13TeV_EBEB_highR9highR9 (ggh_125_13TeV_EBEB_highR9highR9)
  Contains 177149 entries
  Observables: 
    1)               CMS_hgg_mass = 125.477  L(100 - 180) B(160)  "CMS_hgg_mass"
    2)                         dZ = 9.15527e-05  L(-20 - 20) B(40)  "dZ"
    3)             weight_central = 1.61796  L(-999999 - 999999) B(1)  "weight_central"
    4)          weight_PreselSFUp = 1.62514  L(-999999 - 999999) B(1)  "weight_PreselSFUp"
    5)            weight_PS_ISRUp = 1.66881  L(-999999 - 999999) B(1)  "weight_PS_ISRUp"
    6)          weight_PileupDown = 1.70855  L(-999999 - 999999) B(1)  "weight_PileupDown"
    7)            weight_PS_FSRUp = 2.11804  L(-999999 - 999999) B(1)  "weight_PS_FSRUp"
    8)          weight_PS_FSRDown = 0.624188  L(-999999 - 999999) B(1)  "weight_PS_FSRDown"
    9)  weight_ElectronVetoSFDown = 1.61407  L(-999999 - 999999) B(1)  "weight_ElectronVetoSFDown"
   10)        weight_PreselSFDown = 1.61078  L(-999999 - 999999) B(1)  "weight_PreselSFDown"
   11)       weight_TriggerSFDown = 1.61464  L(-999999 - 999999) B(1)  "weight_TriggerSFDown"
   12)            weight_PileupUp = 1.48183  L(-999999 - 999999) B(1)  "weight_PileupUp"
   13)          weight_PS_ISRDown = 1.54053  L(-999999 - 999999) B(1)  "weight_PS_ISRDown"
   14)      weight_SF_photon_IDUp = 1.64629  L(-999999 - 999999) B(1)  "weight_SF_photon_IDUp"
   15)         weight_TriggerSFUp = 1.61949  L(-999999 - 999999) B(1)  "weight_TriggerSFUp"
   16)    weight_SF_photon_IDDown = 1.58978  L(-999999 - 999999) B(1)  "weight_SF_photon_IDDown"
   17)          weight_AlphaSDown = 1.49096  L(-999999 - 999999) B(1)  "weight_AlphaSDown"
   18)    weight_ElectronVetoSFUp = 1.62185  L(-999999 - 999999) B(1)  "weight_ElectronVetoSFUp"
   19)            weight_AlphaSUp = 1.76075  L(-999999 - 999999) B(1)  "weight_AlphaSUp"
   20)             weight_nominal = -339.411  L(-999999 - 999999) B(1)  "weight_nominal"
  Dataset variable "weight" is interpreted as the event weight
```
</details>