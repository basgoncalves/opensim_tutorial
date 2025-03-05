import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.filedialog as filedialog

def select_file(promt="Select a file"):
    # Create a file dialog to select the file
    root = tk.Tk()
    root.withdraw() # Hide the main window
    filepath = filedialog.askopenfilename(title=promt)
    return filepath


def plot_single_csv():
    file_path = select_file('Select the .csv file')
    if not file_path or not file_path.endswith('.csv'):
        raise ValueError('Please select a .csv file')
        
    data = pd.read_csv(file_path)

    print("data:")
    print(data.head())
    
    # plot emg
    plt.figure()
    for column in data.columns:
        if column != 'time':
            plt.plot(data['time'], data[column], label=column)
    plt.legend()
    plt.xlabel('Time [s]')
    plt.ylabel('Values (AU)')
    plt.show()

