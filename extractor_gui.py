from tkinter import messagebox
import tkinter as tk
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

        self._reset_dates()
    
    def update(self, progress, maxi=100):
        """ Updates the progress bar on progress of extractions. """
        pb = self.builder.get_object('pb_main')
        pb['maximum'] = maxi
        pb['value'] = progress

    def _reset_dates(self):
        tv = self.builder.get_object('tv_dates')
        tv["columns"] = (2, 3)
        tv.column("#0", width=50, minwidth=50, stretch=tk.NO)
        tv.column(2, width=50, minwidth=50, stretch=tk.NO)
        tv.column(3, width=50, minwidth=50, stretch=tk.NO)
        tv.heading("#0",text="Day",anchor=tk.W)
        tv.heading(2, text="Month",anchor=tk.W)
        tv.heading(3, text="Year",anchor=tk.W)
    
    def _show_errors(self, error_messages):
        """ Displays error messages. """
        message = ""
        for idx, e in enumerate(error_messages):
            message = message +"{}. {}\n".format(idx+1, e)
        messagebox.showerror(title="Input Error", message=message)
    
    def _show_messages(self, messages):
        """ Displays messages. """
        message = ""
        for idx, e in enumerate(messages):
            message = message +"{}. {}\n".format(idx+1, e)
        messagebox.showinfo(title="Info", message=message)
    
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
        messages = self._cont.extract(meteo_folder, output_folder, start_time, run_time, latitude, longitude, dates_file)
        if len(messages) > 0:
            self._show_messages(messages)
    
    def btn_dates_clicked(self):
        """ Extract the dates from a given csv file. """
        dates_file = self._get_input('pc_dates')
        errors, dates = self._cont.get_dates(dates_file)
        if len(errors) > 0:
            self._show_errors(errors)
        else:
            # Update List View
            tv = self.builder.get_object('tv_dates')
            for date in dates.astype(int):
                print(date)
                tv.insert('', 'end', text=date[0], values=(date[1], date[2]))

    def run(self):
        self.mainwindow.mainloop()