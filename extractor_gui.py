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

        # Set starting text
        self.builder.get_variable('lbl_errors').set("")
    
    def _show_error(self, error_message):
        """ Displays an error message. """
        self.builder.get_variable('lbl_errors').set(error_message)
    
    def btn_run_clicked(self):
        messagebox.showinfo('Message', 'You clicked Button Run')  

    def run(self):
        self.mainwindow.mainloop()