import msk_modelling_python as msk
import subprocess
import os
code_path = os.path.dirname(os.path.abspath(__file__))

def run_calibration(xml_setup_file=None, ):
    if xml_setup_file is None:
        print('Please provide the path to the xml setup file for calibration')
        return
    elif not os.path.isfile(xml_setup_file):
        print('The path provided does not exist')
        return
    
    try:        
        ceinms_install_path = os.path.join(msk.__path__[0], 'src', 'ceinms2', 'src')
        command = " ".join([ceinms_install_path + "\CEINMScalibrate.exe -S", xml_setup_file])
        print(command)
        # result = subprocess.run(command, capture_output=True, text=True, check=True)
        result = None
        return result
    except Exception as e:
        print(e)
        return None
    
if __name__ == '__main__':
    xml_setup_file = os.path.join(os.path.dirname(code_path), 'Simulations', '009_simplified', 'run_baseline', 'ceinms', 'calibration_setup.xml')
    xml_setup_file = r"C:\Git\opensim_tutorial\tutorials\repeated_sprinting\Simulations\009\pre\ceinms\calibration\calibrationSetup.xml"
    run_calibration(xml_setup_file)