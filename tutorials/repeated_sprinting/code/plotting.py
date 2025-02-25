import msk_modelling_python as msk
import matplotlib.pyplot as plt
import numpy as np


class openSim:
    def __init__(self, leg = 'r'):
        self.leg = leg
        self.mot_file = fr'C:\opensim_tutorial\tutorials\repeated_sprinting\Simulations\PC013\trial3_{leg}1\Visual3d_SIMM_input.mot'
        self.mot_files = [
            fr'C:\opensim_tutorial\tutorials\repeated_sprinting\Simulations\PC013\trial3_{leg}1\Visual3d_SIMM_input.mot',
            fr'C:\opensim_tutorial\tutorials\repeated_sprinting\Simulations\PC006\trial2_{leg}1\Visual3d_SIMM_input.mot',
            fr'C:\opensim_tutorial\tutorials\repeated_sprinting\Simulations\PC002\trial2_{leg}1\Visual3d_SIMM_input.mot'
        ]
        self.id_file = fr'C:\opensim_tutorial\tutorials\repeated_sprinting\Simulations\PC013\trial3_{leg}1\inverse_dynamics.sto'
        self.force_file = fr'C:\opensim_tutorial\tutorials\repeated_sprinting\Simulations\PC013\trial3_{leg}1\Results_SO_and_MA\PC013_StaticOptimization_force.sto'


        self.ik_columns = ["hip_flexion_" + leg, "hip_adduction_" + leg, "hip_rotation_" + leg, "knee_angle_" + leg, "ankle_angle_" + leg]
        self.id_columns = ["hip_flexion_" + leg + "_moment", "hip_adduction_" + leg + "_moment", "hip_rotation_" + leg + "_moment", "knee_angle_" + leg + "_moment", "ankle_angle_" + leg + "_moment"]
        self.force_columns = ["add_long_" + leg, "rect_fem_" + leg, "med_gas_" + leg, "semiten_" + leg,"tib_ant_" + leg, "glut_med_avg_" + leg]
        
        self.force_data = msk.pd.read_csv(self.force_file, delim_whitespace=True, skiprows=14)  

        # Compute the average of the three gluteus medius columns
        self.force_data["glut_med_avg_" + leg] = self.force_data[["glut_med1_" + leg, "glut_med2_" + leg, "glut_med3_" + leg]].mean(axis=1)

        self.titles = ["Hip Flexion", "Hip Adduction", "Hip Rotation", "Knee Flexion", "Ankle Plantarflexion"]
        self.titles_muscles = ["Adductor Longus", "Rectus Femoris", "Medial Gastrocnemius", "Semitendinosus", "Tibialis Anterior", "Gluteus Medius"]

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
        self.df_ik = msk.pd.read_csv(self.mot_file, delim_whitespace=True, skiprows=5)
        self.df_id = msk.pd.read_csv(self.id_file, sep="\t", skiprows=6)
        self.df_force = msk.pd.read_csv(self.force_file, sep="\t", skiprows=14)

        # Compute the average of the three gluteus medius columns before normalization
        self.df_force["glut_med_avg_" + self.leg] = self.df_force[["glut_med1_" + self.leg, "glut_med2_" + self.leg, "glut_med3_" + self.leg]].mean(axis=1)

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
            ax.set_title(col.replace("_" + self.leg, "").replace("_avg", " (Avg)"))  # Rename title
            ax.set_title(self.titles[i])
            if i == 0:
                ax.set_ylabel("Angle (deg)")
            ax.set_xlim(0, 100) 
            ax.grid(True)

        #Plot ID (moments)
        for i, col in enumerate(self.id_columns):
            ax = axes[1,i]
            ax.plot(time_normalized, self.id_data[col], color='blue')  # Main curve
            ax.set_title(self.titles[i])
            if i == 0:
                ax.set_ylabel("Moment (Nm)")
            ax.set_xlabel("% Gait Cycle")
            ax.set_xlim(0, 100) 
            ax.grid(True)

        plt.tight_layout()


        # PLOT MUSCLE FORCES 
        fig, axes = plt.subplots(nrows=1, ncols=6, figsize=(15, 4), sharex=True)

        for i, col in enumerate(self.force_columns):
            ax = axes[i]
            ax.plot(time_normalized, self.force_data[col], color='green')
            ax.set_title(self.titles_muscles[i])
            if i == 0:
                ax.set_ylabel("Force (N)")
            ax.set_xlabel("% Gait Cycle")
            ax.set_xlim(0, 100) 
            ax.grid(True)

        plt.tight_layout()
        
        if show:
            plt.show()


    def plot_multiple_trials(self, show=False):
        self.df_ik_list = []  # Store loaded DataFrames
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
                    ax.set_xlim(0, 100) 
                    ax.grid(True)

                    # Set Y-label only for the first subplot
                    if i == 0:
                        ax.set_ylabel("Angle (Degrees)")
                        ax.legend()


                plt.tight_layout()

                if show:
                    plt.show()


os = openSim(leg='r')
os.plot_single_trial(show=True)



