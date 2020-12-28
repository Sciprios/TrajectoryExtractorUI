from threading import Thread
from extractor_gui import TrajectoryExtractorUI

class Controller(object):
    """ This class  controls the running of the trajectory extractor. """

    def __init__(self):
        self._gui = TrajectoryExtractorUI(self)

    def run(self):
        """ Creates a GUI. """
        self._gui.run()