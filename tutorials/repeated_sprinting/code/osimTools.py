import os
import opensim as osim
import numpy as np
import pandas as pd
import unittest
current_dir = os.path.dirname(os.path.realpath(__file__))
simulations_dir = os.path.join(current_dir, "..", "Simulations")
if not os.path.exists(simulations_dir):
    raise Exception(f"Simulations directory not found: {simulations_dir}")

class MOT:
    def __init__(self, path=None):
        self.path = path
        try:
            self.df = pd.read_csv(path, delim_whitespace=True, skiprows=5)
        except Exception as e:
            print(f"Error loading MOT file: {e}")
            self.df = None
            
    def header(self, osim_version='4.3'):
        if osim_version.startswith('4'):
            nRows = len(self.df)
            nColumns = len(self.df.columns)
            try:
                with open(self.path, 'w') as f:
                    f.write("Normalized EMG Linear Envelopes\n")
                    f.write("nRows={}\n".format(len(df)))
                    f.write("nColumns={}\n".format(len(df.columns)))
                    f.write("endheader\n")
            except Exception as e:
                print(f"Error writing MOT file header: {e}")

    def load_mot(file_path):
        try:
            df = pd.read_csv(file_path)
            df = pd.read_csv(file_path, delim_whitespace=True, skiprows=5)
            
            
        
        except Exception as e:
            print(f"Error loading MOT file: {e}")
            return None

    def write_mot(df, file_path=None): 
        try:
            with open(file_path, 'w') as f:
                f.write("Normalized EMG Linear Envelopes\n")
                f.write("nRows={}\n".format(len(df)))
                f.write("nColumns={}\n".format(len(df.columns)))
                f.write("endheader\n")
                df.to_csv(f, sep='\t', index=False, header=True)
            print(f"File written successfully to {file_path}")
        except Exception as e:
            print(f"Error writing MOT file: {e}")

class TestOSIMTools(unittest.TestCase):
    def test_load_mot(self):
        
        example_file = os.path.join(simulations_dir, "009_from_python", "emg.mot")
        self.assertIsNotNone(load_mot(example_file))
        
if __name__ == '__main__':
    unittest.main()