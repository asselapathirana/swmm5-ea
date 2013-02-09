Introduction to SWMM5-EA
========================
`SWMM5-EA <https://code.google.com/p/swmm5-ea/>`_ is GUI based program to demonstrate the use of evolutionary algorithms to optimize drainage networks. It suppports drainage/sewerage networks modelled in `EPA-SWMM 5.0 <http://www.epa.gov/nrmrl/wswrd/wq/models/swmm/>`_ system, based on  "`SWMM5 package: Python bindings for EPA-SWMM 5.0 engine <http://pypi.python.org/pypi/SWMM5/>`_". 

What It is
----------
SWMM5-EA was written for education, not for research. Therefore it has 

- A user friendly (=Click and Run) user interface. 
- Limited functionality so as not to overwhelm the new user. 

This should answer many questions in the form "*Why it does not have feature A ?*". 

At the moment it can demonstrate following types of applications: 

- Optimal sizing of pipes, detention storage or any other variable (or their combinations)
- Calibration of watersheds or networks based on observed data. 
- Optimal planning of staged intervention in a changing (but known) future. For example: If the rainfall increases by 1% every year, what is the optimal detention plan to be implemented at the end of each 10 year period for a system with planning horizon of 30 years? 

There are several basic examples distributed with the program. These are ready to run cases and should work as templates for new cases. 

What it is not
--------------

In its present form, it is not a research tool. Of course no one is banned from doing research with it, but please note that it has not been sufficiently tested for such applications. 

Same applies for real-world design work. 