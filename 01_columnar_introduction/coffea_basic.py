# cell 1

import numpy as np
import awkward as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema

fname = "/eos/cms/store/group/phys_higgs/cmshgg/tutorials/HiggsDNA_FinalFits_2024/HiggsDNA_part/04_base_processor/ggh_M-125_preEE/5d677ef6-111a-428f-a78c-7ae0f68fd140.root"

events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema).events()

# cell 2

print(events.fields)

print(events.Photon.fields)


# cell 3

print(ak.to_list(events.Photon.pt[:3]))

# cell 4

photons = events.Photon

# cell 5

count_number_of_photons = ak.num(photons,axis=1)

# cell 6

print(ak.to_list(count_number_of_photons[19202:19210]))

# cell 7

photons_masked = photons.mask[count_number_of_photons > 1]

# cell 8

print(ak.to_list(photons_masked.pt[19202:19210]))

# cell 9

photons_masked = photons_masked.mask[
    (photons_masked.pt[:,0] > 35) &
    (photons_masked.pt[:,1] > 25)
]

# cell 10

total_selection = ak.fill_none(
    ak.num(photons_masked,axis=1) > 0,
    False
)

photons_selected = photons_masked[total_selection]

# cell 11

# print("\n",
#     "Length of photons:", len(photons), "\n",
#     "Length of photons_masked:", len(photons_masked), "\n",
#     "Length of photons_selected:", len(photons_selected)     
# )

# cell 12

photons_selected["charge"] = ak.zeros_like(photons_selected.pt)

diphoton_pairs = ak.combinations(photons_selected, 2, fields=["lead", "sublead"])

# cell 13

# print(ak.to_list(diphoton_pairs.lead.pt[19202:19210]))

# cell 14

diphotons = diphoton_pairs.lead+diphoton_pairs.sublead

# cell 15

print(diphotons.mass[:,0])

# cell 16

import hist
from hist import Hist

# define the histogram
h = (
    Hist.new.Reg(100, 100, 150, overflow=False, underflow=False, name=r"m$_{\gamma \gamma}$ [GeV]")
    .Weight()
)

# fill diphoton mass
h.fill(diphotons.mass[:,0])

# cell 17

print(h)

# cell 18

import mplhep as hep
import matplotlib.pyplot as plt

hep.style.use(hep.style.CMS)

f, ax = plt.subplots(figsize=(10,10))

ax.set_ylabel("Count")
h.plot(ax=ax,label="ggH")

hep.cms.label("Preliminary",loc=0,com=13.6)

plt.legend()
plt.savefig(f"ggH.png", bbox_inches="tight")

# cell 19

from coffea import processor

class MyProcessor(processor.ProcessorABC):
    def __init__(self):
        pass


    def process(self, events):
        dataset = events.metadata["dataset"]

        # define the histogram
        results={}
        results[dataset]={
            "count": len(events)
        }
            
        h = (
            Hist.new.StrCat([], growth=True, name="dataset", label="Primary dataset")
            .Reg(100, 100, 150, overflow=False, underflow=False, name="x", label = r"m$_{\gamma \gamma}$ [GeV]")
            .Weight()
        )

        # get photons
        photons = events.Photon


        # add selections
        count_number_of_photons = ak.num(photons, axis=1)

        photons_masked = photons.mask[count_number_of_photons > 1]
        photons_masked = photons_masked.mask[
            (photons_masked.pt[:,0] > 35) &
            (photons_masked.pt[:,1] > 25)
        ]

        # save only the events pass the selections
        total_selection = ak.fill_none(
            ak.num(photons_masked,axis=1) > 0,
            False
        )

        photons_selected = photons_masked[total_selection]

        # make the diphoton pair combinations
        photons_selected["charge"] = ak.zeros_like(photons_selected.pt)
        diphoton_pairs = ak.combinations(photons_selected, 2, fields=["lead", "sublead"])

        # diphoton four-momentum
        diphotons = diphoton_pairs.lead+diphoton_pairs.sublead

        h.fill(dataset=dataset,x=diphotons.mass[:,0])


        results["mass"] = h
        return results

    def postprocess(self, accumulant):
        pass

# cell 20

sample_dict = {
    "ggH":[
        "/eos/cms/store/group/phys_higgs/cmshgg/tutorials/HiggsDNA_FinalFits_2024/HiggsDNA_part/04_base_processor/ggh_M-125_preEE/5d677ef6-111a-428f-a78c-7ae0f68fd140.root"
    ],
    "DY": [
        "/eos/cms/store/group/phys_higgs/cmshgg/tutorials/HiggsDNA_FinalFits_2024/HiggsDNA_part/02_03_TnP/DY/00b15860-be57-4739-af70-48a73faa0161.root"
    ]
}

# cell 21

run = processor.Runner(
    # executor=processor.IterativeExecutor(),
    executor=processor.FuturesExecutor(workers=4), # user 4 cores
    schema=NanoAODSchema
)

results = run(
    sample_dict,
    treename="Events",
    processor_instance=MyProcessor(),
)

# cell 22

print(results)

# cell 23

import mplhep as hep
import matplotlib.pyplot as plt

hep.style.use(hep.style.CMS)

f, ax = plt.subplots(figsize=(10,10))

ax.set_ylabel("Count")
results["mass"][{"dataset":"ggH"}].plot(ax=ax,label="ggH")
results["mass"][{"dataset":"DY"}].plot(ax=ax,label="DY")

hep.cms.label("Preliminary",loc=0,com=13.6)

ax.set_yscale("log")
plt.legend()
plt.savefig(f"ggH_DY.png", bbox_inches="tight")

# cell 24

import numpy as np
import awkward as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema

fname = "/eos/cms/store/group/phys_higgs/cmshgg/tutorials/HiggsDNA_FinalFits_2024/HiggsDNA_part/01_intro/ggh_M-125_preEE/5d677ef6-111a-428f-a78c-7ae0f68fd140.root"
events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema).events()
photons = events.Photon

counts = ak.num(photons.pt)
unflatten_photons = ak.flatten(photons)

import correctionlib
evaluator = correctionlib.CorrectionSet.from_file("/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/EGM/2022_Summer22EE/photonSS.json.gz")["Smearing"]
rho = evaluator.evaluate("rho", unflatten_photons.eta, unflatten_photons.r9)
print("smearing scale: \n",rho)

rng = np.random.default_rng(seed=125)

smearing = rng.normal(loc=1., scale=rho)
unflatten_photons["pt_smeared"] = unflatten_photons.pt * smearing

photons = ak.unflatten(unflatten_photons,counts)

print("Photon pT: \n",ak.to_list(photons.pt[:3]))
print("Photon pT smeared: \n",ak.to_list(photons.pt_smeared[:3]))

