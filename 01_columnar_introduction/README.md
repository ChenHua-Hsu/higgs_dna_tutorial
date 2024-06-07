# Setting up the environment

In this section, we will briefly look at columnar operation via [coffea](https://coffeateam.github.io/coffea/index.html) package.

We recommend the use of a **notebook** for interactivity. This makes it easier to visualize the results obtained at each step.

If [**SWAN**](https://swan.docs.cern.ch/intro/what_is/#what-is-swan) does not work for you, you can try the following backup solutions.

## Using VSCode to run a python notebook

#### Setting up the jupyter notebook environment with micromamba

- You can install extensions on VSCode to enable running **jupyter notebook**. Firstly, install the `ipykernel` and `jupyter` packages in the `higgs-dna` environment with the following commands, i.e.,

```bash
# activate the `higgs-dna` if you haven't
micromamba activate higgs-dna
# install packages
micromamba install ipykernel jupyter -y
```

- Then, install the VSCode extensions with the following instruction:
    
    <details>
    <summary> <b>Using VSCode to run a python notebook (click to expand)</b></summary>

    1. Go to `Extensions` in VSCode 

        <img src="figure/VSCode_Extension.png" alt="drawing" style="width:100px;"/>

    2. Search for "python" in the search box. And hit `install in SSH: lxplus9` to install the **Python** extension from **Microsoft**

        <img src="figure/python_ext.png" alt="drawing" style="width:100px;"/>


    3. Once **Python** extension installed. Continue to install the **Jupyter** extension.
        
        Again, search for "jupyter". And install **Jupyter** extension from **Microsoft**

        <img src="figure/jupyter_ext.png" alt="drawing" style="width:100px;"/>

    4. We are able to run the notebook in VSCode. Let us have a quick test.

        - Find the `higgsdna_finalfits_tutorial_24/01_columnar_introduction/coffea_basic.ipynb` in the `File Explore` and open it.

            In the top right corner, hit `Select Kernel` to choose the python kernel. 

            <img src="figure/01_coffea_notebook_1.png" alt="drawing" style="weight:500px;"/>

        - Click `Python Environments...` in the pop-up window.

            <img src="figure/01_coffea_notebook_2.png" alt="drawing" style="weight:500px;"/>

        - Choose the **higgs-dna** environment that has been installed by following [00_HiggsDNA_setup](https://gitlab.cern.ch/jspah/higgsdna_finalfits_tutorial_24/-/tree/master/00_HiggsDNA_setup?ref_type=heads).  

            <img src="figure/01_coffea_notebook_3.png" alt="drawing" style="weight:500px;"/>

        - Each code cell could be executed with **`Shift+Enter`**. Go to the first python code cell (Under **Load a root file from gluon-gluon fusion $H \rightarrow \gamma \gamma$**), then **`Shift+Enter`**, if it works, you will be able to see a checkmark in the bottom right corner (**Note**: If this is the first execution, it may take longer).

            <img src="figure/01_coffea_notebook_4.png" alt="drawing" style="weight:500px;"/>


    </details>

Once configured, you can run the notebook with VSCode, and also use VSCode terminal to run the previously installed `higgs-dna` environment.

## Running the script with `higgs-dna` environment

If you can't use notebook. You can execute the python script with the `coffea` package.

A python script `coffea_basic.py` is provieded. You can run the code with the `higgs-dna` evironment.

<details>
<summary> <b>Running the script with higgs-dna environment (click to expand)</b></summary>



```bash
# activate the `higgs-dna` if you haven't
micromamba activate higgs-dna

# run the script
python coffea_basic.py
```

Please note:

- `coffea_basic.py` just simply gathers the code from the notebook cells. You can find comments (e.g., `# cell 21`) that indicate which notebook cell the code snippet matches. 
    
    **Most of the code snippets are commented. You can uncomment them step by step**.
- The output from `python coffea_basic.py` is not as pretty  as the notebook output. Particularly, we can not view histograms within the terminal directly. 

    **Thus, the histograms are stored as `png` files.**

    Some tips to view the plots:
    
    - Using `ssh -XY` to enable `X11` forwarding for GUI, if you have a stable connection to lxplus. Then you can use `eog` to open png files.

    - To browser plots and files interactively, we could follow the suggestion from common analysis tool (**CAT**) group: [Interactive Plot Browser](https://cms-analysis.docs.cern.ch/guidelines/other/plot_browser/#manage-access-control).
    
        In this way, we could put plots to the **EOS**. Then the plots could be viewed from your own website with the [plot browser](https://cms-analysis.docs.cern.ch/guidelines/other/plot_browser/#install-the-plot-browser).

    - Simply download the plots locally.

</details>

# Exercise 1

Now, let us start! Open `coffea_basic.ipynb` (or `coffea_basic.py`) and play with it.