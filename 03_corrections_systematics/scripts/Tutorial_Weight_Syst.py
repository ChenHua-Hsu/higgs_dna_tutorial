import json
import os
import correctionlib
import logging
import numpy as np
import awkward as ak
from copy import deepcopy

logger = logging.getLogger(__name__)


def Tutorial_Weight(pt, events, year="2022postEE", is_correction=True):
    # for later unflattening:
    counts = ak.num(events.Photon.pt)
    _pt = ak.flatten(events.Photon.pt)
    
    json_file = os.path.join(os.path.dirname(__file__), "./tutorial_correction.json.gz")
    evaluator = correctionlib.CorrectionSet.from_file(json_file)["Tutorial_corr"]

    if is_correction:
        correction = evaluator.evaluate(_pt, "nominal")
        pt_corr = _pt + correction

        corrected_photons = deepcopy(events.Photon)
        pt_corr = ak.unflatten(pt_corr, counts)
        corrected_photons["pt"] = pt_corr
        events.Photon = corrected_photons
        return events
    else:
        correction_up = evaluator.evaluate(_pt, "up")
        correction_down = evaluator.evaluate(_pt, "down")

        corr_up_variation = _pt+correction_up
        corr_down_variation = _pt+correction_down

        return np.concatenate((corr_up_variation.to_numpy().reshape(-1,1), corr_down_variation.to_numpy().reshape(-1,1)), axis=1) * (ak.ones_like(_pt))[:, None]
