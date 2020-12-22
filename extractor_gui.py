from tkinter import messagebox
import pygubu


class TrajectoryExtractorUI:

    def __init__(self, controller):
        self._cont = controller

        self.builder = builder = pygubu.Builder()
        builder.add_from_file('ui.ui')
        self.mainwindow = builder.get_object('frm_main')

        # Set the toplevel window Not resizable
        self.toplevel = self.mainwindow.winfo_toplevel()
        self.toplevel.resizable(False, False)

        builder.connect_callbacks(self)
    
    def btn_run_clicked(self):
        messagebox.showinfo('Message', 'You clicked Button Run')  

    def run(self):
        self.mainwindow.mainloop()