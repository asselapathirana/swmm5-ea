import re, fnmatch
import os
from itertools import product
from glob import glob
# program metadata

NAME=u"SWMM5_EA" # do not have spaces !!
VERSION="5.1.0.103"
VERSION2=VERSION[:[m.start() for m in re.finditer(r"\.",VERSION)][1]]
DESCRIPTION=u"SWMM5-EA"
LICENSE=u"License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
PUBLISHER=u"Assela Pathirana"
AUTHOR=u"Assela Pathirana"
URL="http://assela.pathirana.net/SWMM5_EA"
TARGET="swmm5ec.exe"
SETUPNAME=NAME+"-"+VERSION
PLATFORM="POSIX, WINDOWS"
EMAIL="assela@pathirana.net"
DLURL="https://github.com/asselapathirana/swmm5-ea/releases"
CLASSIFY=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Environment :: Other Environment",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta",
        "Natural Language :: English"
        ]
#LONGDISC="""\
#Optimizing Urban Drainage Networks 
#with EPA-SWMM 5.0 and Evolutionary Methods"
#
#-------------------------------------
#
#Python 2.7 version. 
#"""
head=os.path.abspath(os.path.join(os.path.dirname(__file__)))
ex_=["storage_example", "simple_reservoir_and_pipe_example", "watershed_calibration","stage_example"]
exts_=["inp", "inp_", "yaml", "cal"]
exts_.extend([x.upper() for x in exts_])
examples_=list(product(ex_,exts_))
lst=[ glob(os.path.join(head,"examples",x[0],"*."+x[1])) for x in examples_]
lst.append([os.path.join(os.path.abspath(head),"customcode","README.txt")])
LIST_OF_FILE_GLOBS=[item for sublist in lst for item in sublist]
for root, dirnames, filenames in os.walk(os.path.join(head,"doc","_build")):
  for filename in fnmatch.filter(filenames, '*'):
      LIST_OF_FILE_GLOBS.append(os.path.join(root, filename))

RUN_STATUS_TOBEINITED=0
RUN_STATUS_INITED=1
RUN_STATUS_RUNNING=2
RUN_STATUS_PAUSED=3

#
SWMMREULTSTYPE_FLOOD=0
SWMMREULTSTYPE_CALIB=1
SWMMREULTSTYPE_STAGE=2
SWMMCHOICES= [
     'Flood Volume as a cost',
     'Calibrate a variable',
     'Staged Calc. with Flood vol. as cost'
    ] 
PLOTYTITLE=[
    'Cost',
    'Error',
    'Net Present Cost'] 
SOOTITLES=[ #X and Plot itles for single objective cases
    'Generation Number',
    'Convergence Plot'] # Y title from PLOTYTITLE depending on type of SOO 

MOOTITLES=[
  "Cost 1",
  "Cost 2",
  "Pareto Front"]
SWMMCALIBRATIONFILE=[# ORDER the following appear in swmm5 gui (belive me the order there is different!)
                     1, 8, 9, 10, 
                     #2,
                     3, 6, 7, #5, 
                     4,  12, 11 
                     ]
SWMMCALIBRATIONTYPES=[# this should match with SWMMVARTYPES
    "Subcatchment Runoff",                            #0
    "Subcatchment Groundwater Flow",                  #1
    "Subcatchment Groundwater Elevation", #2
    "Subcatchment Snow Pack Depth", #3
   # "Subcatchment Pollutant Washoff (pollutant 1)", #4
    "Node Depth", #5
    "Node Lateral Inflow", #6 
    "Node Flooding", #7
    #"Node Water Quality (pollutant 1)", #8 
    "Link Flow", #9
    "Link Velocity", #10 
    "Link Depth"] #11
SWMMCALIBRATIONTYPES2=[# this should match with above and below
     'subcatchments',
     'subcatchments',
     'subcatchments',
     'subcatchments',
     #'subcatchments',
     'nodes',
     'nodes',
     'nodes',
     #'nodes',
     'links',
     'links',
     'links'] 
SWMMVARTYPES=[ # refer to swmm5 interfacing guide. This should match with SWMMCALIBRATIONTYPES
    [0,3],[0,4],[0,5],[0,1],
    #[0,6],
    [1,0],[1,3],[1,5],
    #[1,6],
    [2,0],[2,2],[2,1] 
    ]

# make sure the indexes match the values above


SWMMSTAGESEPERATOR=";;;;;;;;  STAGE %s  ;;;;;;;;  NOTE: Do not alter this line in anyway! ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;"
SWMMSTAGEMINIMUMPAT=';;;;;;;;*.*;;;;;*'
def extractSWMMmultiplefiles(string):
    return [x for x in re.split(SWMMSTAGEMINIMUMPAT,string) if x.find('[TITLE]')>-1]
