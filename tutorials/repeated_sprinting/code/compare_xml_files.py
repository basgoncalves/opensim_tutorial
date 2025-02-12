import os
import msk_modelling_python as msk

trial_folder = r'C:\Git\opensim_tutorial\tutorials\repeated_sprinting\Simulations\P013\trial3_r1'
exc_gen_path = os.path.join(trial_folder, 'ceinms','excitationGenerator_right.xml')
# file_path = r'C:\Git\opensim_tutorial\tutorials\repeated_sprinting\Simulations\009\pre\ceinms\excitationGenerators\excitationGenerator_2ndcal.xml'

model_path = r'C:\Git\opensim_tutorial\tutorials\repeated_sprinting\Simulations\P013\PC013_scaled.osim'
xml = msk.bops.readXML(exc_gen_path)

model_ceinms_path = os.path.join(trial_folder, 'ceinms','uncalibratedSubject.xml')
model_ceinms = msk.bops.readXML(model_ceinms_path)
mtu_set = model_ceinms.findall('.//mtu')
ceinms_muscle_names = [mtu.find('name').text for mtu in mtu_set]


for muscle in ceinms_muscle_names:
    print(muscle)    

import pdb; pdb.set_trace()

# get all excitation tags
tagname = 'excitation'
excitations =  xml.findall(f'.//{tagname}')

model = msk.osim.Model(model_path)
muscles = model.getMuscles()
forceSet = model.getForceSet()
muscle_names = [muscle.getName() for muscle in muscles]

if muscles.getSize() != len(excitations):
    print('Number of muscles in the model:', muscles.getSize())
    print('Number of excitations in the xml file:', len(excitations))
    raise ValueError('Number of muscles in the model does not match the number of excitations in the xml file')

mapping_muscles = {}
for excitation in excitations:
    current_muscle = excitation.attrib['id']
    # add to muscle mapping
    if current_muscle not in muscle_names:
        mapping_muscles[current_muscle] = False
        print(f'Muscle {current_muscle} not found in the model')
    else:
        mapping_muscles[current_muscle] = True
        

print(mapping_muscles)
import pdb; pdb.set_trace()