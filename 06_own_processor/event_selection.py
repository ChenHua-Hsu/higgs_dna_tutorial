import awkward as ak

def select_events_VBF_enriched(NTuples_path):

    # Load the parquet files
    events = ak.from_parquet(NTuples_path)

    # Select events according to VBF enriched criteria

    # Select the events with atleas two jets. Remember you have filled events with no dijet combination with -999.0.
    has_two_jets = (events.dijet_pt > -1) # This shuold automatically selection events with atleast two jets

    dijet_delta_eta_cut = (events.dijet_delta_eta > 3.5)

    dijet_mass_cut = (events.dijet_mass > 200)

    events = events[
        has_two_jets
        & dijet_delta_eta_cut
        & dijet_mass_cut
    ]

    return events