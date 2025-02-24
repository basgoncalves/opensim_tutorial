import msk_modelling_python as msk
import matplotlib.pyplot as plt


mot_file = r'C:\opensim_tutorial\tutorials\repeated_sprinting\Simulations\P013\trial3_r1\Visual3d_SIMM_input.mot'
id_file = r'C:\opensim_tutorial\tutorials\repeated_sprinting\Simulations\P013\trial3_r1\inverse_dynamics.sto'
force_file = r'C:\opensim_tutorial\tutorials\repeated_sprinting\Simulations\P013\trial3_r1\Results_SO_and_MA\PC013_StaticOptimization_force.sto'

#Read .mot files
with open(mot_file, "r") as file:
    lines = file.readlines()

# Find the line where actual data starts (usually after 'endheader')
for i, line in enumerate(lines):
    if "endheader" in line:
        start_row = i + 1  # Data starts after this line
        break
else:
    start_row = 0  # If 'endheader' is not found, assume no header

# Load data using Pandas
df_ik = msk.pd.read_csv(mot_file, delim_whitespace=True, skiprows=5)
df_id = msk.pd.read_csv(id_file, sep="\t", skiprows=6)
df_force = msk.pd.read_csv(force_file, sep="\t", skiprows=14)

# df = msk.pd.read_csv(trial_path)
#msk.plot.dataFrame(df, x='time', show=True)

# Time Normalisation Function for Both df_ik and df_id
def time_normalised_df(df, fs=''):
    if not isinstance(df, msk.pd.DataFrame):
        raise Exception('Input must be a pandas DataFrame')
    
    if not fs:
        try:
            fs = 1 / (df['time'][1] - df['time'][0])  # Ensure correct time column
        except KeyError:
            raise Exception('Input DataFrame must contain a column named "time"')
        
    normalised_df = msk.pd.DataFrame(columns=df.columns)

    for column in df.columns:
        normalised_df[column] = msk.np.zeros(101)

        currentData = df[column].dropna()  # Remove NaN values

        timeTrial = msk.np.linspace(0, len(currentData) / fs, len(currentData))  # Original time points
        Tnorm = msk.np.linspace(0, timeTrial[-1], 101)  # Normalize to 101 points

        normalised_df[column] = msk.np.interp(Tnorm, timeTrial, currentData)  # Interpolate

    return normalised_df


# Apply normalisation to both IK (angles) and ID (moments) data
df_ik_normalized = time_normalised_df(df_ik)
df_id_normalized = time_normalised_df(df_id)
df_force_normalized = time_normalised_df(df_force)

# Ensure time is normalized to 101 points
time_normalized = msk.np.linspace(0, 100, 101)  
 


# Extract IK data from normalized DataFrame
ik_columns = ["hip_flexion_r", "hip_adduction_r", "hip_rotation_r", "knee_angle_r", "ankle_angle_r"]
ik_data = df_ik_normalized[ik_columns]


# Extract ID data from normalized DataFrame
id_columns = ["hip_flexion_r_moment", "hip_adduction_r_moment", "hip_rotation_r_moment", "knee_angle_r_moment", "ankle_angle_r_moment"]
id_data = df_id_normalized[id_columns]

# Extract Muscle Forces from normalized DataFrame
force_columns = ["add_long_r", "rect_fem_r", "med_gas_r", "semiten_r","tib_ant_r"]
force_data = df_force_normalized[force_columns]

# Define the layout 
fig, axes = plt.subplots(2, 5, figsize=(15, 4)) 

# Define labels for each plot
titles = ["Hip Flexion", "Hip Adduction", "Hip Rotation", "Knee Flexion", "Ankle Plantarflexion"]
titles_muscles = ["Adductor Longus", "Rectus Femoris", "Medial Gastrocnemius", "Semitendinosus", "Tibialis Anterior"]


#Plot IK (angles)
for i, col in enumerate(ik_columns):
    ax = axes[0,i]
    ax.plot(time_normalized, ik_data[col], color='red')  # Main curve
    ax.set_title(titles[i])
    ax.set_ylabel("Angle (deg)")
    ax.grid(True)

# plt.tight_layout()
# plt.show()

#Plot ID (moments)

for i, col in enumerate(id_columns):
    ax = axes[1,i]
    ax.plot(time_normalized, id_data[col], color='blue')  # Main curve
    ax.set_title(titles[i])
    ax.set_ylabel("Moment (Nm)")
    ax.set_xlabel("% Gait Cycle")
    ax.grid(True)

plt.tight_layout()
plt.show()


# **PLOT MUSCLE FORCES SEPARATELY**
fig, axes = plt.subplots(nrows=1, ncols=5, figsize=(15, 4), sharex=True)


# Plot Muscle Forces in a separate figure
for i, col in enumerate(force_columns):
    ax = axes[i]
    ax.plot(time_normalized, force_data[col], color='green')
    ax.set_title(titles_muscles[i])
    ax.set_ylabel("Force (N)")
    ax.set_xlabel("% Gait Cycle")
    ax.grid(True)

plt.tight_layout()
plt.show()
exit()

# Example of mean and sd plot

# hip_flexion_mean = df_time_normalised["hip_flexion_r"].mean  # Compute mean across trials
# hip_flexion_std = df_time_normalised["hip_flexion_r"].std()  # Compute SD

# # Plot mean curve
# plt.plot(time_normalised, hip_flexion_mean, color='red', label="Mean Hip Flexion")

# # Fill the shaded region (Mean ± 1 SD)
# plt.fill_between(time_normalised, 
#                  hip_flexion_mean - hip_flexion_std, 
#                  hip_flexion_mean + hip_flexion_std, 
#                  color='blue', alpha=0.2, label="±1 SD")

# # Formatting
# plt.xlabel("% Gait Cycle")
# plt.ylabel("Hip Flexion (deg)")
# plt.title("Hip Flexion with Standard Deviation Shading")
# plt.legend()
# plt.xlim(0, 100)
# plt.grid(True)
# plt.show()


