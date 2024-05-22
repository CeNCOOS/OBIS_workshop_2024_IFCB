# Prototype OBIS-ENV-Data package for HABDAC IFCB data products from Santa Cruz Municipal Wharf

__Prepared for 2024 OBIS IOOS Marine Biological Data Mobilization Workshop.__

__Authors: Frederick Bahr (CeNCOOS), Patrick Daniel (UCSC), Stace Beaulieu (WHOI) __

**This is a prototype for testing purposes only. A protocol is being developed to determine if and when appropriate to submit products from automated classification to OBIS.**

Sponsored by NOAA PCMHAB20 project “Harmful Algal Bloom Community Technology Accelerator”

## Background
This is a repository for OBIS 2024 Workshop.  The plan is to take work done by Axiom and Ian Brunjes from previous workshops and create a full workflow to an OBIS ready output.
Code has already been created to generate Event and Occurance tables.  The plan is to supplement these with the EMoF table following best practices.
Pre-workshop coding is being done to translate Ian's magnificent work from R to Python.

## How to Run
Setting up the environoment in `conda`:

    conda create -n obis_ifcb python=3.9 numpy pandas
    conda activate obis_ifcb
    pip install pyworms

## Workflow
1) Check to see if we can query IFCB api for IFCBs available.</p>
2) Create a Json config file of information that has filenames, paths, and data not available by machine</p>
3) Move pyworms code section into a module</p>
4) Create module for event table that returns Panda's DataFrame that can be concatenatted to </p>
5) Do the same for the Occurrence table</p>
6) Do the same for the EMoF table </p>
7) Clean up code to make more efficient and clean 

## Output File Description
