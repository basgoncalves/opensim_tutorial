import os 
import subprocess
import msk_modelling_python as msk
import sys
import numpy as np
import opensim as osim
import xml.etree.ElementTree as ET
import xml.dom.minidom
from code import plotting

plotting.print_test()

exit()

class Project:
    def __init__(self):
        self.pipeline = os.path.dirname(__file__) # pipeline path is the current directory
        self.project_path = os.path.dirname(self.pipeline) # project path is the parent directory of the pipeline
        
        if not  os.path.exists(self.project_path):
            raise FileNotFoundError('Project path not found')
        
    class Trial:
        def __init__(self, trial_path=None):
            self.pipeline = os.path.dirname(__file__)
            
            # raise PermissionError("this file is not completed. Check pipeline_implementation.txt for more details")
            
            if trial_path is not None and os.path.exists(trial_path):
                self.trial_path = trial_path
                self.trial_name = os.path.basename(trial_path)
                self.subject = self.trial_name.split('_')[0]
                
                # osim
                self.joint_angles = os.path.join(trial_path, 'Visual3d_SIMM_input.mot')  
                self.joint_moments = os.path.join(trial_path, 'inverse_dynamics.sto')
                self.muscle_forces = os.path.join(trial_path, '_StaticOptimization_force.sto')
                self.emg_mot = os.path.join(trial_path, 'processed_emg.mot')
                self.emg_csv = os.path.join(trial_path, 'processed_emg_signals.csv')
                self.osim_ExternalLoads_xml = os.path.join(trial_path, 'Visual3d_SIMM_grf.mot')
                self.osim_MuscleAnalysis_folder = os.path.join(trial_path, 'Results_SO_and_MA')
                try:
                    self.osim_MuscleAnalysis_files = os.listdir(self.osim_MuscleAnalysis_folder)
                except FileNotFoundError:
                    print('Muscle analysis folder not found:', self.osim_MuscleAnalysis_folder)
                    self.osim_MuscleAnalysis_files = []

                # ceinms
                self.ceinms_inputData_xml = os.path.join(trial_path,'ceinms', 'inputData.xml') # old "trials.xml"
                self.ceinms_subjetc_uncalibrate_xml = os.path.join(trial_path,'ceinms', 'subject_uncalibrated.xml')
                self.ceinms_subjetc_calibrate_xml = os.path.join(trial_path,'ceinms', 'subject_calibrated.xml')
                self.ceinms_excitationGenerator_xml = os.path.join(trial_path,'ceinms', 'excitationGenerator.xml')
                self.ceinms_calibration_xml = os.path.join(trial_path,'ceinms', 'calibration.xml')
                self.ceinms_calibrationSetup_xml = os.path.join(trial_path,'ceinms', 'ceinmsCalibration.xml')
                self.ceinms_execution_xml = os.path.join(trial_path,'ceinms', 'execution.xml')
                self.ceinms_ceinms_xml = os.path.join(trial_path,'ceinms', 'ceinms.xml')
                self.ceinms_contactModel_xml = os.path.join(trial_path,'ceinms', 'contactModel.xml')
            else:
                raise FileNotFoundError('Trial path not found')
        
        def check_and_fix_names(self):
            names_dict = {
                'calibrated_subject.xml': 'subject_calibrated.xml',
                'uncalibratedSubject.xml': 'subject_uncalibrated.xml',
                'trial_right.xml': 'inputData.xml',
                'excitationGenerator_right_updated.xml': 'excitationGenerator.xml',
                'calibrationCfg.xml': 'calibration.xml',
                'calibrationSetup.xml': 'ceinmsCalibration.xml',
                'execution_cfg.xml': 'execution.xml',
                'exe_setup': 'ceinms.xml'
            }

            # Iterate through the dictionary to rename files
            for old_name, new_name in names_dict.items():
                old_path = os.path.join(self.trial_path, old_name)
                new_path = os.path.join(self.trial_path, new_name)

                # Check if the old file exists before renaming
                if os.path.exists(old_path):
                    # Prevent overwriting if the new file name already exists
                    if os.path.exists(new_path):
                        print(f"Warning: {new_name} already exists. Skipping rename.")
                    else:
                        try:
                            os.rename(old_path, new_path)
                            print(f" Renamed: {old_name} → {new_name}")
                        except PermissionError:
                            print(f"Error: Permission denied when renaming {old_name}.")
                else:
                    print(f"Error: {old_name} not found. Skipping.")
       
        def save_pretty_xml(tree, file_path):
            """Saves the XML tree to a file with proper indentation."""
            # Convert to string and format with proper indents
            rough_string = ET.tostring(tree.getroot(), 'utf-8')
            reparsed = xml.dom.minidom.parseString(rough_string)
            pretty_xml = reparsed.toprettyxml(indent="   ")

            # Write to file
            with open(file_path, 'w') as file:
                file.write(pretty_xml)

        def create_trial_ceinms_xml(self):
            """Creates a template XML with the input string replacing a specific text element.

            Args:
                input_string: The string to be inserted into the XML.
            """

            ma_path = self.osim_MuscleAnalysis_folder
            emg_path = self.emg_mot
            ik_file_path = self.joint_angles
            id_file_path = self.joint_moments
            grf_xml_path = self.osim_ExternalLoads_xml
            
            # save xml path 
            input_data_file_path = self.ceinms_inputData_xml

            # Create the root element
            inputData = ET.Element("inputData")

            # Creatte tendon length tag
            tendon_length_file_path = [file for file in self.osim_MuscleAnalysis_files if '_MuscleAnalysis_FiberLength.sto' in file][0]
            tendonLengthFile_tag = ET.SubElement(inputData, "tendonLengthFile")
            muscleTendonLengthFile_tag = ET.SubElement(inputData, "muscleTendonLengthFile")
            muscleTendonLengthFile_tag.text = os.path.relpath(tendon_length_file_path, os.path.dirname(input_data_file_path))

            # Create excitationsFile tag
            excitationsFile = ET.SubElement(inputData, "excitationsFile")
            excitationsFile.text = os.path.relpath(emg_path, os.path.dirname(input_data_file_path))

            # Create momentArmsFile elements
            momentArmsFiles = ET.SubElement(inputData, "momentArmsFiles")

            leg = leg.lower()[0]
            dofNames = [f"ankle_angle_{leg}", f'knee_angle_{leg}', f'hip_flexion_{leg}']

            for dofName in dofNames:
                moment_arm_file_path = self.osim_MuscleAnalysis_folder + f'/{dofName}_MuscleAnalysis_momentArm.sto'
                print(moment_arm_file_path)
                momentArmsFile = ET.SubElement(momentArmsFiles, "momentArmsFile", dofName=dofName)
                momentArmsFile.text = os.path.relpath(moment_arm_file_path, os.path.dirname(input_data_file_path))

            # Create externalTorquesFile tag
            externalTorquesFile_tag = ET.SubElement(inputData, "externalTorquesFile")
            externalTorquesFile_tag.text = os.path.relpath(id_file_path, os.path.dirname(input_data_file_path))

            # externalLoadsFile
            externalLoadsFile_tag = ET.SubElement(inputData, "externalLoadsFile")
            externalLoadsFile_tag.text = os.path.relpath(grf_xml_path, os.path.dirname(input_data_file_path))

            # motion file
            motionFile_tag = ET.SubElement(inputData, "motionFile")
            motionFile_tag.text = os.path.relpath(ik_file_path, os.path.dirname(input_data_file_path))

            # Create an ElementTree object
            tree = ET.ElementTree(inputData)

            # Save the XML using pretty-printing
            self.save_pretty_xml(tree, input_data_file_path)

            # Write the XML to a file
            #tree.write(ceinms_trial_xml_path, encoding="utf-8", xml_declaration=True)

            print(f"Template XML created: {input_data_file_path}")
        
        def header_mot(self,df,name):

            num_rows = len(df)
            num_cols = len(df.columns) 
            inital_time = df['Time'].iloc[0]
            final_time = df['Time'].iloc[-1]
            df_range = f'{inital_time}  {final_time}'


            return f'name {name}\n datacolumns {num_cols}\n datarows {num_rows}\n range {df_range} \n endheader'
        
        def csv_to_mot(self):
            
            emg_data = msk.bops.pd.read_csv(self.emg_csv)

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

        def make_time_from_zero(self, df):
            time = df['Time']
            start_time = time.iloc[0]
            end_time = time.iloc[-1] - time.iloc[0]
            new_time = time - start_time
            df['Time'] = new_time
            return df
        
        def time_range(self, var_name):
            storage = msk.osim.Storage(self.__getattribute__(var_name))
            return storage.getFirstTime(), storage.getLastTime()
      
P = Project()      
trial_path = r'C:\Git\opensim_tutorial\tutorials\repeated_sprinting\Simulations\009_simplified'
trial = P.Trial(trial_path)
import pdb; pdb.set_trace()         
import os
      
current_path = os.path.dirname(__file__)
trial_path = os.path.join(current_path,'Simulations', 'P013', 'trial3_r1')

if not os.path.exists(trial_path):
    raise FileNotFoundError('File not found:', trial_path)

trial = Project.Trial(trial_path)

# check if files have same time range
range_ik = trial.time_range('joint_angles')
range_id = trial.time_range('joint_moments')
if not range_ik == range_id:
    raise ValueError('Time ranges are not equal:', range_ik, range_id)

f2 = r"C:\Git\opensim_tutorial\tutorials\repeated_sprinting\Simulations\009\pre\inverseKinematics\Run_baseline1\IK.mot"

import pdb; pdb.set_trace()

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
xml_setup_file = os.path.normpath(os.path.join(current_path, "Simulations", "009_simplified", "run_baseline", "ceinms","calibration_setup.xml"))
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
    
    
    