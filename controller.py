from threading import Thread
from extractor_gui import TrajectoryExtractorUI
from ftplib import FTP
import numpy as np
import datetime
import pysplit
import os

class Controller(object):
    """ This class  controls the running of the trajectory extractor. """

    def __init__(self):
        self._gui = TrajectoryExtractorUI(self)
        self._dates = None
        self._worker_thread = None

    def run(self):
        """ Creates a GUI. """
        self._gui.run()
    
    def check_meteo_files(self, meteo_folder):
        """ Checks and downloads missing meteo files. """
        messages = []
        # Check dates and meteofolder have been loaded
        if not os.path.isdir(meteo_folder):
            messages.append("Meteorological folder must be a folder.")
        if self._dates is None:
            messages.append("Please load dates first.")
        # Check worker isn't busy
        if self._worker_thread is not None:
            messages.append("Please wait for current operation to finish first.")
        if len(messages) == 0:
            # Setup worker
            # Run worker
            self._worker_thread = Thread(
                target=self._download_meteo_files,
                args=(meteo_folder,)
            )
            self._worker_thread.start()
            messages.append("Downloading Meteorological files... This might take a while!")
        return messages
    
    def _download_meteo_files(self, meteo_folder):
        """ Method to download meteorological files that don't exist. """
        for didx, d in enumerate(self._dates.astype(int)):
            dte = datetime.date(d[2], d[1], d[0])
            file_location = meteo_folder + "/" + dte.strftime(
                "RP%b-{}.gbl1"
            ).format(str(d[2])[-2:])
            file_down_name = 'RP{}{:02d}.gbl'.format(d[2], d[1])
            if not os.path.exists(file_location):
                self._meteo_update(
                    ((didx)/self._dates.shape[0])*100,
                    messages=["Downloading meteorology for {}/{}".format(d[1], d[2])])
                ftp = FTP('arlftp.arlhq.noaa.gov')
                ftp.login()
                ftp.cwd('pub/archives/reanalysis')
                with open(file_location, 'wb') as local_file:
                    print("Retrieving file: {}".format(file_down_name))
                    ftp.retrbinary(
                        "RETR /pub/archives/reanalysis/" + file_down_name,
                        local_file.write
                    )
            self._meteo_update(((didx+1)/self._dates.shape[0])*100)

    def _meteo_update(self, progress, messages=[]):
        """ Updates the GUI with extrcation progress. """
        if progress == 100:
            self._worker_thread = None
            messages.append("COMPLETED")
        self._gui.update(progress, messages=messages)
    
    def get_dates(self, date_file):
        """ Retrieves dates from a given file. """
        dates = []
        # Test dates file exists.
        errors = self._test_dates(date_file)
        if len(errors) > 0:
            return errors, dates
        # Extract dates from there.
        dates = self._extract_dates(date_file)
        if len(dates.shape) < 2:
            errors.append("Invalid date file, please provide data in the format day,month,year.")
        self._dates = dates
        return errors, dates
    
    def _extract_dates(self, date_file):
        """ Extracts dates, assuming a particular format. """
        dates = np.genfromtxt(date_file, delimiter=',')
        return dates

    def _test_dates(self, dates_file):
        """ Verifies dates file. """
        errors = []
        if not os.path.isfile(dates_file):
            errors.append("Dates file must be a file.")
        return errors

    def extract(self, meteo_folder, output_folder, start_time, run_time, altitude, latitude, longitude, dates_file):
        """ Extracts the trajectories. """
        if self._worker_thread is not None:
            return ["Please wait for current extraction to finish."]
        else:
            print("Attempting extraction: {}, {}, {}, {}, {}, {}, {}, {}".format(meteo_folder, output_folder, start_time, run_time, altitude, latitude, longitude, dates_file))
            init_vars, errors = self._validate_requirements(meteo_folder, output_folder, start_time, run_time, altitude, latitude, longitude, dates_file)
            # Check dates exist
            if self._dates is None:
                errors.append("Please extract dates first.")
            if len(errors) > 0:
                return errors
            # Check meteorological files exist.
            errors = self._test_meteorology(init_vars['meteo_folder'], self._dates)
            print(errors)
            if len(errors) > 0:
                return errors
            # Run extraction on a new thread.
            print(init_vars['altitude'])
            self._worker_thread = Thread(
                target=self.get_trajs,
                args=(
                    self._extraction_update,
                    self._dates,
                    init_vars['latitude'],
                    init_vars['longitude'],
                    init_vars['altitude'],
                    init_vars['output_folder'],
                    init_vars['meteo_folder'],
                    init_vars['start_time'],
                    init_vars['run_time'],)
            )
            self._worker_thread.start()
            return ["Extracting Trajectories..."]
    
    def _extraction_update(self, progress, messages=[]):
        """ Updates the GUI with extrcation progress. """
        if progress == 100:
            self._worker_thread = None
            messages.append("COMPLETED")
        self._gui.update(progress, messages=messages)
    
    def get_trajs(self, update_method, dates, lat, lon, altitude, output_folder, meteo_folder, start_time, run_time):
        """ Extracts trajectories with the given initiation values. """
        for didx, d in enumerate(dates.astype(int)):
            print("EXTRACTING {}".format(d))
            day = d[0]
            month = d[1]
            year = d[2]

            days = slice(int(day)-1, int(day), 1)
            try:
                pysplit.generate_bulktraj(
                'traj_',
                "C:/hysplit4/working",
                output_folder,
                meteo_folder,
                [year], [month],
                [start_time],
                [altitude],
                (lat, lon),
                run_time,
                monthslice=days,
                meteo_bookends=([1, 2, 3, 4, 5], []),
                get_reverse=False,
                get_clipped=False)
            except OSError:
                update_method(((didx+1)/dates.shape[0])*100, messages=["Meteorological files missing for event {}-{}-{}".format(day, month, year)])
            else:
                update_method(((didx+1)/dates.shape[0])*100)
                

    def _validate_requirements(self, meteo_folder, output_folder, start_time, run_time, altitude, latitude, longitude, dates_file):
        """ Validates the inputs, meteorological files and dates file to ensure data is valid before extraction. """
        errors = []
        # Validate inputs
        init_vars, init_errors = self._test_initiation_parameters(meteo_folder, output_folder, start_time, run_time, altitude, latitude, longitude)
        errors = errors + init_errors
        return init_vars, errors

    def _test_initiation_parameters(self, meteo_folder, output_folder, start_time, run_time, altitude, latitude, longitude):
        """ Verifies inputs are valid, returning values and appropriate error messages. """
        errors = []
        vals = {}
        # Check the output folder is a directory that exists
        if not os.path.isdir(output_folder):
            errors.append("Output folder must be a folder.")
        else:
            vals["output_folder"] = output_folder
        # Check meteo folder is a directory that exists
        if not os.path.isdir(meteo_folder):
            errors.append("Meteorological folder must be a folder.")
        else:
            vals["meteo_folder"] = meteo_folder
        # Ensure start and run times are integers.
        try:
            start_time = int(start_time)
            run_time = int(run_time)
        except ValueError:
            errors.append("Start and run times must be an integers, e.g start time: '18' for 18:00 or '0' for 00:00 and run time: '-5' or '48'.")
        else:
            if start_time < 0:
                errors.append("Start time cannot be negative.")
            vals["start_time"] = start_time
            vals["run_time"] = run_time
        # Ensure altitude is valid
        try:
            altitude = int(altitude)
        except ValueError:
            errors.append("Altitude must be an integer in meters (m).,e.g 500, 1250 etc.")
        else:
            if altitude < 1:
                errors.append("Altitude cannot be < 500m.")
            vals["altitude"] = altitude
        # Ensure longitude and latitude are floats.
        try:
            longitude = float(longitude)
            latitude = float(latitude)
        except ValueError:
            errors.append("Longitude and latitude must be provided as floats. E.g Latitude")
        else:
            if longitude > 180 or longitude < -180:
                errors.append("Longitude must be between 180 and -180 degrees.")
            if latitude > 90 or latitude < -90:
                errors.append("Latitude must be between 90 and -90 degrees.")
            vals["longitude"] = longitude
            vals["latitude"] = latitude
        return vals, errors

    def _test_meteorology(self, meteo_folder, dates):
        """ Verifies meteorological files are available for all dates requested. """
        errors = []
        return errors