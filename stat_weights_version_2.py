import tkinter as tk
from tkinter import ttk, messagebox

class StatWeightsDialog(tk.Toplevel):
    def __init__(self, parent, stats_list):
        super().__init__(parent)
        self.title("Select Stats and Assign Weights")
        self.selected_stats = None  # Will hold results after submit

        self.geometry("400x500")

        # Scrollable frame setup
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Dicts to hold widgets
        self.checkboxes = {}
        self.entries = {}

        # Create stat checkboxes and entries
        for stat in stats_list:
            frame = ttk.Frame(scrollable_frame)
            frame.pack(fill="x", pady=2, padx=5)

            var = tk.BooleanVar()
            chk = ttk.Checkbutton(frame, text=stat, variable=var)
            chk.pack(side="left", anchor="w")

            entry = ttk.Entry(frame, width=6)
            entry.insert(0, "0.5")
            entry.pack(side="right", anchor="e")

            self.checkboxes[stat] = var
            self.entries[stat] = entry

        # Submit button
        submit_btn = ttk.Button(self, text="Submit", command=self.on_submit)
        submit_btn.pack(pady=10)

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        parent.wait_window(self)

    def on_submit(self):
        selected = {}
        for stat, var in self.checkboxes.items():
            if var.get():
                try:
                    weight = float(self.entries[stat].get())
                    if 0 <= weight <= 1:
                        selected[stat] = weight
                    else:
                        messagebox.showerror("Invalid weight", f"Weight for {stat} must be between 0 and 1.")
                        return
                except ValueError:
                    messagebox.showerror("Invalid input", f"Weight for {stat} must be a number.")
                    return

        self.selected_stats = selected
        self.destroy()

    def on_close(self):
        # User closed window without submitting
        self.selected_stats = {}
        self.destroy()


def get_stat_weights(root):
    stats_list = [ 'Dist/90','Poss Won/90', 'Poss Lost/90', 'Gwin','Pts/Gm', 'Tgls/90', 'Tcon/90', 'Gls','Gls/90', 'Conv %', 'Mins/Gl', 'Last Gl', 'xG', 'xG/90', 
                  'xG-OP', 'NP-xG', 'NP-xG/90', 'Shots','Shot/90', 'xG/shot', 'ShT', 'ShT/90', 'Shot %', 'Shots Outside Box/90', 'Goals Outside Box', 'Pens',
    'Pens S', 'Pen/R', 'Ast', 'Asts/90', 'xA', 'xA/90', 'Pas A', 'Ps A/90', 'Ps C', 'Ps C/90', 'Pas %', 'Pr Passes', 'Pr passes/90', 'K Pas', 'K Ps/90', 'OP-KP', 'OP-KP/90',
    'CCC', 'Ch C/90', 'Cr A', 'Crs A/90', 'Cr C', 'Cr C/90', 'Cr C/A', 'OP-Crs A', 'OP-Crs A/90', 'OP-Crs C', 'OP-Crs C/90', 'OP-Cr %', 'Drb', 'Drb/90', 'FA', 'Off',
    'Sprints/90', 'Tck A', 'Tck/90', 'Tck C', 'Tck R', 'K Tck', 'K Tck/90', 'Itc', 'Int/90', 'Blk', 'Blk/90', 'Shts Blckd', 'Shts Blckd/90', 'Clear', 'Clr/90', 'Fls', 'Yel',
    'Red', 'Gl Mst', 'Hdrs A', 'Aer A/90', 'Hdrs', 'Hdrs W/90', 'Hdrs L/90', 'Hdr %', 'K Hdrs/90', 'Pres A', 'Pres A/90', 'Pres C', 'Pres C/90', 'Shutouts', 'Cln/90',
    'Conc', 'All/90', 'Last C', 'xGP', 'xGP/90', 'Svh', 'Svp', 'Svt', 'Saves/90', 'Sv %', 'xSv %', 'Pens Faced', 'Pens Saved', 'Pens Saved Ratio']

    dialog = StatWeightsDialog(root, stats_list)
    return dialog.selected_stats
