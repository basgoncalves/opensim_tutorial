import msk_modelling_python as msk
import matplotlib.pyplot as plt


mot_file = r'C:\opensim_tutorial\tutorials\repeated_sprinting\Simulations\P013\trial3_r1\Visual3d_SIMM_input.mot'

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
df = msk.pd.read_csv(mot_file, delim_whitespace=True, skiprows=start_row)

# df = msk.pd.read_csv(trial_path)
#msk.plot.dataFrame(df, x='time', show=True)

# Time Normalisation Function
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
        Tnorm = msk.np.linspace(0, timeTrial[-1], 101)  # Normalise to 101 points

        normalised_df[column] = msk.np.interp(Tnorm, timeTrial, currentData)  # Interpolate

    return normalised_df

#Apply normalisation
df_time_normalised = time_normalised_df(df)

# Extract data
time_normalised = msk.np.linspace(0, 100, 101)  


# Extract IK data from normalized DataFrame
ik_columns = ["hip_flexion_r", "hip_adduction_r", "hip_rotation_r", "knee_angle_r", "ankle_angle_r"]
ik_data = df_time_normalised[ik_columns]

# Define the layout 
fig, axes = plt.subplots(1, 5, figsize=(15, 4)) 

# Define labels for each plot
ik_titles = ["Hip Flexion", "Hip Adduction", "Hip Rotation", "Knee Flexion", "Ankle Plantarflexion"]


#Plot IK (angles)
for i, col in enumerate(ik_columns):
    ax = axes[i]
    ax.plot(time_normalised, ik_data[col], color='red')  # Main curve
    ax.set_title(ik_titles[i])
    ax.set_ylabel("Angle (deg)")
    ax.set_xlabel("% Gait Cycle")
    ax.grid(True)

plt.tight_layout()
plt.show()

# Example of mean and sd plot
# Extract Hip Flexion Data (already time-normalized)
hip_flexion_mean = df_time_normalised["hip_flexion_r"].mean  # Compute mean across trials
hip_flexion_std = df_time_normalised["hip_flexion_r"].std()  # Compute SD

# Plot mean curve
plt.plot(time_normalised, hip_flexion_mean, color='red', label="Mean Hip Flexion")

# Fill the shaded region (Mean ± 1 SD)
plt.fill_between(time_normalised, 
                 hip_flexion_mean - hip_flexion_std, 
                 hip_flexion_mean + hip_flexion_std, 
                 color='blue', alpha=0.2, label="±1 SD")

# Formatting
plt.xlabel("% Gait Cycle")
plt.ylabel("Hip Flexion (deg)")
plt.title("Hip Flexion with Standard Deviation Shading")
plt.legend()
plt.xlim(0, 100)
plt.grid(True)
plt.show()