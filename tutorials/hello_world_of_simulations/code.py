import msk_modelling_python as msk
import tkinter as tk
from tkinter import simpledialog

def plot_sto_results(file_path='', column_names=''):
    if not file_path:
        file_path = msk.ut.select_file()
                
    results_df = msk.bp.import_sto_data(file_path)
    
    if not column_names:
        column_names = results_df.columns.tolist()
        column_names = select_from_list(column_names)
        print(column_names)
    
    # msk.bp.plot_line_df(results_df)
    pass

def select_from_list(options=[]):
    root = tk.Tk()
    root.withdraw()
    
    selected_options = []
    
    def on_select():
        for i, var in enumerate(vars):
            if var.get():
                selected_options.append(options[i])
        root.quit()
    
    vars = []
    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)
    
    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient='vertical', command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    for option in options:
        var = tk.BooleanVar()
        chk = tk.Checkbutton(scrollable_frame, text=option, variable=var)
        chk.pack(anchor='w')
        vars.append(var)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    ok_button = tk.Button(root, text="OK", command=on_select)
    ok_button.pack()
    
    root.deiconify()
    root.mainloop()
    
    return selected_options


if __name__ == '__main__':
    
    data_folder = r'C:\Git\opensim_tutorial\tutorials\repeated_sprinting'
    subject = '009'
    columns_ik = ['hip_flexion_r', 'knee_angle_r', 'ankle_angle_r']
    
    paths_baseline = msk.bops.subject_paths(data_folder=data_folder, subject_code=subject, session_name='session1', trial_name='run_baseline')
    paths_post = msk.bops.subject_paths(data_folder=data_folder, subject_code=subject, session_name='session1', trial_name='run_post_fatigue')
    print(paths_baseline.id_output)
    print(paths_post.id_output)
    
    # plot_sto_results(file_path=paths_baseline.id_output)
    import pdb; pdb.set_trace()
    ik_df = msk.bops.import_sto_data(paths_baseline.ik_output)
    print(ik_df.columns)
    msk.bops.plot_line_df(ik_df, columns_to_plot=columns_ik, legend=columns_ik)



# END