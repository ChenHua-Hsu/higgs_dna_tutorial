import gzip
import correctionlib.schemav2 as cs
import rich

corr = cs.Correction(
    name="Tutorial_corr",
    version=0,
    inputs=[
        cs.Variable(
            name="pt", type="real", description="photon pt"
        ),
        cs.Variable(
            name="syst", type="string", description="systematic could be nominal, up, down"
        )
    ],
    output=cs.Variable(
        name="weight", type="real", description="not weight, it's the shift on the photon pt"
    ),
    data=cs.Category(
        nodetype="category",
        input="syst",
        content=[
            # up: nominal scale factor + shift values
            cs.CategoryItem(
                key="up",
                value=cs.Binning(
                    nodetype="binning",
                    input="pt",
                    edges=[0, 60, 90, 120, 180],
                    content=[5, 10, 15, 20],
                    flow=1.5,
                ),
            ),
            # nominal scale factor
            cs.CategoryItem(
                key="nominal",
                value=cs.Binning(
                    nodetype="binning",
                    input="pt",
                    edges=[0, 60, 90, 120, 180],
                    content=[5, 5, 10, 10],
                    flow=1.0,
                ),
            ),
            # down: nominal scale factor + shift values
            cs.CategoryItem(
                key="down",
                value=cs.Binning(
                    nodetype="binning",
                    input="pt",
                    edges=[0, 60, 90, 120, 180],
                    content=[-5, -10, -15, -20],
                    flow=0.5,
                ),
            ),
        ],
        # default is same as nominal
        default=cs.Binning(
            nodetype="binning",
            input="pt",
            edges=[0, 60, 90, 120, 180],
            content=[5, 5, 10, 20],
            flow=1,
        ),
    )
)

cset = cs.CorrectionSet(
    schema_version=2,
    description="Tutorial photon pt correction, for leading photon pt in [0, 60, 90, 120, 180] GeV, the photon pt are corrected with [5, 5, 10, 10] GeV",
    corrections=[
        corr,
    ],
)
rich.print(cset)

# save json
with gzip.open("tutorial_correction.json.gz", "wt") as fout:
    fout.write(cset.json(exclude_unset=True))

