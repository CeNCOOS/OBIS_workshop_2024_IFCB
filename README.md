# Prototype OBIS-ENV-Data package for HABDAC IFCB data products from Santa Cruz Municipal Wharf

__Prepared for 2024 OBIS IOOS Marine Biological Data Mobilization Workshop.__

__Authors: Frederick Bahr (CeNCOOS), Patrick Daniel (UCSC), Stace Beaulieu (WHOI)__

**This is a prototype for testing purposes only. A protocol is being developed to determine if and when appropriate to submit products from automated classification to OBIS.**

Sponsored by NOAA PCMHAB20 project “Harmful Algal Bloom Community Technology Accelerator”

## Background
This is a repository for CeNCOOS at the 2024 OBIS IOOS Marine Biological Data Mobilization Workshop.  The plan is to take work done by Axiom and Ian Brunjes (SCCOOS) from previous workshops and create a full workflow to an OBIS-ENV-Data ready output.
Code has already been created to generate Event and Occurrence tables.  The plan is to supplement these with the EMoF table following best practices (http://dx.doi.org/10.25607/OBP-1955).
Pre-workshop coding is being done to translate Ian's magnificent work from R to Python.

## How to Run
Setting up the environoment in `conda`:

    conda create -n obis_ifcb python=3.9 numpy pandas
    conda activate obis_ifcb
    pip install pyworms
Additional packages needed in conda are:
```
 import numpy as np
 import pandas as pd
 import pyworms
 import requests
 import json
 import os
 import pyworms
 import math
```
## Input Files
- IFCB data products and metadata are acquired using IFCB Dashboard API
- Also, in data folder: class_names_matched_to_WoRMS, class_thresholds, DwC_matching_to_IFCB

## Workflow
The prototype workflow is run in a notebook (see notebooks folder). Some of the Helper Functions in the notebook are available in the utilities folder.</p>
1) Load class labels and call WoRMS API</p>
2) Load class specific thresholds</p>
3) Load helper functions</p>
4) Call the dashboard API</p>
5) Get available datasets from the dashboard</p>
6) Get bin files within the date range</p>
7) Get bin metadata file</p>
8) Check if the bin file has an autoclass file on the dashboard and load the file into a pandas dataframe</p>
9) Get the ml_analyzed from the IFCB database for each bin</p>
10) Get image feature information</p>
11) Select top class for each roi</p>
12) Generate a summary table</p>
13) Generate event table</p>
14) Generate the occurrence table</p>
15) Generate Extended Measurement of Fact Table including Pelagic Size Structure Database (PSSdbb) biovolume</p>
<!--
1) Check to see if we can query IFCB api for IFCBs available.</p>
2) Create a Json config file of information that has filenames, paths, and data not available by machine</p>
3) Move pyworms code section into a module</p>
4) Create module for event table that returns Panda's DataFrame that can be concatenatted to </p>
5) Do the same for the Occurrence table</p>
6) Do the same for the EMoF table </p>
7) Clean up code to make more efficient and clean -->

## Output Files
- In data folder: ifcb_event.csv, ifcb_occurrence.csv, ifcb_emof.csv
