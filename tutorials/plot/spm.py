import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import spm1d

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

# simple spm ttest
# dataset = spm1d.data.uv1d.t1.Random()
# print(dataset)
# Y,mu = dataset.get_data()  #Y is (10x100), mu=0

# t = spm1d.stats.ttest(Y, mu)  #mu is 0 by default
# ti = t.inference(alpha=0.05, two_tailed=True, interp=True)
# ti.plot()

# plt.show() # has to be called to show plot
#########################################################################################################
# forces ttest
df = pd.read_csv(".\Visual3d_StaticOptimization_force.sto", sep="\t", skiprows=14)
df_time_normalised = time_normalise_df(df) 

fig, axs = plt.subplots(2)
plt.subplots_adjust(wspace=0.2, hspace =0.34, top=0.9, left=0.14, right=0.75,bottom=0.06)
axs[0].plot(df_time_normalised["rect_fem_r"], label='Rectus femoris')
axs[0].plot(df_time_normalised["vas_lat_r"], label='Vastus lateralis')
axs[0].set_xlim(0, 100)
axs[0].set_ylabel('Muscle Force [N]')
axs[0].set_xlabel("Time normalised values")
axs[0].set_title("Muscle forces (right)")
# axs[0].legend()
axs[0].legend(bbox_to_anchor=(1.4, 0.7), loc='upper right')
# Convert to numpy arrays (two different datasets)
rec_forces = np.array(df_time_normalised["rect_fem_r"])  # Rectus femoris
vastus_forces = np.array(df_time_normalised["vas_lat_r"])  # Vastus lateralis
vas_med = np.array(df_time_normalised["vas_med_r"])  
vastus_int = np.array(df_time_normalised["vas_int_r"]) 

# Ensure they are stacked correctly for SPM1D
muscle_forces = np.vstack([rec_forces, vastus_forces])
muscle_forces_vas = np.vstack([vas_med, vastus_int])


t = spm1d.stats.ttest_paired(muscle_forces, muscle_forces_vas)  #mu is 0 by default
ti = t.inference(alpha=0.05, two_tailed=True)
ti.plot() 
ti.plot_threshold_label(fontsize=8)

plt.show()


#Plotting Mean and SD 

spm1d.plot.plot_mean_sd(muscle_forces, linecolor='b', facecolor=(0.7,0.7,1), edgecolor='b', label='Rectus')
spm1d.plot.plot_mean_sd(muscle_forces_vas, linecolor='r', facecolor=(1,0.7,0.7), edgecolor='r', label='Vastus')
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper right')
plt.tight_layout()
plt.show()