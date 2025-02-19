import os 
import subprocess
# import msk_modelling_python as msk
import sys
import numpy as np
import opensim as osim

class Project:
    def __init__(self, path):
        self.path = path
        self.simulations = os.path.join(path, 'Simulations')
        self.pipeline = os.path.dirname(__file__)
        

P = Project(os.path.dirname(__file__))
file_path = os.path.join(P.simulations, r'P013\trial3_r1\processed_emg_signals.csv')

emg_data = msk.bops.pd.read_csv(file_path)

fs = int(1/(emg_data['Time'][1] - emg_data['Time'][0]))

time = emg_data['Time']

# start time from new time point
start_time = 1.539
end_time = time[-1:]  - time[0] + start_time

num_samples = int((end_time - start_time) / (1/fs))
new_time = np.linspace(start_time, end_time, num_samples)

emg_data['Time'] = new_time


import pdb; pdb.set_trace()

exit()

try:
    model = osim.Model()
    print("OpenSim model created successfully!")

except Exception as e:
    print(e)


current_path = os.path.dirname(__file__)
print(current_path)
print(sys.executable)

try:
    import msk_modelling_python as msk
    msk.bops.test_bops()

    print('MSk loaded properly')
except Exception as e:
    print('ERROR:', e)

# run CEINMS
ceinms_install_path = msk.__path__[0] + '\src' + '\ceinms2' + '\src'

if os.path.exists(ceinms_install_path):
    print('CEINMS path found:', ceinms_install_path )

else:
    print('ceinms path NOT FOUND:', ceinms_install_path)
    raise FileNotFoundError


#Define the path to the main XML setup file
current_path = os.path.dirname(__file__)
xml_setup_file = os.path.normpath(os.path.join(current_path, "Simulations", "P013", "trial3_r1", "ceinms", "calibrationSetup.xml"))
print(current_path)
print(xml_setup_file)

# Construct the command
command = " ".join([ceinms_install_path + "\CEINMScalibrate.exe -S", xml_setup_file])

print(command)

if os.path.exists(xml_setup_file):
    print("XML file exists:", xml_setup_file)
else:
    print("ERROR: XML file doesn't exist:", xml_setup_file)
    sys.exit(1)

# Run the command
try:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print("Output:\n", result.stdout)
except subprocess.CalledProcessError as e:
    print("Error:\n", e)
    sys.exit(1)

result = subprocess.run(command, capture_output=True, text=True, check=True)

# try: 
#     print('Run the CEINMS executable')
#      os.system(command)
# except Exception as e:
#     print('ERROR:', e)
#     sys.exit(1)
    
    
    