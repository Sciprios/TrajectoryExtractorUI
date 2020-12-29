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
        message = "\n".join(error_messages)
        messagebox.showerror(title="Input Error", message=message)
        
    
    def _get_input(self, input_lbl):
        """ Retrieves input from the interface for a given object. """
        return self.builder.get_variable(input_lbl).get()
    
    def btn_run_clicked(self):
        meteo_folder = self._get_input('pc_meteo')
        output_folder = self._get_input('pc_output')
        start_time = self._get_input('tb_start_time')
        run_time = self._get_input('tb_run_time')
        dates_file = self._get_input('pc_dates')
        self._cont.extract(meteo_folder, output_folder, start_time, run_time, dates_file)
    
    def btn_dates_clicked(self):
        """ Extract the dates from a given csv file. """
        raise NotImplementedError()

    def run(self):
        self.mainwindow.mainloop()