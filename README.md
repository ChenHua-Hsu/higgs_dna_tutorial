# HiggsDNA and FinalFits Tutorial June 2024

`HiggsDNA` and `FinalFits` run on any contemporary scientific linux machine. You are free to follow the tutorial from the computing infrastructure of your choice, but we highly recommend that you use `lxplus` (v9!) since we designed and tested the tutorial on `lxplus`.

Please make sure that you have deposited a valid ssh key for your CERN Gitlab account and that your private key is also present in the `~/.ssh/` directory and the host `gitlab.cern.ch` is entered in the `~/.ssh/config` file. For more information, consult https://docs.gitlab.com/ee/user/ssh.html.

This repository contains submodules.
Please clone the repository with the `--recurse-submodules` command to ensure that the `HiggsDNA` submodule is cloned appropriately.
We recommend that you clone this repository in your `eos` space to avoid reaching your quota in the `afs` home directory.
You can reach your area at `/eos/user/<first_letter_of_your_CERN_username>/<your_CERN_username>/`.
For more information on the personal `eos` area, also known as CERNBox, please refer to https://cern.service-now.com/service-portal?id=service_element&name=CERNBox-Service.

If you are happy with the chosen location, execute the following command:
```
git clone --recurse-submodules ssh://git@gitlab.cern.ch:7999/jspah/higgsdna_finalfits_tutorial_24.git
```

## Connecting via VSCode

Of course, you can follow the tutorial however you want.
In the most basic setup, you can plainly use the shell and work with `nano` or `vi` and then `scp` any plots that you want to view.
For reasons of convenience, we recommend you to use `VSCode`, however.
This is a modern editor with powerful extensions that allows you to view plots and edit code almost effortlessly and combines an `sftp` browser and terminal sessions.

To set up VSCode, download it from the official website https://code.visualstudio.com/download for your respective operating system.

Then, install the `Remote - SSH` extension. For more extensive information, see https://code.visualstudio.com/docs/remote/ssh, we just describe the basic setup steps here.

In the left-most column of VSCode, you should see a new icon now, a monitor with an ssh button at the bottom right. Click on it and you see the ssh overview. Mouse-over the `SSH` field in the `REMOTES (TUNNELS/SSH)` category, click on the gear symbol and check your `config`. Make sure that it includes an entry for `lxplus`, e.g.,

```
Host lxplus
  HostName lxplus.cern.ch
  User <your_CERN_username>
  ForwardX11 yes
  ServerAliveInterval 60
  ServerAliveCountMax 30
```

You can then try to connect to `lxplus` if you expand the options in the `SSH` field. If that worked, you can even open a specific directory (we recommend that you work in your CERNbox `eos` area for this tutorial) in VSCode! Make sure to explore further extensions like a PDF browser or linters for `bash` and `python` to make your life easier.

Note that `VSCode` is known to have some weird behaviour from time to time with `lxplus` due to the way the CERN computing infrastructure is set up. We recommend following the tips & tricks below for a smoother experience.

### Configure the VScode server installation path
When you first log in to lxplus with VSCode, it will attempt to install a server on lxplus which it requires for `Remote - SSH` to work. By default, the installation path is the home directory (`~/`). If there is not enough space there to install the server, this can cause issues. We therefore recommend that you configure the installation path to somewhere else, like on your afs workspace (if you have one), or on eos.

To do this, go to File -> Preferences -> Settings and search for `remote.SSH.serverInstallPath`. Click `Add item` and type `lxplus.cern.ch` for the key, and your path, e.g. `/eos/user/s/jsmith` as the value. 

### Set a longer connection timeout 
If your log-in process takes too long, your connection will timeout. Sometimes, lxplus is just slow and we just need to wait a little longer. To save yourself from getting in an infinite timeout loop, set a longer timeout.

To do this, go to File -> Preferences -> Settings and search for `remote.SSH.remote.SSH.connectTimeout`. Set the number to something higher, e.g. 180.

### Set remote platform
This option tells vscode what type of operating system the ssh server is running. This may or may not help but it seems like a sensible thing to set.

To do this, go to File -> Preferences -> Settings and search for `remote.SSH.remotePlatform`. Click `Add item` and type `lxplus.cern.ch` for the key, and `linux` as the value. 

### Reinstalling the VSCode server
Sometimes the trick is to simply reinstall the vscode server. 

To do this, login to lxplus via a terminal or other means, and delete the server directory. By default, the server is installed in your home directory, so you would run:
```
rm -r ~/.vscode-server/
```
but if you have changed the server installation path, you'll have to look there instead.

### Alternatives 
If `VSCode` does not work for you or you do not like it, you can also consider the alternatives `MobaXterm` for Windows (https://mobaxterm.mobatek.net) and `PyCharm` for all systems (https://www.jetbrains.com/de-de/pycharm/).

## HiggsDNA Part

### Setting up your working environment

Please follow the instructions outlined in the `README.md` in the `00_HiggsDNA_setup` subdirectory to set up and test your HiggsDNA installation.

## FinalFits Part

Please follow the instructions outlined in the `README.md` in the `07_FinalFits` subdirectory to set up and test your Final Fits installation.