import sys
import os

sys.path.append(".."+os.sep+os.sep+"service")

"""Create a stand-alone executable"""

try:
    from guidata.disthelpers import Distribution
except ImportError:
    raise ImportError, "This script requires guidata 1.4+"

import swmm_ea_controller as sc

def create_executable():
    """Build executable using ``guidata.disthelpers``"""
    dist = Distribution()
    dist.setup(name=sc.NAME, version=sc.VERSION,
               description=sc.DESCRIPTION,
               script="swmm5ec_.pyw", target_name="swmm5ec.exe", 
    icon="../res/DNA.ico")
    dist.add_modules('guidata', 'guiqwt')
    # Building executable
    dist.build('cx_Freeze')


if __name__ == '__main__':
    create_executable()