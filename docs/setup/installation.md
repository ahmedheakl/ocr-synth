# Installation

## 📚 Requirements

- Python >= 3.11
- [Poetry](https://python-poetry.org/docs/#installation) (for dependency management)
- Latest version of docling (check for charts represented as tabular data in the picture annotation)

### Install the dependencies using Poetry
```bash
poetry install
poetry env activate
```
In case you python version is not compatible, or poetry install is giving some errors, you can create a conda env before:
```bash
conda create -n py311 python=3.11
conda activate py311
```
and the do the `poetry install`, you don't need to activate the poetry env if you follow this path.

### Git clone the chart generation repo
```bash
cd synthetic_data_generation
git clone https://github.ibm.com/DeepSearch/chart-rendering.git
```
then change the name of the folder fromm chart-rendering to chart_rendering.
Then switch to the branch dev/syn_data_adaptation

#### Install a LaTeX Compiler

Before you run the SDG, you must install a LaTeX compiler. On a Mac you can install MacTeX (the full version is required). MacTeX can be found here: ```https://www.tug.org/mactex/```.

### Use on a RedHatMachine

You need to manually install al the latex packages in the Latex environment
For some of the package you'll need to manually download, add them and then run

```
sudo mktexlsr /usr/share/texlive/texmf-dist/```

To update the TeX filename database.