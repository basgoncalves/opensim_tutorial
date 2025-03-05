import msk_modelling_python as msk
import subprocess
import os

exit()
code_path = os.path.dirname(os.path.abspath(__file__))
xml_setup_file = os.path.join(os.path.dirname(code_path), 'Simulations', '009_simplified', 'run_baseline', 'ceinms', 'calibration_setup.xml')
xml_setup_file = r'"C:\Git\opensim_tutorial\tutorials\repeated_sprinting\Simulations\009\pre\ceinms\calibration\calibrationSetup.xml"'
ceinms_install_path = os.path.join(msk.__path__[0], 'src', 'ceinms2', 'src')
command = " ".join([ceinms_install_path + "\CEINMScalibrate.exe -S", xml_setup_file])
print(command)
result = subprocess.run(command, capture_output=True, text=True, check=True)