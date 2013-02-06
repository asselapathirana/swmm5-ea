Building:
--------
1. Use setup.py on top to build sdist and bdist_wininst
python setup.py sdist
python setup.py bdist_wininst
2. Use setup.py in directory "./service" to build standalone exe for windows
python setup.py (Note: no need tpo give additional option like bdist_wininst) 
It will also run innnosetup and make the installer. 
NOTE: data_files=[[dirname(x)[13:],[x]] for x in lst] line on service/setup.py is a precarious way of doing things. Fix this. 

Debugging:
* When debugging main entrypoint should be the main function in swmm_ea_controller.py
Building Stand-alone executable
* Just run setup.py script (python setup.py)
[Preperation: First in inspyred\ec\observers.py comment out the following two imports (hack! so undo later!)
#import email
#import smtplib
2. entry point here whould be swmm5ec_.pyw (a simple script that calls swmm_ea_controller.py) (for windows)
3. guidata/configtools.py has to be patched as follows: 

36c36,37
<         if osp.isfile(parentdir): 
---
>         parentdir2 = osp.split(datapath.rstrip(os.path.sep))[0]
>         if osp.isfile(parentdir) or osp.isfile(parentdir2):

(for linux)

]

** when using cx_freeze (or any other freezing utility,) freeze_support calling at the top level is essential for sane operation of frozen code. 
(This is done in swmm5ec_.pyw

** VERSIONS etc: All information is kept central in swmm_ea_controller.py
** innosetup: setup.py will write the install.iss file, which can directly be compiled with innosetup. 


