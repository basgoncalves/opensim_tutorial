import os 
import subprocess
# import msk_modelling_python as msk
import sys
import opensim as osim


try:
    model = osim.Model()
    print("OpenSim model created successfully!")

except Exception as e:
    print(e)


current_path = os.path.dirname(__file__)
print(current_path)
print(sys.executable)

try:
    import msk_modelling_python as msk
    msk.bops.test_bops()

    print('MSk loaded properly')
except Exception as e:
    print('ERROR:', e)

# run CEINMS
ceinms_install_path = msk.__path__[0] + '\src' + '\ceinms2' + '\src'

if os.path.exists(ceinms_install_path):
    print('CEINMS path found:', ceinms_install_path )

else:
    print('ceinms path NOT FOUND:', ceinms_install_path)
    raise FileNotFoundError



# Define the path to the main XML setup file
xml_setup_file = r"C:\CEINMS\simulations\P013\trial3_r1\ceinms\calibrationSetup.xml"

# Construct the command
command = " ".join([ceinms_install_path + "\CEINMScalibrate.exe -S", xml_setup_file])
# command = ["CEINMScalibrate", "-S", xml_setup_file]

print(command)

# Run the command
try:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print("Output:\n", result.stdout)
except subprocess.CalledProcessError as e:
    print("Error:\n", e.stderr)
    sys.exit(1)
    
try: 
    print('Run the CEINMS executable')
    # os.system(command)
except Exception as e:
    print('ERROR:', e)
    sys.exit(1)
    