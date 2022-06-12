SWMM5 EA by Assela Pathirana
----------------------------

SWMM5 EA is a simple application to demonstrate how genetic algorithms can be used 
to solve optimization problems in the field of urban drainage. Typical problems 
it can solve include: Find the optimal pipe/channel sizes for a drainage network to handle a 
flow of a given magnitude. Sizing of SuDS systems for the same purpose. 
Cost-benefit optimization of interventions.

SWMM5-EA Versions
-----------------
* Version 5.1.0.103 is identical source with 5.1.0.102. Only the (swmm5) binaries have been optimized. 
* Version 5.1.0.102 released to fix a bug in version 5.1.0.10. Do not use 5.1.0.10. It has compatibility problems. 

SWMM Versions
--------------

US-EPA the author of the excellent SWMM software, has the annoying practice of removing old SWMM binaries
each time they publish a new SWMM version. Old SWMM versions are not forward compatible in a straight-forward way. 
In order to avoid frustration, I am compelled to keep the newest SWMM binary that is compatible with SWMM5-EA for download. 
Download the swmm version from  https://github.com/asselapathirana/swmm5-ea/releases .


Dependencies
-------------

SWMM5 EA has been tested only on python 2.7 (2.7.6).  
SWMM5 EA has following dependencies. 

* guidata>=1.5.1
* guiqwt>=2.2.1
* inspyred>=1.0
* numpy>=1.6.2
* PyQT>=4.8.1 
* yaml>=3.10
* sip>=4.11.2 
* swmm5>=0.3
* diff_match_patch>=20121119
* pyaml

Installation: 
-------------
The package can be installed in variety of ways. 
:On Linux: 

a) Source distribution: SWMM5_EA-X.Y.Z.K.zip -- can be installed to the python tree with 'python setup.py install'
b) Sources:  SWMM5_EA-X.Y.Z.K.tar.gz -- includes the whole development material in addition to the distribution
c) Clone the latest source from github (same as b, but could be the latest version.)  https://github.com/asselapathirana/swmm5-ea/

:On Windows:

a) Install as a stand-alone software: Use the installer SWMM5_EA-X.Y.Z.K.exe  -- 
This is the recommended method if you just want to use the software. It is available at https://github.com/asselapathirana/swmm5-ea/releases .
b) Install as a python package: Use SWMM5_EA-X.Y.Z.K.win32.exe
c) Source distribution: SWMM5_EA-X.Y.Z.K.zip -- can be installed to the python tree with 'python setup.py install'
d) Sources:  SWMM5_EA-X.Y.Z.K.tar.gz -- includes the whole development material in addition to the distribution
e) Clone the latest source from github (same as b, but could be the latest version.) https://github.com/asselapathirana/swmm5-ea/

Usage:
------
If you installed swmm5ea as a stand-alone program (windows) use the start menu. 
If installed as a python package you can:

1. Double click on swmm_ea_controller.py (in Python27\Lib\site-packages\swmm5ea directory for windows)
2. Use within python as follows:

::

    >>> from swmm5ea import swmm_ea_controller
    >>> sc=swmm_ea_controller.swmmeacontroller()
    >>> sc.show()
    



