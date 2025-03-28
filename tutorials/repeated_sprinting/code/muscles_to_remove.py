import utils
import helpers
import opensim as osim
import os
import msk_modelling_python
# Load the model
# model = osim.Model(r"C:\Git\opensim_tutorial\tutorials\repeated_sprinting\Simulations\TD006\TD006_scaled.osim")
model = osim.Model(r"C:\Git\opensim_tutorial\tutorials\repeated_sprinting\Simulations\009\pre\009_Rajagopal2015_FAI_rra_opt_N10_v4.osim")
model.initSystem()  
mvic = []
sum_mvic = 0
# run through the muscles and print max isometric force and moment arm at rest
for i in range(model.getMuscles().getSize()):
    muscle = model.getMuscles().get(i)
    mvic.append(muscle.getMaxIsometricForce())
    sum_mvic = sum_mvic + mvic[-1]

# Calculate maximum moments
max_moments = []
for i in range(model.getMuscles().getSize()):
    muscle = model.getMuscles().get(i)
    moment_arm = muscle.getGeometryPath().getLength(model.initSystem())  # Assuming moment arm is the length of the path at rest
    max_moment = muscle.getMaxIsometricForce() * moment_arm
    max_moments.append(max_moment)

# check which muscles have less maximum moment than 10% of the total maximum moment
muscles_to_remove = []
for i in range(model.getMuscles().getSize()):
    muscle = model.getMuscles().get(i)
    if max_moments[i] < 0.05 * max(max_moments):
        muscles_to_remove.append(muscle.getName())

print("Muscles to remove:")
print(muscles_to_remove)

import matplotlib.pyplot as plt

# Plot the maximum moments
plt.figure(figsize=(10, 6))
plt.bar(range(len(max_moments)), max_moments, tick_label=[model.getMuscles().get(i).getName() for i in range(model.getMuscles().getSize())])
plt.xlabel('Muscles')
plt.ylabel('Maximum Moment')
plt.title('Maximum Moments of Muscles')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()