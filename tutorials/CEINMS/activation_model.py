import pandas as pd

file_path =  r"C:\Git\opensim_tutorial\tutorials\repeated_sprinting\Simulations\PC002\trial2_r1\processed_emg_signals_processed.mot"

data = {
    'time': [0.0752, 0.0852, 0.0952, 0.1052, 0.1152],
    'RGLTMED': [0.003484, 0.003648, 0.003812, 0.003973, 0.004133],
    'RRF': [0.008919, 0.009174, 0.009428, 0.009682, 0.009934],
    'RADDLONG': [-0.024304, -0.021115, -0.017930, -0.014750, -0.011577],
    'RST': [0.006295, 0.006464, 0.006633, 0.006801, 0.006969],
    'RTA': [-0.001700, -0.001340, -0.000979, -0.000616, -0.000252],
    'RGM': [-0.001432, -0.000847, -0.000264, 0.000316, 0.000893]
}

emg_data = pd.DataFrame(data)
emg_data =  pd.read_csv(file_path, sep='\t', skiprows=5)

print(emg_data.head())

d = 0.015
alpha = 1
e = 0.6
C1 = 0.8
C2 = -0.5
B1 = C1 + C2
B2 = C1 * C2
A = -3 # shape factor

frame = 3
current_time = 0.0952

u = [0.01, 0.01]
a = [0, 0]
for index, irow in emg_data.iterrows():
    t = irow['time'] # current time
    e = irow['RGLTMED'] * 100# current emg value
    
    # excitation 
    u.append((alpha * e) - (C1+C2)*u[index-1] - C1*C2*u[index-2])
    
    # activation
    a.append((e**(A*u[index])-1) / (e**(A)-1))
    

# plot activation and excitation
import matplotlib.pyplot as plt
plt.figure()
plt.plot(emg_data['time'], u[2:], label='Excitation')
plt.plot(emg_data['time'], a[2:], label='Activation')

plt.xlabel('Time (s)')
plt.ylabel('Value')

plt.legend()
plt.show()
    
exit()

current_emg = emg_data.loc[frame-1, 'RGLTMED']
u_previous_2 = 0.003484
u_previous = 0.003648



# activation 
a = (current_emg**(A*u)-1) / (current_emg**(A)-1)

print('EMG value')
print(current_emg)

print('Excitation value')
print(u)

print('Activation value')
print(a)