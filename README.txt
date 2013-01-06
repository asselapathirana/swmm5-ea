SWMM5 EA by Assela Pathirana
----------------------------
SWMM5 EA is a simple application to demonstrate how genetic algorithms can be used to solve optimization problems in the field of urban drainage. Typical problems it can solve include: Find the optimal pipe/channel sizes for a drainage network to handle a flow of a given magnitude. Sizing of SuDS systems for the same purpose. Cost-benefit optimization of interventions.

Dependancies:
-------------
SWMM5 EA has been tested only on python 2.7 (2.7.3). I noticed that python 2.7.2 multiprocessing module has a bug. If you use 2.7.2, either upgrade to 2.7.3 or use the program with  num_cpus (Number of CPUs in the Graphical interface) set to 1. 
SWMM5 EA has following dependancies. 
guidata>=1.5.1
guiqwt>=2.2.1
inspyred>=1.0
numpy>=1.6.2
PyQT>=4.8.1 
yaml>=3.10
sip>=4.11.2 
swmm5>=0.3
diff_match_patch>=20121119

Installation: 
-------------
The package can be installed in variety of ways. 
In Linux: 
a) Source distribution: SWMM5_EA-X.Y.Z.K.zip -- can be installed to the python tree with 'python setup.py install'
b) Sources:  SWMM5_EA-X.Y.Z.K.tar.gz -- includes the whole development material in addition to the distribution
c) or chcekout the project (same as b, but could be the latest version.) hg clone https://code.google.com/p/swmm5-ea/ (need Mercurial)
In Windows:
a) Install as a stand-alone software: Use the installer SWMM5_EA-X.Y.Z.K.exe
b) Install as a python package: Use SWMM5_EA-X.Y.Z.K.win32.exe
c) Source distribution: SWMM5_EA-X.Y.Z.K.zip -- can be installed to the python tree with 'python setup.py install'
d) Sources:  SWMM5_EA-X.Y.Z.K.tar.gz -- includes the whole development material in addition to the distribution
e) or chcekout the project (same as d, but could be the latest version.) hg clone https://code.google.com/p/swmm5-ea/ (need Mercurial)

Usage:
-----
If you installed swmm5ea as a stand-alone program (windows) use the start menu. 
If installed as a python package you can:
1. Double click on swmm_ea_controller.py (in Python27\Lib\site-packages\swmm5ea directory for windows)
2. Use within python as follows:
>>> from swmm5ea import swmm_ea_controller
>>> sc=swmm_ea_controller.swmmeacontroller()
>>> sc.show()



