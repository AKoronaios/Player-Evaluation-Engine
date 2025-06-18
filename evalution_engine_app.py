# main_app.py

from load_cleaning_data import *
from stat_weights_version_2 import *
from evaluate_players_by_position import *
from show_evalution import show_evaluation_table
from filter_dataset_version_2 import FilterWindow
import tkinter as tk
from tkinter import filedialog, messagebox


# Global storage for intermediate results
df_cleaned = None
filtered_result = None
stat_weights_dict = None

def handle_load_data():
    global df_cleaned
    file_path = filedialog.askopenfilename(
        filetypes=[("HTML Files", "*.html")],
        title="Select HTML file"
    )
    if file_path:
        try:
            df_cleaned = load_cleaning_data(file_path)
            messagebox.showinfo("Success", "Data cleaned")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file:\n{e}")

def handle_filters():
    global filtered_result
    if df_cleaned is None:
        messagebox.showwarning("Warning", "Please load and clean data first.")
        return

    def save_filtered(df):
        global filtered_result
        filtered_result = {"df": df}
        messagebox.showinfo("Success", "Data filtered successfully.")

    FilterWindow(root, df_cleaned, callback=save_filtered)

def handle_stats():
    global stat_weights_dict
    try:
        # Pass your main root window as parent to keep it modal
        stat_weights_dict = get_stat_weights(root)
        if stat_weights_dict:
            messagebox.showinfo("Success", "Stats and weights selected!")
        else:
            messagebox.showinfo("Info", "No stats selected.")
        return stat_weights_dict
    except Exception as e:
        messagebox.showerror("Error", f"Stat selection failed:\n{e}")
        return {}

def handle_evaluate():
    if filtered_result is None or stat_weights_dict is None:
        messagebox.showwarning("Warning", "Please filter data and set stat weights first.")
        return
    try:
        evaluated_df = evaluate_players_by_position(filtered_result['df'], stat_weights_dict)
        show_evaluation_table(evaluated_df)
    except Exception as e:
        messagebox.showerror("Error", f"Evaluation failed:\n{e}")

# GUI Setup
root = tk.Tk()
root.title("Football Analytics Tool")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Football Analytics Tool", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=20)

tk.Button(root, text="1. Load & Clean Data", command=handle_load_data, width=30).pack(pady=5)
tk.Button(root, text="2. Set Up Filters", command=handle_filters, width=30).pack(pady=5)
tk.Button(root, text="3. Select Stats & Weights", command=handle_stats, width=30).pack(pady=5)
tk.Button(root, text="4. Evaluate Players", command=handle_evaluate, width=30).pack(pady=5)

tk.Button(root, text="Exit", command=root.quit, width=30).pack(pady=20)

root.mainloop()
