# Import necessary libraries
import opensim as osim
import numpy as np
import pandas as pd
import os
import shutil

def run_ik_tool(model, folder, marker_file = None, output_file = None, results_directory = None, task_set = None):
    # Find marker file and task set file
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".trc"):
                marker_file = os.path.join(root, file)
            elif "taskset" in file:
                task_set = os.path.join(root, file)
        # Define output file   
        output_file = os.path.join(root, "IK" + ".mot") 
        # Define results dir
        results_directory = root
    
    # Create inverse kinematics tool, set parameters and run
    ik_tool = osim.InverseKinematicsTool()
    ik_tool.setModel(model)
    ik_tool.set_marker_file(marker_file)
    ik_tool.set_output_motion_file(output_file)
    ik_tool.set_results_directory(results_directory)
    ik_task_set = osim.IKTaskSet(task_set)
    ik_tool.set_IKTaskSet(ik_task_set) 
    ik_tool.printToXML(os.path.join(folder, "setup_IK.xml"))
    ik_tool.run()


def run_id_tool(model, folder, LowpassCutoffFrequency = 6):
    
    for root, dirs, files in os.walk(folder):
        # Find coordinates file
        for file in files:
            if file == "IK.mot":
                coordinates_file = os.path.join(root, file)
        # Find external loads file
            elif file == "externalloads.xml":
                external_loads_file = os.path.join(root, file)
        # Set output file
        output_file = os.path.join(root, "ID.sto")
        # Set results directory
        results_directory = root
    
    # Setup for excluding muscles from ID
    exclude = osim.ArrayStr()
    exclude.append("Muscles")
    # Setup for setting time range
    IKData = osim.Storage(coordinates_file)

    # Create inverse dynamics tool, set parameters and run
    id_tool = osim.InverseDynamicsTool()
    id_tool.setModel(model)
    id_tool.setCoordinatesFileName(coordinates_file)
    id_tool.setExternalLoadsFileName(external_loads_file)
    id_tool.setOutputGenForceFileName(output_file)
    id_tool.setLowpassCutoffFrequency(LowpassCutoffFrequency)
    id_tool.setStartTime(IKData.getFirstTime())
    id_tool.setEndTime(IKData.getLastTime())
    id_tool.setExcludedForces(exclude)
    id_tool.setResultsDir(folder)
    id_tool.printToXML(os.path.join(folder, "setup_ID.xml"))
    id_tool.run()