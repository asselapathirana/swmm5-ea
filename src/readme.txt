build_with_cx_freeze.py can create the executable, but...
1. First in inspyred\ec\observers.py comment out the following two imports (hack! so undo later!)
#import email
#import smtplib
2. entry sint here whould be swmm5ec.pyw (a simple script that calls swmm_ea_controller.py)

When debugging with wing ide (or any other way) the entry point should be
swmm_ea_controller.py

When editing something with qt designer, use build.bat to rebuild things. This is needed to be done before and after running
qt designer. Uncomment ONLY the ui file you want to translate (the bat file hangs at first ui translate)

** when using cx_freeze (or any other freezing utility,) freeze_support calling is essential for sane operation of frozen code. 



################################
old stuff
1. May have to change project->properties->debug directory if moved (it used absolute path)
2. Run prep.bat in inspyred directory 
3. actionslots.bash <mainwindow.py> can print a set of slot functions for actions. 
2. There are two projects ex1 and gui to be compiled. ex1 set (1) as inspyred. gui set (1) as inspyred\src
3. build.bat is shared between the two. 
use build.bat to build distributable system. 
Then use install script with inno setup installer (open sourcoe) to build the installer.  


#########################
