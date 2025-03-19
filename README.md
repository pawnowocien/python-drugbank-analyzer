# DrugBank data analyzer

### [University Project] [Python]

**Warning:** The assignment and comments in the code are written in **Polish**.

## About the project

This project is a [DrugBank](https://go.drugbank.com/) data analyzer that processes and visualizes information about drugs, their interactions, pathways, and more. It uses various Python libraries such as `pandas`, `matplotlib`, `networkx`, and `fastapi` to perform data analysis and generate visualizations.

The assignment is available [here](docs/assignment.pdf).

## Installation

You can install the required dependencies with:

`pip install pandas matplotlib networkx scipy fastapi uvicorn xmltodict requests beautifulsoup4 pytest`

## Usage

To run the analyzer, use `main.py` script. You have to specify which modules to run (1-12) using a string of numbers and ranges (allowed smbols are numbers, commas and hyphens).

Modules 13-15 cannot be run via `main.py`:
- Module 13 - Generates data
- Module 14 - Contains is `pytest` tests
- Module 15 - Runs a FastAPI server (to execute, run `uvicorn module_15:app --reload` and access the docs)

For some modules, the user must specify drug ID or gene. Good examples are: `DB00001`, `DB00005` for drug IDs and `F2`, `FCGR3A` for genes.

## Command Format

`python main.py <modules> [options]`

### Options

- `sv` - save the generated plots to the graphics directory.
- `sh` - show the generated plots.
- `ge` - run using generated data (100 from the sample, 19,900 generated).

### Examples

**Run module 1 with default settings**

`python main.py 1`

**Run module 2, save plots but do not display them**

`python main.py 2 -sv`

**Run modules 1-4 and 12, display plots, and use generated data**

`python main.py 1-4,12 -sh -ge`


## Additional Information

### Function Arguments & Configuration

Many functions across modules share these common arguments:

Argument        | Description                               | Default Value
| -             | -                                         | - |
data=None       | Selects the data source.                  | Uses drugbank_partial.xml by default. 
save_path=None  | Specifies the save location for images.	| No saving if not provided.
show=True	    | Controls whether plots are displayed.	    | Enabled by default.

### Recommended Reading Order

Before diving into the module scripts, it’s helpful to review these files first:

- `utils.py` – Contains utility functions used across multiple modules.
- `display.py` – Handles default visualization functions.