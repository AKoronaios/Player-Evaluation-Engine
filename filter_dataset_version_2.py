# filter_dataset.py

import tkinter as tk
from tkinter import ttk
import pandas as pd

class FilterWindow:
    def __init__(self, master, df, callback):
        self.df = df
        self.filtered_df = df.copy()
        self.callback = callback  # Function to call when filtering is done

        self.window = tk.Toplevel(master)
        self.window.title("Filter Data")
        self.window.geometry("400x500")

        # Dropdowns for Nat and Division
        self.nat_var = tk.StringVar()
        self.div_var = tk.StringVar()
        self.nat_var.set("All")
        self.div_var.set("All")

        nat_list = ["All"] + sorted(df["Nat"].dropna().unique().tolist())
        div_list = ["All"] + sorted(df["Division"].dropna().unique().tolist())

        ttk.Label(self.window, text="Nationality:").pack()
        self.nat_dropdown = ttk.Combobox(self.window, textvariable=self.nat_var, values=nat_list)
        self.nat_dropdown.pack(pady=5)

        ttk.Label(self.window, text="Division:").pack()
        self.div_dropdown = ttk.Combobox(self.window, textvariable=self.div_var, values=div_list)
        self.div_dropdown.pack(pady=5)

        # Multi-select list for Position
        ttk.Label(self.window, text="Position(s):").pack()
        all_positions = set()
        for pos in df["Position"]:
            all_positions |= pos if isinstance(pos, set) else set()

        self.position_listbox = tk.Listbox(self.window, selectmode=tk.MULTIPLE, height=6)
        for pos in sorted(all_positions):
            self.position_listbox.insert(tk.END, pos)
        self.position_listbox.pack(pady=5)

        # Age slider
        ttk.Label(self.window, text="Age Range:").pack()
        self.age_min = tk.IntVar(value=14)
        self.age_max = tk.IntVar(value=55)
        tk.Scale(self.window, from_=14, to=55, orient=tk.HORIZONTAL, variable=self.age_min, label="Min Age").pack()
        tk.Scale(self.window, from_=14, to=55, orient=tk.HORIZONTAL, variable=self.age_max, label="Max Age").pack()

        # Salary slider
        ttk.Label(self.window, text="Salary Range:").pack()
        min_salary = int(df["Salary"].min())
        max_salary = int(df["Salary"].max())
        self.salary_min = tk.IntVar(value=min_salary)
        self.salary_max = tk.IntVar(value=max_salary)

        tk.Scale(self.window, from_=min_salary, to=max_salary, orient=tk.HORIZONTAL,
                 resolution=10000, variable=self.salary_min, label="Min Salary").pack()
        tk.Scale(self.window, from_=min_salary, to=max_salary, orient=tk.HORIZONTAL,
                 resolution=10000, variable=self.salary_max, label="Max Salary").pack()

        # Filter button
        tk.Button(self.window, text="Apply Filters", command=self.apply_filters).pack(pady=10)

    def apply_filters(self):
        df = self.df.copy()

        # Filter by Nat
        nat = self.nat_var.get()
        if nat != "All":
            df = df[df["Nat"] == nat]

        # Filter by Division
        div = self.div_var.get()
        if div != "All":
            df = df[df["Division"] == div]

        # Filter by Position
        selected_indices = self.position_listbox.curselection()
        selected_positions = [self.position_listbox.get(i) for i in selected_indices]
        if selected_positions:
            df = df[df["Position"].apply(lambda pos_set: bool(set(selected_positions) & pos_set))]

        # Filter by Age
        df = df[(df["Age"] >= self.age_min.get()) & (df["Age"] <= self.age_max.get())]

        # Filter by Salary
        df = df[(df["Salary"] >= self.salary_min.get()) & (df["Salary"] <= self.salary_max.get())]

        self.filtered_df = df.copy()
        self.callback(self.filtered_df)
        self.window.destroy()

# Usage:
# from filter_dataset import FilterWindow
# FilterWindow(root, df, callback=store_result)
