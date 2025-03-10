import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
current_dir = os.path.dirname(__file__)

# simple plot

#plt.plot([1, 2, 3, 4])
#plt.ylabel('some numbers')
#plt.show()
################################################################################################################################################
# force plot
df = pd.read_csv(os.path.join(current_dir, "Visual3d_StaticOptimization_force.sto"), sep='\t', skiprows=14)

# print(df.to_string())
# print(df.columns)
# print(df["rect_fem_r"])

#plt.plot(df["rect_fem_r"])
#plt.ylabel('Force [N]')
#plt.xlabel("Number")
#plt.title("Rectus femoris (right)")
#plt.show()
################################################################################################################################################
# time normalised plot
def time_normalise_df(df, fs=''):

    if not type(df) == pd.core.frame.DataFrame:
        raise Exception('Input must be a pandas DataFrame')
    
    if not fs:
        try:
            fs = 1/(df['time'][1]-df['time'][0])
        except  KeyError as e:
            raise Exception('Input DataFrame must contain a column named "time"')
    
    normalised_df = pd.DataFrame(columns=df.columns)

    for column in df.columns:
        normalised_df[column] = np.zeros(101)

        currentData = df[column]
        currentData = currentData[~np.isnan(currentData)]
        
        timeTrial = np.arange(0, len(currentData)/fs, 1/fs)        
        Tnorm = np.arange(0, timeTrial[-1], timeTrial[-1]/101)
        if len(Tnorm) == 102:
            Tnorm = Tnorm[:-1]
        normalised_df[column] = np.interp(Tnorm, timeTrial, currentData)
    
    return normalised_df


df_time_normalised = time_normalise_df(df)
# 101 values 
# print(df_time_normalised)
# plt.plot(df_time_normalised["rect_fem_r"])
# plt.xlim(0, 100)
# plt.ylabel('Force [N]')
# plt.xlabel("Time normalised values")
# plt.title("Rectus femoris (right)")
# plt.show()

################################################################################################################################################
# Two plots in one graphs


# fig, ax = plt.subplots()

# ax.set_title('A single graph')
# ax.plot(df_time_normalised["rect_fem_r"])

# ax.set_title('A single graph')
# ax.plot(df_time_normalised["vas_lat_r"])

# plt.show()

################################################################################################################################################
# Two graphs in one figure


fig, ax = plt.subplots(2)

plt.subplots_adjust(wspace=0.2, hspace =0.53, top=0.9, left=0.17, right=0.82,bottom=0.1)

fig.suptitle('Two graphs')
ax[0].plot(df_time_normalised["rect_fem_r"])
ax[1].plot(df_time_normalised["vas_lat_r"])

ax[0].set_xlim(0,100)
ax[1].set_xlim(0,100)

ax[0].set_xlabel('Percentage of single leg support')
ax[0].set_ylabel('Force (N)')
ax[1].set_xlabel('Percentage of single leg support')
ax[1].set_ylabel('Force (N)')

ax[0].set_title('Rectus Femoris')
ax[1].set_title('Vastus Lateralis')
plt.show()

#Automatically saving the figure

fig.savefig(os.path.join(current_dir, "test.png"))


