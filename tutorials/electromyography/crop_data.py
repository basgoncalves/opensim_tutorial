import os
import pandas as pd
import numpy as np
from matplotlib.widgets import SpanSelector
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import tkinter as tk
from tkinter import filedialog  

def select_columns(list_columns):
    # create a box to select the columns
    root = tk.Tk()
    root.title("Select the columns")
    root.geometry("300x300")
    root.resizable(False, False)
    root.columnconfigure(0, weight=1)

    # Create a listbox to display the columns
    listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
    for col in list_columns:
        listbox.insert(tk.END, col)
    listbox.grid(row=0, column=0, columnspan=3, sticky="nsew")

    # Add a button to confirm the selection
    def on_confirm():
        selected_indices = listbox.curselection()
        selected_columns[:] = [list_columns[i] for i in selected_indices]
        print("Selected columns:", selected_columns)
        root.quit()
        root.destroy()

    selected_columns = []
    confirm_button = tk.Button(root, text="Select", command=on_confirm)
    confirm_button.grid(row=1, column=2, sticky="nsew")

    root.mainloop()
    
    
    return selected_columns

def select_and_save_data(filepath, output_filepath):
    """
    Loads data from a file, plots it, allows region selection with the mouse,
    and saves the selected data to a new file.

    Args:
        filepath (str): Path to the input data file.
        output_filepath (str): Path to save the selected data.
    """
    try:
        # Load the data (assuming comma-separated values, adjust as needed)
        df = pd.read_csv(filepath)
        df.columns = df.columns.str.strip() # remove spaces before and after the column names
        
        if len(df.columns) < 2:
            x = list(np.arange(len(df)))
            y = df.iloc[:, 0]
        else:
            x = df.iloc[:,0] # Assuming the first column is the x-axis and the second is the y-axis
            selected_columns = select_columns(df.columns)
            trimmed_columns = [col.strip() for col in selected_columns]
            y = df[trimmed_columns]

        # import pdb; pdb.set_trace()
        fig, ax = plt.subplots()
        ax.plot(x,y)
        ax.set_title("Select a region to keep (close fig to continue ...)")

        selected_data = None

        def line_select_callback(eclick, erelease):
            """Callback for line selection."""
            nonlocal selected_data
            x1, y1 = eclick.xdata, eclick.ydata
            x2, y2 = erelease.xdata, erelease.ydata

            # Determine the min and max x values for the selected region
            x_min = min(x1, x2)
            x_max = max(x1, x2)

            # Filter the data based on the selected x range
            selected_data = df.iloc[(x >= x_min) & (x <= x_max)]

            print("Selected region:")
            print(f"X range: [{x_min}, {x_max}]")
            print(f"Number of points selected: {len(selected_data)}")

        def toggle_selector(event):
            """Toggle selector on and off."""
            if event.key == 't':
                if toggle_selector.RS.active:
                    toggle_selector.RS.set_active(False)
                else:
                    toggle_selector.RS.set_active(True)

        # Create the rectangle selector
        toggle_selector.RS = RectangleSelector(
            ax, line_select_callback,
            useblit=True,
            button=[1],  # Only react to left mouse button
            minspanx=5, minspany=5,
            spancoords='pixels',
            interactive=True
        )

        fig.canvas.mpl_connect('key_press_event', toggle_selector)
        plt.show()

        if selected_data is not None:
            # Save the selected data to the output file
            selected_data.to_csv(output_filepath, index=False)
            print(f"Selected data saved to {output_filepath}")
        else:
            print("No region selected.")

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")

current_path = os.path.dirname(os.path.abspath(__file__))
file_list = os.listdir(current_path)


file_path = filedialog.askopenfilename()
output_file_path = file_path.replace(".csv", "_selected.csv")
select_and_save_data(file_path, output_file_path)
