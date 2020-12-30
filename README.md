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
2. Check and retrieve meteorological files (optional)
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

### 2. Check and retrieve meteorological files (optional)

Meteorological data is the foundation for extracting trajectories. Therefore, you must have the required meteorological data for your selected dates. Although this is optional it is highly recommended, this process will automatically retrieve all required meteorological data for the dates provided from NOAA [here](ftp://arlftp.arlhq.noaa.gov/pub/archives/reanalysis).

Once you've extracted your dates press the `Get Meteo Button` (highlighted green in Figure 2.1), this will begin the checking are retrieving process. The progress bar in the bottom right (highlighted red in Figure 2.1) will show progress of the system in retrieving all required meteorological files. You will also be notified each time a new meteorological file is going to be downloaded and a `Completed` message will be shown when this is complete.

#### Figure 2.1. The locations of important date extraction components.

![Highlighting the location of meteorological retrieval parts of the interface.](images/meteo.png?raw=true "Figure 2.1")

### 3. Extract Trajectories

Finally we get to the fun bit! Once you've got your dates, got your meteorological data it's time to make some trajectories. To do this you must define the initiation parameters in the boxes highlighted red in Figure 3.1. These parameters are detailed below:

Parameter | Less | Example
--- | --- | ---
Meteo. Files | A folder containing meteorological data. | `C:/MeteoFiles/`
Output Folder | A folder in which trajectories should be exported. | `C:/Trajectories/`
Start Time | The time of day to start the extraction using the 24-hour clock. | 18
Run Length | The time to run trajectories for. This should be negative for backwards trajectories. | -24
Altitude (m) | Altitude in meters to begin extraction. | 500
Latitude | Latitude starting point of the extraction. | -3.25
Longitude | Longitude starting point of the extraction. | -0.5

Once you've defined your parameters you can press the `Run` button highlighted green in Figure 3.1. This will first verify your inputs and then run the PySPLIT extraction program, progress can be seen in the progress bar (highlighted green in Figure 3.1). Any issues will be raised via message boxes, for example in the case of missing meteorological files.

#### Figure 3.1. The locations of important trajectory extraction components.

![Highlighting the location of meteorological retrieval parts of the interface.](images/trajs.png?raw=true "Figure 3.1")