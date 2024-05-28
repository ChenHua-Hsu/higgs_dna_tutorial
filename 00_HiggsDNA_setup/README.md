# Installation instructions for HiggsDNA

The `HiggsDNA` framework is provided as a submodule in this tutorial repository.

General installation instructions are available at https://higgs-dna.readthedocs.io/en/latest/installation.html.

## Setting up the environment

For this tutorial, we propose two main options, which are already outlined at the above link, to set up your software environment for HiggsDNA.
The two options are using a micromamba environment (preferred) or using a docker image (alternative).

If you already have a working environment to run HiggsDNA in, you can skip this step and go straight to the "Installing HiggsDNA" step.

### Micromamba environment

If you already have a working micromamba installation on lxplus, skip straight ahead to the Section "Setting up the HiggsDNA conda environment with micromamba".

#### Setting up micromamba

<add motivation for micromamba compared to conda>

Follow the instruction for the automatic install provided at https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html#automatic-install.
This means: Execute

```
"${SHELL}" <(curl -L micro.mamba.pm/install.sh)
```

in the root directory of the tutorial repository.
He will ask you a serious of questions to determine your preferred setup.
Please specify a location in `eos` for the micromamba prefix as it can take up quite some space and the quota of the home directory is limited on lxplus.
The binary folder can be in your home as it does not take up a lot of space.
For these example instructions, we used `./micromamba_dir` in the root directory of the repository.
Please also answer `Y` when prompted for `Init shell` and `Configure conda-forge`.
If this was successful, you will receive some printout about appending lines to your `~/.bashrc`, this is intended. Please use a clean shell now or run

```
source ~/.bashrc
```

in the current shell.

Test if `micromamba` is available now by running

```
micromamba --version
```

and check if this command returns the version without an error.

#### Setting up the HiggsDNA conda environment with micromamba

In the root directory of this repository, install the conda environment.
Note that this might take a while depending on the occupancy of the lxplus node.
Make sure to either do this in the background while you are working on other things to keep the ssh session alive or execute the commands in a `tmux` session to keep them running even when you leave your desk.
Note that `tmux` sessions close by default if you log out on lxplus9.
If you want to keep them alive, run the setup on lxplus8.

```
micromamba env create --prefix micromamba_dir/envs/higgs-dna -f HiggsDNA/environment.yml
```

You have to confirm the installation with `Y` after the initial collection of packages from the `conda-forge` channel.
Note that we install the environment in a a different location compared to the default (which would be in your home) as disk space in the home directory is a scarce ressource on lxplus. 

After the installation has finished, test it. You can find the expected output below.
```
(base) [jspah@lxplus903 higgsdna_finalfits_tutorial_24]$ micromamba activate higgs-dna 
(higgs-dna) [jspah@lxplus903 higgsdna_finalfits_tutorial_24]$ python
Python 3.10.14 | packaged by conda-forge | (main, Mar 20 2024, 12:45:18) [GCC 12.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import coffea
>>> coffea.__version__
'0.7.22'
```

### Docker image

TODO: FINISH THIS SECTION

First, create the directory to store the apptainer cache:

```
mkdir apptainer-cache
```

```
SINGULARITY_CACHEDIR=./apptainer-cache apptainer shell --bind /afs -B /cvmfs/cms.cern.ch \
--bind /tmp --bind /eos/cms/ \
--env KRB5CCNAME=$KRB5CCNAME --bind /etc/sysconfig/ngbauth-submit \
docker://gitlab-registry.cern.ch/higgsdna-project/higgsdna:lxplus-c1fd1280
```

## Installing HiggsDNA

Note: If you have a working HiggsDNA setup already, you can skip straight ahead to the validation of the installation, of course.
Regardless whether you use the classical `conda` environment or the alternative setup with the image, you have to install `HiggsDNA`. Follow the commands below:

```
cd HiggsDNA
conda activate higgs-dna # alternatively, use the image
pip install -e .[dev]
```

Validate your installation afterwards by checking the `help` output of our main steering script:

```
python scripts/run_analysis.py --help
````

Also check if all the unit tests pass without errors (warnings are ok):

```
pytest
```

If that worked, you are all set from the HiggsDNA side!