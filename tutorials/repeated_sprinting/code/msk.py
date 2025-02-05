import utils
import helpers
import opensim as osim
import os

# Load the model
model = osim.Model("tutorials/repeated_sprinting/Simulations/009/session1/rajagopal_scaled.osim")
model.initSystem()  

utils.run_ik_tool(model, "tutorials/repeated_sprinting/Simulations/009/session1/run_baseline")

# utils.run_id_tool(model, "simulations/009/Run_baselineA1_LL1")