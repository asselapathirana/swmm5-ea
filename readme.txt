Debugging:
* When debugging main entrypoint should be the main function in swmm_ea_controller.py
Building Stand-alone executable
* Just run setup.py script (python setup.py)
[Preperation: First in inspyred\ec\observers.py comment out the following two imports (hack! so undo later!)
#import email
#import smtplib
2. entry point here whould be swmm5ec_.pyw (a simple script that calls swmm_ea_controller.py)
]

** when using cx_freeze (or any other freezing utility,) freeze_support calling at the top level is essential for sane operation of frozen code. 
(This is done in swmm5ec_.pyw

** VERSIONS etc: All information is kept central in swmm_ea_controller.py
** innosetup: setup.py will write the install.iss file, which can directly be compiled with innosetup. 


