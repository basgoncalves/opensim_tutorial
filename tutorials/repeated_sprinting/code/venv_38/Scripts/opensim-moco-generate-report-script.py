#!C:\CEINMS\venv_38\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'opensim==4.3','console_scripts','opensim-moco-generate-report'
__requires__ = 'opensim==4.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('opensim==4.3', 'console_scripts', 'opensim-moco-generate-report')()
    )
