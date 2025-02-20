import os
import xml.etree.ElementTree as ET
import xml.dom.minidom
from . import msk


subject = 'PC013'
leg = 'right'
trial_name = "Trial3"
ceinms_path = f'{subject}\\ceinms'
trial_path = f'{subject}\\ Trials\\{trial_name} (Best)'
ceinms_trial_xml_path = os.path.join(ceinms_path, "ceinms_trial.xml")
create_trial_ceinms_xml(trial_path, subject, trial_name,  ceinms_trial_xml_path, leg)