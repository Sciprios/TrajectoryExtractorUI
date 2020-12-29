from threading import Thread
from extractor_gui import TrajectoryExtractorUI
import os

class Controller(object):
    """ This class  controls the running of the trajectory extractor. """

    def __init__(self):
        self._gui = TrajectoryExtractorUI(self)

    def run(self):
        """ Creates a GUI. """
        self._gui.run()
    
    def get_dates(self, date_file):
        """ Retrieves dates from a given file. """
        dates = []
        # Test dates file exists.
        errors = self._test_dates(date_file)
        if len(errors) > 0:
            return errors, dates
        # Extract dates from there.
        raise NotImplementedError()
        return errors, dates

    def _test_dates(self, dates_file):
        """ Verifies dates file. """
        errors = []
        if not os.path.isfile(dates_file):
            errors.append("Dates file must be a file.")
        return errors

    def extract(self, meteo_folder, output_folder, start_time, run_time, latitude, longitude, dates_file):
        """ Extracts the trajectories. """
        print("{}, {}, {}, {}, {}, {}, {}".format(meteo_folder, output_folder, start_time, run_time, latitude, longitude, dates_file))
        errors = self._validate_requirements(meteo_folder, output_folder, start_time, run_time, latitude, longitude, dates_file)
        if len(errors) > 0:
            print(errors)
            return errors
        # Check if any errors exist
        #   IF they do return them
        #   ELSE move onto extraction
        raise NotImplementedError()

    def _validate_requirements(self, meteo_folder, output_folder, start_time, run_time, latitude, longitude, dates_file):
        """ Validates the inputs, meteorological files and dates file to ensure data is valid before extraction. """
        errors = []
        # Validate inputs
        init_vars, init_errors = self._test_initiation_parameters(meteo_folder, output_folder, start_time, run_time, latitude, longitude)
        errors = errors + init_errors
        # Validate dates file
        # Validate meteorological files
        return errors

    def _test_initiation_parameters(self, meteo_folder, output_folder, start_time, run_time, latitude, longitude):
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
        # Ensure start time are integers.
        try:
            start_time = int(start_time)
            run_time = int(run_time)
        except ValueError:
            errors.append("Start and run times must be an integers, e.g start time: '18' for 18:00 or '0' for 00:00 and run time: '-5' or '48'.")
        else:
            vals["start_time"] = start_time
            vals["run_time"] = run_time
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