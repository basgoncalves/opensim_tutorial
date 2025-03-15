import pandas as pd


## Excitation 

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

print(emg_data.head())

d = 0.015
alpha = 1
e = 0.6
C1 = 0.8
C2 = -0.5
B1 = C1 + C2
B2 = C1 * C2

frame = 3
current_time = 0.0952

current_emg = emg_data.loc[frame-1, 'RGLTMED']
u_previous_2 = 0.003484
u_previous = 0.003648

u = (alpha * current_emg) - (C1+C2)*u_previous - C1*C2*u_previous_2

print('EMG value')
print(current_emg)

print('Excitation value')
print(u)


u = [0,0]
## Activation
A = -3
a = (current_emg ** (A*u)-1)/(current_emg **(A) - 1)
print('Activation value')
print(a)


## Creating a plot

for irow in range(0, len(emg_data)):
    t = emg_data.loc[irow, 'time']
    e = emg_data.loc[irow, 'RGLTMED']

    #excitation
    u.append((alpha*e) - B1*u[irow-1] - B2*u[irow-2])

    #activation
    a.append((e**(A*u[irow])-1)/(e**A - 1))

    