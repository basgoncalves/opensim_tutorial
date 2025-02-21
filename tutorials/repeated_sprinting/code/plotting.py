import msk_modelling_python as msk

trial_path = r'C:\opensim_tutorial\tutorials\repeated_sprinting\Simulations\P013\trial3_r1\processed_emg_signals_updated.csv'
df = msk.pd.read_csv(trial_path)
msk.plot.dataFrame(df, x='Time', show=True)

def print_test():
    print("Hello World")
    return "Hello World"


# plot joint angles 