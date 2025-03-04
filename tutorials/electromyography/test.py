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

emg_file = select_file('Select the EMG file')
joint_angles_file = select_file('Select the joint angles file')

emg_data = pd.read_csv(emg_file)
joint_angles_data = pd.read_csv(joint_angles_file)

print("EMG data:")
print(emg_data.head())

print("Joint angles data:")
print(joint_angles_data.head())

# plot emg
plt.figure()
for column in emg_data.columns:
    if column != 'time':
        plt.plot(emg_data['time'], emg_data[column], label=column)
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel('EMG')
plt.show()

