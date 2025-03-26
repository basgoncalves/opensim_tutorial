import msk_modelling_python as msk
import matplotlib.pyplot as plt
import numpy as np
import os

class File:
    def __init__(self, path):
        if not os.path.isfile(path):
            print(f"\033[93mFile not found: {path}\033[0m")
            return
        
        self.path = path
        self.name = os.path.basename(path)
        self.extension = os.path.splitext(path)[1]
        
        try:
            endheader_line = msk.classes.osimSetup.find_file_endheader_line(path)
        except:
            print(f"Error finding endheader line for file: {path}")
            endheader_line = 0
        # Read file based on extension
        try:
            if self.extension == '.csv':
                self.data = msk.pd.read_csv(path)
            elif self.extension == '.json':
                self.data = msk.bops.import_json_file(path)
            elif self.extension == '.xml':
                self.data = msk.bops.XMLTools.load(path)
            else:
                try:
                    self.data = msk.pd.read_csv(path, sep="\t", skiprows=endheader_line)
                except:
                    self.data = None
                    
            # add time range for the data
            try:
                self.time_range = [self.data['time'].iloc[0], self.data['time'].iloc[-1]]
                try:
                    self.time_range = [self.data['Time'].iloc[0], self.data['Time'].iloc[-1]]
                except:
                    pass
            except:
                self.time_range = None
        
        except Exception as e:
            print(f"Error reading file: {path}")
            print(e)
            self.data = None
            self.time_range = None
            
class Trial:
    '''
    Class to store trial information and file paths, and export files to OpenSim format
    
    Inputs: trial_path (str) - path to the trial folder
    
    Attributes:
    path (str) - path to the trial folder
    name (str) - name of the trial folder
    og_c3d (str) - path to the original c3d file
    c3d (str) - path to the c3d file in the trial folder
    markers (str) - path to the marker trc file
    grf (str) - path to the ground reaction force mot file
    ...
    
    Methods: use dir(Trial) to see all methods
    
    '''
    def __init__(self, trial_path):        
        self.path = trial_path
        self.name = os.path.basename(self.path)
        self.subject = os.path.basename(os.path.dirname(self.path))
        self.c3d = os.path.join(os.path.dirname(self.path), self.name + '.c3d')
        self.markers = File(os.path.join(self.path,'markers_experimental.trc'))
        self.grf = File(os.path.join(self.path,'Visual3d_SIMM_grf.mot'))
        self.emg = File(os.path.join(self.path,'processed_emg.mot'))
        self.ik = File(os.path.join(self.path,'Visual3d_SIMM_input.mot'))
        self.id = File(os.path.join(self.path,'inverse_dynamics.sto'))
        self.so_force = File(os.path.join(self.path,'Results_SO_and_MA', f'{self.subject}_StaticOptimization_force.sto'))
        self.so_activation = File(os.path.join(self.path, 'Results_SO_and_MA', f'{self.subject}_StaticOptimization_activation.sto'))
        self.jra = File(os.path.join(self.path,'joint_reacton_loads.sto'))
        
        # load muscle analysis files
        self.ma_targets = ['_MomentArm_', '_Length.sto']
        self.ma_files = []
        try:
            files = os.listdir(os.path.join(self.path, 'Results_SO_and_MA'))
            for file in files:
                if file.__contains__(self.ma_targets[0]) or file.__contains__(self.ma_targets[1]):
                    self.ma_files.append(File(os.path.join(self.path, 'Results_SO_and_MA', file)))
        except:
            self.ma_files = None
                    
        # settings files
        self.grf_xml = File(os.path.join(self.path,'GRF_Setup.xml'))
        self.settings_json = File(os.path.join(self.path,'settings.json'))
                              
    
    def check_files(self):
        '''
        Output: True if all files exist, False if any file is missing
        '''
        files = self.__dict__.values()
        all_files_exist = True
        for file in files:
            if not os.path.isfile(file):
                print('File not found: ' + file)
                all_files_exist = False
                
        return all_files_exist
    
    def create_settings_json(self, overwrite=False):
        if os.path.isfile(self.settings_json) and not overwrite:
            print('settings.json already exists')
            return
        
        settings_dict = self.__dict__
        msk.bops.save_json_file(settings_dict, self.settings_json)
        print('trial settings.json created in ' + self.path)
    
    def exportC3D(self):
        msk.bops.c3d_osim_export(self.og_c3d) 

    def create_grf_xml(self):
        msk.bops.create_grf_xml(self.grf, self.grf_xml)

    def print_to_json(self):
        print(msk.bops.save_json_file(self.__dict__), jsonFilePath = self.settings_json)

class openSim:
    def __init__(self, leg = 'r', subjects =['PC002','PC006','PC013'], trial_names = ['trial1','trial2','trial3'], trial_number = 1):
        self.code_path = os.path.dirname(__file__)
        self.simulations_path = os.path.join(os.path.dirname(self.code_path), 'Simulations')
        self.subjects = {}
        
        for subject in subjects:
            self.subjects[subject] = {}
            
            for trial in trial_names:                
                self.trial_path = os.path.join(self.simulations_path, subject, f'{trial}_{leg}{trial_number}')
                try:
                    self.subjects[subject][trial] = Trial(self.trial_path)
                except Exception as e:
                    self.subjects[subject][trial] =  None
                    print(f"Error loading trial: {self.trial_path}")
                    print(e)
        

        self.ik_columns = ["hip_flexion_" + leg, "hip_adduction_" + leg, "hip_rotation_" + leg, "knee_angle_" + leg, "ankle_angle_" + leg]
        self.id_columns = ["hip_flexion_" + leg + "_moment", "hip_adduction_" + leg + "_moment", "hip_rotation_" + leg + "_moment", "knee_angle_" + leg + "_moment", "ankle_angle_" + leg + "_moment"]
        self.force_columns = ["add_long_" + leg, "rect_fem_" + leg, "med_gas_" + leg, "semiten_" + leg,"tib_ant_" + leg]


        self.titles = ["Hip Flexion", "Hip Adduction", "Hip Rotation", "Knee Flexion", "Ankle Plantarflexion"]
        self.titles_muscles = ["Adductor Longus", "Rectus Femoris", "Medial Gastrocnemius", "Semitendinosus", "Tibialis Anterior"]

    # Time Normalisation Function 
    def time_normalised_df(self, df, fs=None):
        if not isinstance(df, msk.pd.DataFrame):
            raise Exception('Input must be a pandas DataFrame')
        
        if not fs:
            try:
                fs = 1 / (df['time'][1] - df['time'][0])  # Ensure correct time column
            except KeyError:
                raise Exception('Input DataFrame must contain a column named "time"')
            
        normalised_df = msk.pd.DataFrame(columns=df.columns)

        for column in df.columns:
            if column == 'time':  # Skip time column
                continue	
            normalised_df[column] = msk.np.zeros(101)

            currentData = df[column].dropna()  # Remove NaN values

            timeTrial = msk.np.linspace(0, len(currentData) / fs, len(currentData))  # Original time points
            Tnorm = msk.np.linspace(0, timeTrial[-1], 101)  # Normalize to 101 points

            normalised_df[column] = msk.np.interp(Tnorm, timeTrial, currentData)  # Interpolate

        return normalised_df

    def plot_single_trial(self, show = False):
        #Read .mot files
        with open(self.mot_file, "r") as file:
            lines = file.readlines()

        # Find the line where actual data starts (usually after 'endheader')
        for i, line in enumerate(lines):
            if "endheader" in line:
                start_row = i + 1  # Data starts after this line
                break
        else:
            start_row = 0  # If 'endheader' is not found, assume no header

        # Load data using Pandas
        self.df_ik = msk.pd.read_csv(self.mot_file, delim_whitespace=True, start_row=start_row)
        self.df_id = msk.pd.read_csv(self.id_file, sep="\t", start_row=6)
        self.df_force = msk.pd.read_csv(self.force_file, sep="\t", start_row=14)

        # Apply normalisation to both IK (angles) and ID (moments) data
        self.df_ik_normalized = self.time_normalised_df(df=self.df_ik)
        self.df_id_normalized = self.time_normalised_df(df=self.df_id)
        self.df_force_normalized = self.time_normalised_df(df=self.df_force)

        # Ensure time is normalized to 101 points
        time_normalized = msk.np.linspace(0, 100, 101)  
 
        # select the specified columns         
        self.ik_data = self.df_ik_normalized[self.ik_columns]
        self.id_data = self.df_id_normalized[self.id_columns]
        self.force_data = self.df_force_normalized[self.force_columns]
            
        # Define the layout 
        fig, axes = plt.subplots(2, 5, figsize=(15, 4)) 

        #Plot IK (angles)
        for i, col in enumerate(self.ik_columns):
            ax = axes[0,i]
            ax.plot(time_normalized, self.ik_data[col], color='red')  # Main curve
            ax.set_title(self.titles[i])
            if i == 0:
                ax.set_ylabel("Angle (deg)")
            ax.grid(True)

        #Plot ID (moments)
        for i, col in enumerate(self.id_columns):
            ax = axes[1,i]
            ax.plot(time_normalized, self.id_data[col], color='blue')  # Main curve
            ax.set_title(self.titles[i])
            if i == 0:
                ax.set_ylabel("Moment (Nm)")
            ax.set_xlabel("% Gait Cycle")
            ax.grid(True)

        plt.tight_layout()


        # PLOT MUSCLE FORCES 
        fig, axes = plt.subplots(nrows=1, ncols=5, figsize=(15, 4), sharex=True)

        for i, col in enumerate(self.force_columns):
            ax = axes[i]
            ax.plot(time_normalized, self.force_data[col], color='green')
            ax.set_title(self.titles_muscles[i])
            if i == 0:
                ax.set_ylabel("Force (N)")
            ax.set_xlabel("% Gait Cycle")
            ax.grid(True)

        plt.tight_layout()
        
        if show:
            plt.show()

    def plot_multiple_trials(self, show=False):
        self.df_ik_list = []  # Store loaded DataFrames
        
        for subject in self.subjects:
            for trial in self.subjects[subject]:
                trial_obj = self.subjects[subject][trial]
                if trial_obj:
                    self.df_ik_list.append(trial_obj.ik.data)
                    
        for file in self.mot_files:  # Loop through each file
            with open(file, "r") as f:
                lines = f.readlines()

            # Load data using Pandas
            df = msk.pd.read_csv(file, delim_whitespace=True, skiprows=5)
            self.df_ik_list.append(df)

        # Normalize all loaded IK data
        self.df_ik_normalized_list = []  # Store normalized DataFrames

        for df in self.df_ik_list:  # Loop through each loaded DataFrame
            df_normalized = self.time_normalised_df(df=df)  # Apply normalization
            self.df_ik_normalized_list.append(df_normalized)  # Store normalized DataFrame

        # Ensure time is normalized to 101 points
        time_normalized = msk.np.linspace(0, 100, 101)

        # Select the specified columns from normalized data
        self.ik_data_list = []  # Store DataFrames with only the required columns

        for df_normalized in self.df_ik_normalized_list:  # Loop through each normalized DataFrame
            if set(self.ik_columns).issubset(df_normalized.columns):  # Check if columns exist
                self.ik_data_list.append(df_normalized[self.ik_columns])  # Select only specified columns
            else:
                print("Warning: Some specified columns are missing in a file.")

        # Plot mean and sd
        # Check if IK data exists
        if not self.ik_data_list:
            print("No IK data available to plot!")
        else:
            # Convert list of DataFrames to a single NumPy array
            combined_df = np.array([df.values for df in self.ik_data_list])  # Shape: (num_trials, num_timepoints, num_columns)

            # Check if data is properly structured
            if combined_df.shape[0] < 2:
                print("Not enough trials to calculate mean and standard deviation!")
            else:
                # Compute Mean and Standard Deviation
                mean_values = np.mean(combined_df, axis=0)
                std_values = np.std(combined_df, axis=0)

                # Normalize time from 0 to 100% Gait Cycle
                time_values = np.linspace(0, 100, combined_df.shape[1])

                # Create a shared figure for all subplots
                fig, axes = plt.subplots(nrows=1, ncols=len(self.ik_columns), figsize=(20, 5), sharex=True)

                if len(self.ik_columns) == 1:
                    axes = [axes]  # If only one column, ensure it's iterable

                for i, col in enumerate(self.ik_columns):
                    ax = axes[i]

                    # Plot mean line
                    ax.plot(time_values, mean_values[:, i], color='red', label="Mean", linewidth=2)

                    # Shade the standard deviation range
                    ax.fill_between(time_values, mean_values[:, i] - std_values[:, i],
                                    mean_values[:, i] + std_values[:, i], color='red', alpha=0.2, label="SD Range")

                    # Formatting
                    ax.set_title(col)
                    ax.set_xlabel("Gait Cycle (%)")
                    ax.set_xlim(0, 100)  # X-axis from 0% to 100% of the gait cycle
                    ax.grid(True)

                    # Set Y-label only for the first subplot
                    if i == 0:
                        ax.set_ylabel("Angle (Degrees)")
                        ax.legend()


                plt.tight_layout()

                if show:
                    plt.show()


os = openSim(leg='r', subjects=['PC002', 'PC013'], trial_names=['trial2', 'trial3'], trial_number=1)
os.plot_multiple_trials(show=True)


import pdb; pdb.set_trace()
# end



