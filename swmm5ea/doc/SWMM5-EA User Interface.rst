SWMM5-EA User Interface
=======================
SWMM5-EA graphical user interface is shown below. 

 .. figure:: figures/gui.png
   :alt: SWMM5-EA Graphical user interface with important toolbar buttons annotated. 
   :align: center
   :scale: 50%
   
   SWMM5-EA Graphical user interface with important toolbar buttons annotated. 
  

  
Typical Workflow
----------------
 
 Typical use of SWMM5-EA in a new problem involves following steps: 
 
  1. Create a SWMM network using SWMM 5.0 desktop application. (See :ref:`SWMM 5.0 <swmm5-label>` on how to install SWMM 5.0)
  2. Decide the decision variables (e.g. For a detention storage optimization case like :doc:`Example 1<Simple Optimization>`, this could be a variable indicating the size of each storage)
  3. Decide cost functions (e.g. In :doc:`Example 1<Simple Optimization>` this is the sum of construction cost of reservoirs and a *penalty* cost for flooding). 
  4. Create a new SWMM5-EA project. 
  5. Edit the project parameters to suitable values. 
  6. Copy the SWMM input file to the project space. (Use the button)
  7. Edit the SWMM file and introduce the place-holders (See :ref:`How SWMM5-EA exploits the input file <place_holders_label>`)
  8. Initialize the optimization (check 'output'/'Errors and Warnings' panes for any problems). 
  9. Run the Optimization
  
  