import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.filedialog as filedialog

def find_header_line(file_path):
    """
    Find the line number where the header is located in a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        int: Line number of the header.
    """
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            if line.startswith('time'):
                return i
    return None

def run():
    file_path = filedialog.askopenfilename(title='Select mot or sto file')
    header_line = find_header_line(file_path)
    data = pd.read_csv(file_path, sep='\t', skiprows=header_line)
    print(data.head())

    # convert to csv
    output_file = file_path.replace('.mot', '.csv').replace('.sto', '.csv')
    data.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

if __name__ == '__main__':
    run()
    

