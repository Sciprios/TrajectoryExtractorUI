from tkinter import messagebox
import pygubu


class TrajectoryExtractorUI:

    def __init__(self, controller):
        self._cont = controller

        self.builder = pygubu.Builder()
        self.builder.add_from_file('ui.ui')
        self.mainwindow = self.builder.get_object('frm_main')

        # Set the toplevel window Not resizable
        self.toplevel = self.mainwindow.winfo_toplevel()
        self.toplevel.resizable(False, False)

        self.builder.connect_callbacks(self)
    
    def _show_errors(self, error_messages):
        """ Displays error messages. """
        message = ""
        for idx, e in enumerate(error_messages):
            message = message +"{}. {}\n".format(idx+1, e)
        messagebox.showerror(title="Input Error", message=message)
        
    
    def _get_input(self, input_lbl):
        """ Retrieves input from the interface for a given object. """
        return self.builder.get_variable(input_lbl).get()
    
    def btn_run_clicked(self):
        meteo_folder = self._get_input('pc_meteo')
        output_folder = self._get_input('pc_output')
        start_time = self._get_input('tb_start_time')
        run_time = self._get_input('tb_run_time')
        longitude = self._get_input('tb_longitude')
        latitude = self._get_input('tb_latitude')
        dates_file = self._get_input('pc_dates')
        # Extract trajectories
        errors = self._cont.extract(meteo_folder, output_folder, start_time, run_time, latitude, longitude, dates_file)
        if len(errors) > 0:
            self._show_errors(errors)
    
    def btn_dates_clicked(self):
        """ Extract the dates from a given csv file. """
        dates_file = self._get_input('pc_dates')
        errors, dates = self._cont.get_dates(dates_file)
        if len(errors) > 0:
            self._show_errors(errors)
        # Update List View

    def run(self):
        self.mainwindow.mainloop()