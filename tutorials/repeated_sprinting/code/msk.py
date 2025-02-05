import utils
import helpers
import opensim as osim
import os

# Load the model
model = osim.Model("simulations/009/static copy/009_Rajagopal2015_FAI_os4.osim")
model.initSystem()  

# utils.run_ik_tool(model, "simulations/009/Run_baselineA1_copy")

utils.run_id_tool(model, "simulations/009/Run_baselineA1_LL1")