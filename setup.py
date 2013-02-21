import sys, os
from distutils.core import setup
from itertools import product
sys.path.append("."+os.sep+os.sep+"swmm5ea")
import swmm_ea_controller as sc

with open("README.txt","r") as f:
    README=f.read()

cwd=os.path.join(os.getcwd(),"swmm5ea")
package_data=[x[len(cwd)+1:] for x in sc.LIST_OF_FILE_GLOBS ]


#package_data.append("*.pyw")
LONGDISC="""%(rm)s\n""" % { "rm": README}
setup(
    name = sc.NAME,
    packages = ["swmm5ea"],
    package_data={'swmm5ea': package_data},
    version = sc.VERSION,
    description = sc.DESCRIPTION,
    author = sc.AUTHOR,
    license=sc.LICENSE,
    #publisher=sc.PUBLISHER,
    author_email = sc.EMAIL,
    url = sc.URL,
    download_url = sc.DLURL,
    keywords = ["EPA-SWMM", "GA", "Urban Drainage"],
    classifiers = sc.CLASSIFY,
    long_description = LONGDISC
)