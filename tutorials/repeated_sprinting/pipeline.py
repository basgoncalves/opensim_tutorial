import os 
import subprocess
import msk_modelling_python as msk
import sys
import numpy as np
import opensim as osim

class Project:
    def __init__(self, path):
        self.path = path
        self.simulations = os.path.join(path, 'Simulations')
        self.pipeline = os.path.dirname(__file__)
    

    def header_mot(self,df,name):

        num_rows = len(df)
        num_cols = len(df.columns) 
        inital_time = df['Time'].iloc[0]
        final_time = df['Time'].iloc[-1]
        df_range = f'{inital_time}  {final_time}'


        return f'name {name}\n datacolumns {num_cols}\n datarows {num_rows}\n range {df_range} \n endheader'
    
    def csv_to_mot(self, csv_path):
        
        emg_data = msk.bops.pd.read_csv(file_path)

        fs = int(1/(emg_data['Time'][1] - emg_data['Time'][0]))

        time = emg_data['Time']

        # start time from new time point
        start_time = 1.539
        end_time = time.iloc[-1] - time.iloc[0] + start_time

        num_samples = len(emg_data)
        #num_samples = int((end_time - start_time) / (1/fs))
        new_time = np.linspace(start_time, end_time, num_samples)

        emg_data['Time'] = new_time

        # Define a new file path 
        new_file_path = os.path.join(P.simulations, r'P013\trial3_r1\processed_emg_signals_updated.csv')

        # Save the modified DataFrame
        emg_data.to_csv(new_file_path, index=False)  # index=False prevents adding an extra index column

        # save to mot
        header = P.header_mot(emg_data, "processed_emg_signals")

        mot_path = new_file_path.replace('.csv','.mot')
        with open(mot_path, 'w') as f:
            f.write(header + '\n')  
            # print column names 
            f.write('\t'.join(map(str, emg_data.columns)) + '\n')
            for index, row in emg_data.iterrows():
                f.write('\t'.join(map(str, row.values)) + '\n')  # C

    def check_osim_model(self):
        try:
            model = osim.Model()
            print("OpenSim model created successfully!")

        except Exception as e:
            print(e)

    
P = Project(os.path.dirname(__file__))
file_path = os.path.join(P.simulations, r'P013\trial3_r1\processed_emg_signals.csv')
# P.csv_to_mot(file_path)


current_path = os.path.dirname(__file__)
print(current_path)
print(sys.executable)

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

exit()
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
    
    
    