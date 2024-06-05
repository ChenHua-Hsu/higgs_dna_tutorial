## Tutorial overview
The accompanying slides for this tutorial can be found attached to the [Indico page](https://indico.cern.ch/event/1398580/sessions/551110/#20240618).

In this tutorial we will build the statistical model for a simple analysis based on Run 3 data (2022 preEE). This corresponds to an integrated luminosity of 8 fb $^{-1}$. After the standard H$\rightarrow\gamma\gamma$ triggers and preselection are applied, events are categorised according to the lead/sublead photon $\eta$ and $R_9$. In total there are ten analysis categories:
```
EBEB_highR9highR9,EBEB_highR9lowR9,EBEB_lowR9highR9,EBEE_highR9highR9,EBEE_highR9lowR9,EBEE_lowR9highR9,EEEB_highR9highR9,EEEB_highR9lowR9,EEEB_lowR9highR9,EEEE_incl
```
We consider the contributions in these categories from both ggH and VBF to build the signal models. The background models are obtained directly from data using the discrete-profiling method. We will then learn how to construct a Higgs combine datacard with the relevant systematic uncertainty information, and eventually perform a likelihood scan to extract the rate of Higgs boson production.

This tutorial is split into five sections. You can follow the links for detailed instructions.

* [Trees2WS](./trees2ws): we will learn how to convert the ROOT tree output of HiggsDNA into a Final Fits compatible RooWorkspace.
* [Signal modeling](./signal_modeling): we will use the signal MC RooWorkspaces to build signal models.
* [Background modeling](./background_modeling): we will use the data RooWorkspaces to build the background models with the discrete-profiling method.
* [Datacard creation](./datacard): we will build a Combine datacard from the inputs.
* [Combine and plotting](./combine): we will convert the datacard into a RooWorkspace, perform fits and plot the output.

Enjoy!