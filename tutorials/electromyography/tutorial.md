# BIP OpenSim

Basilio Goncalves - basilio.goncalves@univie.ac.at
Hans Kainz - hans.kainz@univie.ac.at

![Alt text](.\Presentation\Snippets\1.0.2_NRG.png) 
![Alt text](.\Presentation\Snippets\1.0.2_UniVie.png)

## Required Software
-
- OpenSim (version 4.4 preferable)
- Mokka - https://biomechanical-toolkit.github.io/news/2016/10/08/mokka-new-links/
- Windows OS (tutorial works for Mac with minor adjustments)

## Useful tutorials:
- https://simtk-confluence.stanford.edu:8443/display/OpenSim/Tutorial+1+-+Intro+to+Musculoskeletal+Modeling
- https://simtk-confluence.stanford.edu:8443/display/OpenSim/Workshops+and+Events
- https://simtk-confluence.stanford.edu:8443/display/OpenSim/ESMAC+Workshop+September+2022
- https://simtk-confluence.stanford.edu:8443/display/OpenSim/Overview+of+OpenSim+Workflows#OverviewofOpenSimWorkflows-SimulationPipelines(Workflows)

# Useful tools:
- VSCode or other IDE

---
# Electromyography  

Data in - 

# 1. Inspecting EMG data

Using Mokka, loa

## 1.1 Load data

https://www.sciencedirect.com/science/article/abs/pii/S0278591920305068
hnttps://www.sciencedirect.com/science/article/abs/pii/S0021929009003169
https://www.sciencedirect.com/science/article/abs/pii/S0966636223010044


## 1.2 Muscle activity during different tasks

### Taks
- 10 meter sprint
- Side step cut

### Muscles
- VM = vastus medialis
- VL = vastus lateralis
- RF = rectus femoris
- GRA = gracilis
- TA = tibialis anterior
- ADDLONG = adductor longus
- SEMIMEM = semimembranosus
- BFLH = biceps femoris long head
- GM = gastrocnemius medialis
- GL = gastrocnemius lateralis
- TFL = tensor fasciae latae
- GLUTMAX = gluteus maximus
- GLUTMED = gluteus medius
- PIRI = piriformis
- OBTINT = obturator internus
- QF = quadratus femoris


### Questions:
- What is the maximum value 



## 1.4 Run all the steps of the simulation Gait2392 (60 min - 15h40)
- Run scale tool (subject01_Setup_Scale.xml)
- Inverse kinematics tool (subject01_Setup_Scale.xml)
- Inverse dynamics tool (subject01_Setup_Scale.xml)
- Static optimization (subject01_Setup_Scale.xml)
- Analyze tool (subject01_Setup_Analyze.xml)
- Plot simulation results for each step (load the results files first)


![Alt text](.\Presentation\Snippets\1.4.1mtu_length_hams_walking.png) 

### Questions
- What are the range of marker errors during the inverse kinematics step?
- What are the peak hip, knee, and ankle angles?
- what are the peak sagittal joint moments hip, knee, and ankle?
- What are the lat_gas and rect_fem peak forces and activation?
- What are the mtu lengths for bflh_r and soleus_r. 
- What are the maximum reserves moments hip_flexion_r, hip_adduction_r,	hip_rotation_r,	knee_angle_r,	ankle_angle_r
- What is the peak vertical component of hip contact loads, relative to participants body weight?


---
#  Medical imaging                       

# 2. Different medical imaging modalities

## 2.1 Analyse ultrasound images

## 2.2. Analysis MRI images


# 3. Muscle and joint contact forces

Calculate muscle forces during sprinting (60 min)

https://simtk-confluence.stanford.edu:8443/display/OpenSim/How+Static+Optimization+Works


## 3.1 Scaling, Inverse kinematics (20 min)
- Theory
    https://simtk-confluence.stanford.edu:8443/display/OpenSim/How+Scaling+Works
    https://simtk-confluence.stanford.edu:8443/display/OpenSim/How+Inverse+Kinematics+Works
- Load the model 
    "Tutorials\Sprinting\009\session1\"
    model name "Rajagopal_generic.osim"
- Run the scale tool using "setup_Scale_1.xml"
- Show how to adjust and apply proper scaling settings
- Go throught the problems with the scalling
    Marker errors
    Marker weights
    Scalling factors

- Scale the same model with two different sets of weights (1000 vs 500 vs 1 for anatomical landmarks)
    1. Load the model "Tutorials\Sprinting\009\session1\Rajagopal_generic.osim"
    2. Change the weights and save new setup file
    3. Run Scale tool
    4. Overlay experimental markers (right click "subject01 -> Motions -> static pose")
    5. Load subject01_Setup_IK.xml and run IK tool
    6. Assess marker errors
    7. Repeat with different weights 

    Note: Right click the models to show/hide, change offset, etc... 

### 2.2.1 Questions 
- How do marker weights change scale factors? 
- What are, approximately, total, RMS, and maximum marker errors?
- Plot hip, knee, and ankle angles
- What is the peak hip flexion angle during sprinting?
- What is the peak knee flexion angle during sprinting?
- What is the peak ankle plantarflexion angle during sprinting?
- How can you increase the trust on your results?


## 3.2 Visualize GRF and set up .xml file (15 min)
- Associate motion data "subject01_walk1_grf.mot"
- Check if the force vecotrs are syncronized with motion (if there is a delay or offset, restart opensim)
- run inverse dynamics tool 
- plot right and left ankle moments

### 2.3.1 Questions 
- How much is the peak grf relative to participant bodyweight?
- What are the peak plantar flexion moment?
- Why is the left ankle moment so much smaller compared with right?

![Alt text](.\Presentation\Snippets\2.3.1_wrong_grf_application.png)

## 3.3 Apply GRF to correct bodies (15 min)
- Load the setup_ID.xml
- Change the point of application of the forces
- run inverse dynamics tool

### 2.4.1 Questions 
- Compare hip, knee, and ankle moments
- How did moments change during stance?
- How did moments change during swing?
- Plot the residual moments (pelvis). Are they acceptable?

![Alt text](.\Presentation\Snippets\2.3.1_correct_grf_application.png)

## 3.4 Residual reduction analysis (45 min)
- Theory about RRA 
    https://simtk-confluence.stanford.edu:8443/display/OpenSim/How+RRA+Works 
- Explore the setup files for RRA tool.
    setup_RRA.xml
    actuators_RRA.xml
    tasks_RRA.xml
- Load .\Run_baseline\setup_RRA.xml and run RRATool
- Plot results for pelvis moments from .\Run_baseline\inverse_dynamics.sto
- Plot results for pelvis moments from .\Run_baseline\RRA\_Actuation_force.sto

### Questions 
- What is a residual moment?
- What are the setup files needed to run the RRA tool?
- After, RRA, What changed in the trunk segment properties?
- What is the optimal force of the actuators hip_adduction_r and MX?
- Why are the optimal forces so different between the coordinates?
- Plot the trunk, hip, knee, and ankle kinematics before and after RRA (ik.mot and .\RRA\_Kinematics_q.sto)
- What changed more hip flexion or trunk extension angles?
- How did the residual moments change after RRA?
- Are the residual moments acceptable?



## 3.5 Calculate muscle forces during sprinting (20 min)
- Load rra adjusted model 
- Explore the setup files
    setup_SO.xml
    actuators_SO.xml
- Run SO tool
- Plot muscle forces and muscle activations (bflh_r and gaslat_r)
- Adjust the model maximum isometric force of all muscles (double them)

### Questions
- What are the main 3 factors affecting muscle forces
- What is the main difference between the actuator.xml files from RRA and SO?
- What are peak force of biceps femoris and soleus muscles?
- How do the muscle activations look?
- What are the errors that show up on the messages window?
- Double the maximum isometric force of all muscles and re-run the simulations. What changed?


![Alt text](.\Presentation\Snippets\3.1.1_muscle_activations.png)

![Alt text](.\Presentation\Snippets\3.1.1_muscle_activations_large_actuators_250.png)

![Alt text](.\Presentation\Snippets\3.1.1_researves_large_actuators_250.png)


## 3.6 Calculate joint reaction loads (30 min)
- How joint reaction loads work
- Load rra ajudsted model 
- Open Analyze tool and run setup_Analyze.xml
- Plot the three components of hip contact force

### Questions
- What are the input files to calculate joint reaction loads?
- What should be the apply_on_bodies and express_in_frame inputs?
- What are the peak hip and knee joint forces in the 3 different axis?


## 3.7 Explore muscle analysis (45 min)
- plot moment arms (all the hip muscles)
- Increase the radius of wrapping surface of Gmax1_r to 0.055 and plot results again
- Do the same for one knee muscle

### Questions
- Are there any muscle moment arm dicontinuities?
- What is the hip muscle with longest length during sprinting?
