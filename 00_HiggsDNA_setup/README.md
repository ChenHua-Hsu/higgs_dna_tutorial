# Installation instructions for HiggsDNA

The `HiggsDNA` framework is provided as a submodule in this tutorial repository.

General installation instructions are available at https://higgs-dna.readthedocs.io/en/latest/installation.html.

## Setting up the environment

For this tutorial, we propose two main options, which are already outlined at the above link, to set up your software environment for HiggsDNA.
The two options are using a micromamba environment or using apptainer.
The tutorial has been set up and tested using the first approach, so we would recommend to give that a go first, although both approaches are valid.

If you already have a working environment to run HiggsDNA in, you can skip this step and go straight to the "Installing HiggsDNA" step.

### Micromamba environment

If you already have a working micromamba installation on lxplus, skip straight ahead to the Section "Setting up the HiggsDNA conda environment with micromamba".

#### Setting up micromamba

We suggest to use the `micromamba` software to install an environment for HiggsDNA to thrive in. It is a faster, standalone version of `conda`.

Follow the instruction for the automatic install provided at https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html#automatic-install.
This means: Execute

```
cd higgsdna_finalfits_tutorial_24
"${SHELL}" <(curl -L micro.mamba.pm/install.sh)
```

in the root directory of the tutorial repository.
He will ask you a serious of questions to determine your preferred setup. Please answer as follows:

```
Micromamba binary folder? [~/.local/bin] 
Init shell (bash)? [Y/n] Y
Configure conda-forge? [Y/n] Y
Configure conda-forge? [~/micromamba] /eos/user/home-<letter>/<username>/higgsdna_finalfits_tutorial_24/micromamba
```

We specify a location in `eos` for the micromamba prefix as it can take up quite some space and the quota of the home directory is limited on lxplus.
The binary folder can be in your home as it does not take up a lot of space.
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
cd HiggsDNA
micromamba env create --prefix /eos/user/<letter>/<username>/higgsdna_finalfits_tutorial_24/micromamba_dir/envs/higgs-dna -f environment.yml
```

You have to confirm the installation with `Y` after the initial collection of packages from the `conda-forge` channel.
Note that we install the environment in a a different location compared to the default (which would be in your home) as disk space in the home directory is a scarce ressource on lxplus.

After the installation has finished, test it.
You can find the expected output below.
```
(base) [jspah@lxplus903 higgsdna_finalfits_tutorial_24]$ micromamba activate higgs-dna 
(higgs-dna) [jspah@lxplus903 higgsdna_finalfits_tutorial_24]$ python
Python 3.10.14 | packaged by conda-forge | (main, Mar 20 2024, 12:45:18) [GCC 12.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import coffea
>>> coffea.__version__
'0.7.22'
```
Note: If everything went according to plan, `micromamba activate higgs-dna` is the correct command to activate your environment.
If it does not work, please carefully check the printout of `micromamba` after installing the environment.
There, he will say `To activate this environment, use:` and give you the exact command to use.

#### Setting up the jupyter notebook environment with micromamba

For some exercises, we are going to use python [`jupyter notebook`](https://jupyter.org/). So please also install the `ipykernel` and `jupyter` packages in your `higgs-dna` environment, i.e.,

```bash
# activate the `higgs-dna` if you haven't
micromamba activate higgs-dna
# install packages
micromamba install ipykernel jupyter -y
```

Then, please also check the **enviroment settings of the first exercise**: [01_columnar_introduction](01_columnar_introduction/README.md), and choose one of the methods of setting up the environment.

### Apptainer

`Apptainer` is another possibility if you do not want to use `micromamba` or it does not work for you.
You can always start a shell with an image of our latest build of HiggsDNA with
```
apptainer shell -B /eos/user/<letter>/<username>/<path_to_higgsdna_finalfits_tutorial_24> -B /afs -B /cvmfs/cms.cern.ch -B /tmp  -B /eos/cms/  -B /etc/sysconfig/ngbauth-submit -B ${XDG_RUNTIME_DIR}  --env KRB5CCNAME="FILE:${XDG_RUNTIME_DIR}/krb5cc" /cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/higgsdna-project/higgsdna:latest
```
This is a very lightweight method, but it is arguably not as flexible because you rely on the latest version. You can run HiggsDNA commands in this `apptainer` shell, so you can try to run
```
run_analysis.py --help
```
for example.
Note that `run_analysis.py` is invoked as an executable script and need not be found anywhere in your directory.
Because you mounted your tutorial directory with the `-B` argument, you can also execute plotting scripts (that we will use later in the tutorial) inside such a shell. If you also want to develop, you should also install HiggsDNA in editable mode, see the Section below for that.

## Installing HiggsDNA

Note: If you have a working HiggsDNA setup already, you can skip straight ahead to the validation of the installation, of course.
Regardless whether you use the classical `conda` environment or the alternative setup with the image, you have to install `HiggsDNA`. Follow the commands below:

```
cd HiggsDNA
micromamba activate /eos/home-<letter>/<username>/higgsdna_finalfits_tutorial_24/micromamba_dir/envs/higgs-dna # alternatively, use the image (or correct the path if it differs).
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

NB: With the apptainer setup, tests can fail due to issues with xgboost, as explained in https://higgs-dna.readthedocs.io/en/latest/installation.html#docker-singularity. You do not need to worry about that.