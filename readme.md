[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3875550.svg)](https://doi.org/10.5281/zenodo.3875550)
# A Map Representation of the ASET-RSET concept

Base case scenario for demonstration purposes. Reference implementation of the methodology proposed in 

B. Schröder, L. Arnold, and A. Seyfried; "A Map Representation of the ASET-RSET Concept", accepted for publication in the Fire Safety Journal, 2020

## Fire Simulation

* Conducted with NIST's Fire Dynamics Simulator. Available here: https://pages.nist.gov/fds-smv/
* Simple Room with a simplified fire i.e. a constant HRR of 60 kW
* Write-out of extinction and temperature at a height of z = 2.0 m (.sf)
* Simulation time 120 s
* Output data is part of the repository

## Evacuation Simulation

* Conducted with JuPedSim. Available here: http://www.jupedsim.org
* Room occupied with 100 agents
* Instantaneous movement towards the exit
* Write-out of pedestrian's trajectories (.xml)
* 10 computational realisations (random seed ranges from 1254 to 1263)
* Simulation time 200 s
* Output data is part of the repository

## Requirements for the Analysis

* Python 3.8
* Python modules: glob, xml.etree.ElementTree, numpy, scipy, matplotlib+pyplot, pylab

## ASET map generation

* preprocessing for conversion of FDS slices to ascii format
* generation of ASET map from ascii slicefiles (.txt)
* execute python 0_ASET/aset_map.py

## RSET map generation (incorporating 10 computational realisations)

* generation of RSET map from trajectories (.xml)
* execute python 1_RSET/rset_map.py

## Difference map generation and consequence quantification

* execute python 2_DIFF/diff_map.py
