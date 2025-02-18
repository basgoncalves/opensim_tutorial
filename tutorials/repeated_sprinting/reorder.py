import pandas as pd

# Define file paths
import os

input_file = "Simulations/P013/trial3_r1/inverse_dynamics.sto"
output_file = "Simulations/P013/trial3_r1/inverse_dynamics_ordered3.sto"

# Read the input .sto file and find header index
with open(input_file, 'r') as f:
    lines = f.readlines()

# Identify the line where column headers start
header_index = None
for i, line in enumerate(lines):
    if line.startswith("time"):  # Assuming "time" is the first column
        header_index = i
        break

# Extract metadata (everything before column headers)
metadata = lines[:header_index]

# Read the data (skip metadata but keep column headers)
df = pd.read_csv(input_file, delim_whitespace=True, skiprows=header_index)


# Define the desired column order
desired_columns = [
    "time", "pelvis_tilt_moment", "pelvis_list_moment", "pelvis_rotation_moment",
    "pelvis_tx_force", "pelvis_ty_force", "pelvis_tz_force",
    "hip_flexion_r_moment", "hip_adduction_r_moment", "hip_rotation_r_moment",
    "knee_angle_r_moment", "ankle_angle_r_moment", "subtalar_angle_r_moment",
    "mtp_angle_r_moment", "hip_flexion_l_moment", "hip_adduction_l_moment",
    "hip_rotation_l_moment", "knee_angle_l_moment", "ankle_angle_l_moment",
    "subtalar_angle_l_moment", "mtp_angle_l_moment", "lumbar_extension_moment",
    "lumbar_bending_moment", "lumbar_rotation_moment"
]

# Ensure all required columns exist
existing_columns = [col for col in desired_columns if col in df.columns]
missing_columns = [col for col in desired_columns if col not in df.columns]

# Print warning if any columns are missing
if missing_columns:
    print("Warning: The following columns are missing from the input file:", missing_columns)

# Reorder dataframe
df_reordered = df[existing_columns]

# Write the metadata and reordered data to a new file
with open(output_file, 'w') as f:
    f.writelines(metadata)  # Write metadata first
    df_reordered.to_csv(f, sep='\t', index=False)  # Write reordered data

# Print first few rows to verify
print(df_reordered.head())
