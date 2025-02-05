# Import necessary libraries
import opensim as osim
import numpy as np
import pandas as pd
import os
import shutil
import xml.etree.ElementTree as ET

def rename_outputs():
    root_dir = "/Fatigue-prediction-MSC-Thesis"
    for root, dirs, files in os.walk("."):
        for file in files:
            path = os.path.join(root, file)
            if file.startswith(".\\"):
                new_name = file[2:]
                new_path = os.path.join(root, new_name)
                os.rename(path, new_path)
            elif file.startswith("..\\"):
                new_name = file[6:]
                new_path = os.path.join(root, new_name)
                os.rename(path, new_path)
                
def taskset_converter(file_path,*args):
    with open(file_path, 'r') as file:
        data = file.read()
        print(data)

