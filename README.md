# TrajectoryExtractorUI
A GUI extraction tool for trajectories using Pysplit.

## Requirements
 Written and tested using Python 3.7 and Hysplit. All required libraries are given in the `requirements.txt` file. To install these using the following commands:

### Anaconda
    conda install --file requirements.txt

### Pip
    pip install -r requirements.txt

## Extraction Process

The extraction process has three steps:
1. Retrieve dates
2. Check meteorological files (optional)
3. Extract trajectories

### 1. Retrieving Dates

Firstly, a set of dates can be extracted from a CSV file using the file selector highlighted green in Figure 1.1. This CSV file is expected to be formated in the following way: `Day,Month,Year`. For example:

```
28,02,1995
03,12,2010
04,05,2009
17,11,1990
```

Once you've selected the dates file, press the `Get Dates` button (highlighted blue in Figure 1.1) to extract the dates which will then be shown in the table highlighted red in Figure 1.1.

#### Figure 1.1. The locations of important date extraction components.

![Highlighting the location of date extraction parts of the interface.](images/dates.png?raw=true "Figure 1.1")


