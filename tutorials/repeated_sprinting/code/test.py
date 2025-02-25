from msk_modelling_python import classes
import os



current_dir = os.path.dirname(os.path.realpath(__file__))
model_path = os.path.join(current_dir, "..", "models", "009_rajagopal_scaled.osim")

tool = classes.XMLTools()
tool_ceinms = tool.ceinms()
# tool_ceinms.create_calibration_setup(save_path=os.path.join(current_dir, "calibration_setup.xml"))
# tool_ceinms.create_calibration_cfg(save_path=os.path.join(current_dir, "calibration_cfg.xml"))
tool_ceinms.create_subject_uncalibrated(osimModelFile=model_path, save_path=os.path.join(current_dir, "subject_uncalibrated.xml"))
import pdb; pdb.set_trace()
exit()
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom
import opensim as osim
import numpy as np
import pandas as pd
import msk_modelling_python as msk
import matplotlib.pyplot as plt
import screeninfo

def set_relative_figure_size(width=0.8, height=0.8):
    # Set the relative size of the figure
    fig = plt.gcf()
    screen_size = screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height
    screen_size2 = screeninfo.get_monitors()[1].width, screeninfo.get_monitors()[1].height
    import pdb; pdb.set_trace()
    fig.set_size_inches(screen_size[0] / fig.dpi * width, screen_size[1] / fig.dpi * height)


fig = plt.figure()
plt.plot([1, 2, 3, 4])
set_relative_figure_size(0.5, 0.9)
plt.show()




exit()
path = r"C:\Git\opensim_tutorial\tutorials\repeated_sprinting\models\009_rajagopal_scaled.osim"
joint_angles = r"C:\Git\opensim_tutorial\tutorials\repeated_sprinting\Simulations\009_simplified\run_baseline\ik.mot"
model = osim.Model(path)
model.initSystem()
muscles = model.getMuscles()

mtus = []
for muscle in muscles:
    mtu = {
        "name": muscle.getName(),
        "c1": "-0.5",
        "c2": "-0.5",
        "shapeFactor": "0.1",
        "optimalFibreLength": muscle.getOptimalFiberLength(),
        "pennationAngle": muscle.getPennationAngleAtOptimalFiberLength(),
        "tendonSlackLength": muscle.getTendonSlackLength(),
        "tendonSlackLength": muscle.getTendonSlackLength(),
        "maxIsometricForce": muscle.getMaxIsometricForce(),
        "strengthCoefficient": "1"
    }
    # calculate muscle force for a state
    
    muscle_states = pd.DataFrame(columns=['activation', 'fiberLength', 'fiberVelocity', 'tendonForce', 'fiberForce', 'tendonForce', 'tendonLength', 'muscleStiffness', 'fiberForce'])
    activations = np.linspace(0, 1, 100)
    
    for activation in activations:        
        state = model.initSystem()
        muscle.setActivation(state, activation)
        model.realizeDynamics(state)
        tendon_force = muscle.getTendonForce(state)
        pennation_angle = muscle.getPennationAngle(state)
        fiber_length = muscle.getFiberLength(state)
        fiber_velocity = muscle.getFiberVelocity(state)
        tendon_length = muscle.getTendonLength(state)
        muscle_stiffness = muscle.getMuscleStiffness(state)
        
        # calculate fiber force
        fiber_force = muscle.getMaxIsometricForce() * activation * np.cos(pennation_angle) * (fiber_length / muscle.getOptimalFiberLength())
        
        muscle_states.loc[len(muscle_states)] = [activation, 
                             fiber_length, 
                             fiber_velocity, 
                             tendon_force, 
                             fiber_force, 
                             tendon_force, 
                             tendon_length, 
                             muscle_stiffness,
                             fiber_force]
        
    # plot mucles states over activation
    
    msk.plot.dataFrame(muscle_states, x='activation', single_plot=False, show=True)
    import pdb; pdb.set_trace()
    print(mtu)
    exit()