import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def select_file(promt="Select a file"):
    # Create a file dialog to select the file
    root = tk.Tk()
    root.withdraw() # Hide the main window
    filepath = filedialog.askopenfilename(title=promt)
    return filepath

def filter_emg()