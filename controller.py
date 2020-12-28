from threading import Thread
from extractor_gui import TrajectoryExtractorUI

class Controller(object):
    """ This class  controls the running of the trajectory extractor. """

    def __init__(self):
        self._gui = TrajectoryExtractorUI(self)

    def run(self):
        """ Creates a GUI. """
        self._gui.run()
    
    def extract(self, meteo_folder, output_folder, start_time, run_time, dates_file):
        """ Extracts the trajectories. """
        print("{}, {}, {}, {}, {}".format(meteo_folder, output_folder, start_time, run_time, dates_file))
        raise NotImplementedError()