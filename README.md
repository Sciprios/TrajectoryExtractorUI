# TrajectoryExtractorUI
A GUI extraction tool for trajectories using Pysplit.

## Requirements
 Written and tested using Python 3.7 and Hysplit. All required libraries are given in the `requirements.txt` file. To install these using the following commands:

### Anaconda
    conda install --file requirements.txt

### Pip
    pip install -r requirements.txt

## Extraction Process

### Preliminaries
In order to extract trajectories you will need the meteorological data files associated with the dates and times you wish to extract for. For example, to extract a trajectory for 48 hours backwards from 01-12-2000, meteorological files for both 12-2000 and 11-2000 will be required as the backwards trajectory will go through both months.

If you find any issues in the identification of meteorological files please see the Pysplit Github page [here](https://github.com/mscross/pysplit).