# FinalFits tutorial

## Installation
Let's begin by setting up the FinalFits package in a CMSSW build. To avoid conflicts with the HiggsDNA environment you will want to deactivate the micromambda environment.
```
conda deactivate
```

The [FinalFits package](https://github.com/cms-analysis/flashggFinalFit/tree/dev_higgsdnafinalfit) is built on top of the [Combine](http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/) and [CombineTools](https://github.com/cms-analysis/CombineHarvester/tree/main/CombineTools) packages. We will use the recent EL9-compatible `Combine` branch in `CMSSW_14_1_0_pre4`, which is based on ROOT 6.30. The installation instructions are provided below. We recommend you to work in your EOS area (`/eos/user/a/abc`) on lxplus. Many plots will be produced throughout the tutorial and we leave it up to the participants for the best way to view the plots (vscode, EOS web area, scp to local, ...).
```
cd 07_FinalFits
export SCRAM_ARCH=el9_amd64_gcc12
cmsrel CMSSW_14_1_0_pre4
cd CMSSW_14_1_0_pre4/src
cmsenv

COMBINE_TAG=07b56c67ba6e4304b42c3a6cdba710d59c719192
COMBINEHARVESTER_TAG=94017ba5a3a657f7b88669b1a525b19d34ea41a2
FINALFIT_TAG=higgsdnafinalfit

# Install Combine with the latest EL9 compatible branch
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit && git fetch origin ${COMBINE_TAG} && git checkout ${COMBINE_TAG}

# Install CombineTools in CombineHarvester
cd ${CMSSW_BASE}/src
bash <(curl -s https://raw.githubusercontent.com/cms-analysis/CombineHarvester/${COMBINEHARVESTER_TAG}/CombineTools/scripts/sparse-checkout-https.sh)
cd CombineHarvester && git fetch origin ${COMBINEHARVESTER_TAG} && git checkout ${COMBINEHARVESTER_TAG}

# Compile libraries
cd ${CMSSW_BASE}/src
cmsenv
scram b clean
scram b -j 16

# Install Final Fit package
git clone -b $FINALFIT_TAG https://github.com/cms-analysis/flashggFinalFit.git
cd flashggFinalFit/
source setup.sh
```

Ignore the compilation warnings from the CombineTools package. These will be fixed in the near future. 

In every new shell/terminal, we must go to the base directory of the flashggFinalFit repository and reactivate the environment with:
```
source setup.sh
```

## Pre-tutorial work
The Combine [parametric exercise](http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/tutorial2023/parametric_exercise/) is based on a H$\rightarrow\gamma\gamma$ analysis, and closely follows the steps which Final Fits performs under-the-hood. We strongly advise participants to go through the parametric exericse beforehand. This will help better understand the material in this tutorial. You can use the branch of Combine which you have just installed. 