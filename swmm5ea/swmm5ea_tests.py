import unittest
import swmm5ec as sec
import swmm_ea_controller as con
from swmm5 import swmm5 as sw
import swmmeaproject as sp
import shutil
import slotdiff
import sys

class test_calibration(unittest.TestCase):
    """This class tests the calibration functionality of swmm5ea. It tests only the calculation engine. Not the GUI part"""
    @unittest.skipIf('-noswmm' in sys.argv,\
                         'Skipping swmm test')    
    def setUp(self):
        with open("test.inp", "w") as f:
            f.write(inputfile) 
        ret=sw.RunSwmmDll("test.inp","test.rpt","test.bin")
        #shutil.copy2("test.inp","test.inp_")
        self.assertEqual(ret,0) # run was without problems we are ready to use that results. 


    
    def test_unchanging_input(self):
        """Assets that the 'fitness' should be nearly perfect if we 'recycle' the output of a swmm input file as calibration data 
        and keep the input file unaffected by GA input"""
        
        for i in range(len(con.SWMMCALIBRATIONTYPES)):
            ret=sw.OpenSwmmOutFile("test.bin")
            self.assertEqual(ret,0)            
            print "\nTesting: ", con.SWMMCALIBRATIONTYPES[i]+"\n"
            calibdata=[]
            print "Retriving : ", con.SWMMVARTYPES[i][0],1,con.SWMMVARTYPES[i][1]
            for j in range(sw.cvar.SWMM_Nperiods):
                
                ret,z=sw.GetSwmmResult(con.SWMMVARTYPES[i][0],1,con.SWMMVARTYPES[i][1],
                                           j+1) #swmmm counts from 1! 
                calibdata.append(z+2.0)
            # now we have some 'calib data'. So test whether GA will treat it nicely!
            p=sp.parameters_class_()
            p.num_inputs=5
            p.swmmResultCodes=[con.SWMMVARTYPES[i][0],1,con.SWMMVARTYPES[i][1]]
            fillers=[23,24.343,332.22,332.3,3.2]
            p.valuerange=[[1,2]]*5
            p.projectdirectory="."
            p.swmmouttype=[con.SWMMREULTSTYPE_CALIB, con.SWMMCHOICES[con.SWMMREULTSTYPE_CALIB]]
            p.calibdata=calibdata
            f=sec.getFitness(fillers,inputfile,p)
            sw.CloseSwmmOutFile()
            self.assertAlmostEqual(f,2*360.)
            


class test_diffSWMM(unittest.TestCase):
    """Functionality of diff utility used to compare *.inp file with *.inp_ (slotted) file. diff_patch_match utility is 
    versatile, but can have some fuzzy errors."""
    def setUp(self):
        self.sd=slotdiff.slotDiff(None,None)
        
    def test_same_file(self):
        """same file for both inp and inp_ should result in a True comparision"""
        self.assertTrue(self.sd.testDiffStr(inputfile,inputfile, verbose=True))
    def test_with_wrong_slot(self):
        """same file for both inp and inp_ should result in a True comparision"""
        self.assertFalse(self.sd.testDiffStr(wronginput1,tinyinput))    
        self.assertFalse(self.sd.testDiffStr(wronginput2,tinyinput))
    def test_with_unrelated(self):
        """Unrelated files should not compare True"""
        self.assertFalse(self.sd.testDiffStr(slotfile,tinyinput)) 
        self.assertFalse(self.sd.testDiffStr(rightinput1,inputfile))
    def test_with_right_slots1(self):
        """ Compare Slotted file with right input with corressponding input"""
        self.assertTrue(self.sd.testDiffStr(rightinput1,tinyinput, verbose=True))
    def test_with_right_slots2(self):
        """ Compare Slotted file with right input with corressponding input"""
        self.assertTrue(self.sd.testDiffStr(slotfile,inputfile, verbose=True))
def main_function():
    try:
            sys.argv.remove('-noswmm')
    except ValueError:
        pass    
    unittest.main()
    
tinyinput="""
;;Name           Type      Intrvl Catch  Source    
;;-------------- --------- ------ ------ ----------
Gage1            VOLUME   0:03   1.0    TIMESERIES ABM10yrs2hrs    

[SUBCATCHMENTS]
"""
rightinput1="""
;;Name           Type      Intrvl Catch  Source    
;;-------------- --------- ------ ------ ----------
Gage1            VOLUME   0:03   @!v10!@    TIMESERIES ABM10yrs2hrs    

[SUBCATCHMENTS]
"""
wronginput1="""
;;Name           Type      Intrvl Catch  Source    
;;-------------- --------- ------ ------ ----------
Gage1            VOLUME   @!v1!@   1.0    TIMESERIES ABM10yrs2hrs    

[SUBCATCHMENTS]
"""
wronginput2="""
;;Name           Type      Intrvl Catch  Source    
;;-------------- --------- ------ ------ ----------
Gage1            @!v1!@   0:03   1.0    TIMESERIES ABM10yrs2hrs    

[SUBCATCHMENTS]
"""



    
slotfile="""
[TITLE]

[OPTIONS]
FLOW_UNITS           LPS
INFILTRATION         CURVE_NUMBER
FLOW_ROUTING         DYNWAVE
START_DATE           10/28/2011
START_TIME           00:00:00
REPORT_START_DATE    10/28/2011
REPORT_START_TIME    00:00:00
END_DATE             10/28/2011
END_TIME             06:00:00
SWEEP_START          01/01
SWEEP_END            12/31
DRY_DAYS             0
REPORT_STEP          00:01:00
WET_STEP             00:01:00
DRY_STEP             00:01:00
ROUTING_STEP         0:00:01 
ALLOW_PONDING        NO
INERTIAL_DAMPING     PARTIAL
VARIABLE_STEP        0.75
LENGTHENING_STEP     0
MIN_SURFAREA         0
NORMAL_FLOW_LIMITED  SLOPE
SKIP_STEADY_STATE    NO
FORCE_MAIN_EQUATION  H-W
LINK_OFFSETS         DEPTH
MIN_SLOPE            0

[EVAPORATION]
;;Type       Parameters
;;---------- ----------
CONSTANT     0.0
DRY_ONLY     NO

[RAINGAGES]
;;               Rain      Time   Snow   Data      
;;Name           Type      Intrvl Catch  Source    
;;-------------- --------- ------ ------ ----------
Gage1            VOLUME   0:03   @!v1!@    TIMESERIES ABM10yrs2hrs    

[SUBCATCHMENTS]
;;                                                 Total    Pcnt.             Pcnt.    Curb     Snow    
;;Name           Raingage         Outlet           Area     Imperv   Width    Slope    Length   Pack    
;;-------------- ---------------- ---------------- -------- -------- -------- -------- -------- --------
E1               Gage1            J8               120      42       @!v274!@ 2.16142032087 0                        
1                Gage1            4                120      42       @!v3!@ @!v4!@ 0                        
2                Gage1            3                120      42       16047.2742455 2.16142032087 0                        

[SUBAREAS]
;;Subcatchment   N-Imperv   N-Perv     S-Imperv   S-Perv     PctZero    RouteTo    PctRouted 
;;-------------- ---------- ---------- ---------- ---------- ---------- ---------- ----------
E1               @!v3!@ @!v3!@ @!v3!@ @!v3!@ 25         OUTLET    
1                0.156646244473 0.203077120449 1.64517849588 3.43542982182 25         OUTLET    
2                0.156646244473 0.203077120449 1.64517849588 3.43542982182 25         OUTLET    

[INFILTRATION]
;;Subcatchment   CurveNum   HydCon     DryTime   
;;-------------- ---------- ---------- ----------
E1               70         0.5        7         
@!v3!@                70         0.5        7         
2                70         0.5        7         

[JUNCTIONS]
;;               Invert     Max.       Init.      Surcharge  Ponded    
;;Name           Elev.      Depth      Depth      Depth      Area      
;;-------------- ---------- ---------- ---------- ---------- ----------
J8               23.459     3          0          0          0         
3                0          0          0          0          0         
4                @!v0!@          0          0          0          0         

[OUTFALLS]
;;               Invert     Outfall    Stage/Table      Tide
;;Name           Elev.      Type       Time Series      Gate
;;-------------- ---------- ---------- ---------------- ----
J12              15.649     FREE                        NO

[CONDUITS]
;;               Inlet            Outlet                      Manning    Inlet      Outlet     Init.      Max.      
;;Name           Node             Node             Length     N          Offset     Offset     Flow       Flow      
;;-------------- ---------------- ---------------- ---------- ---------- ---------- ---------- ---------- ----------
T5               J8               J12              235        @!0.0*v1+0.01*v2+max(v1,v3)*0.01!@       0          0          0          0         
1                J8               3                400        0.01       0          0          0          0         
2                J8               4                400        0.01       0          0          0          0         

[XSECTIONS]
;;Link           Shape        Geom1            Geom2      Geom3      Geom4      Barrels   
;;-------------- ------------ ---------------- ---------- ---------- ---------- ----------
T5               RECT_OPEN    @!.4*v1!@               3          0          0          1                    
1                CIRCULAR     1                0          0          0          1                    
2                CIRCULAR     1                0          0          0          1                    

[LOSSES]
;;Link           Inlet      Outlet     Average    Flap Gate 
;;-------------- ---------- ---------- ---------- ----------

[TIMESERIES]
;;Name           Date       Time       Value     
;;-------------- ---------- ---------- ----------
;2hr
2hrRainfall                 0:00       0.00      
2hrRainfall                 0:01       0.12      
2hrRainfall                 0:02       0.12      
2hrRainfall                 0:03       0.12      
2hrRainfall                 0:04       0.12      
2hrRainfall                 0:05       0.12      
2hrRainfall                 0:06       0.13      
2hrRainfall                 0:07       0.13      
2hrRainfall                 0:08       0.13      
2hrRainfall                 0:09       0.14      
2hrRainfall                 0:10       0.13      
2hrRainfall                 0:11       0.14      
2hrRainfall                 0:12       0.15      
2hrRainfall                 0:13       0.15      
2hrRainfall                 0:14       0.14      
2hrRainfall                 0:15       0.16      
2hrRainfall                 0:16       0.16      
2hrRainfall                 0:17       0.16      
2hrRainfall                 0:18       0.17      
2hrRainfall                 0:19       0.17      
2hrRainfall                 0:20       0.17      
2hrRainfall                 0:21       0.17      
2hrRainfall                 0:22       0.18      
2hrRainfall                 0:23       0.19      
2hrRainfall                 0:24       0.19      
2hrRainfall                 0:25       0.2       
2hrRainfall                 0:26       0.2       
2hrRainfall                 0:27       0.2       
2hrRainfall                 0:28       0.21      
2hrRainfall                 0:29       0.22      
2hrRainfall                 0:30       0.23      
2hrRainfall                 0:31       0.23      
2hrRainfall                 0:32       0.24      
2hrRainfall                 0:33       0.25      
2hrRainfall                 0:34       0.26      
2hrRainfall                 0:35       0.27      
2hrRainfall                 0:36       0.28      
2hrRainfall                 0:37       0.29      
2hrRainfall                 0:38       0.3       
2hrRainfall                 0:39       0.31      
2hrRainfall                 0:40       0.33      
2hrRainfall                 0:41       0.35      
2hrRainfall                 0:42       0.37      
2hrRainfall                 0:43       0.39      
2hrRainfall                 0:44       0.41      
2hrRainfall                 0:45       0.43      
2hrRainfall                 0:46       0.46      
2hrRainfall                 0:47       0.5       
2hrRainfall                 0:48       0.53      
2hrRainfall                 0:49       0.57      
2hrRainfall                 0:50       0.62      
2hrRainfall                 0:51       0.67      
2hrRainfall                 0:52       0.74      
2hrRainfall                 0:53       0.81      
2hrRainfall                 0:54       0.91      
2hrRainfall                 0:55       1.02      
2hrRainfall                 0:56       1.17      
2hrRainfall                 0:57       1.34      
2hrRainfall                 0:58       1.58      
2hrRainfall                 0:59       1.89      
2hrRainfall                 1:00       2.34      
2hrRainfall                 1:01       2.1       
2hrRainfall                 1:02       1.73      
2hrRainfall                 1:03       1.45      
2hrRainfall                 1:04       1.24      
2hrRainfall                 1:05       1.08      
2hrRainfall                 1:06       0.96      
2hrRainfall                 1:07       0.86      
2hrRainfall                 1:08       0.78      
2hrRainfall                 1:09       0.7       
2hrRainfall                 1:10       0.65      
2hrRainfall                 1:11       0.59      
2hrRainfall                 1:12       0.55      
2hrRainfall                 1:13       0.51      
2hrRainfall                 1:14       0.48      
2hrRainfall                 1:15       0.45      
2hrRainfall                 1:16       0.43      
2hrRainfall                 1:17       0.39      
2hrRainfall                 1:18       0.38      
2hrRainfall                 1:19       0.36      
2hrRainfall                 1:20       0.34      
2hrRainfall                 1:21       0.33      
2hrRainfall                 1:22       0.32      
2hrRainfall                 1:23       0.3       
2hrRainfall                 1:24       0.29      
2hrRainfall                 1:25       0.27      
2hrRainfall                 1:26       0.26      
2hrRainfall                 1:27       0.26      
2hrRainfall                 1:28       0.24      
2hrRainfall                 1:29       0.24      
2hrRainfall                 1:30       0.23      
2hrRainfall                 1:31       0.22      
2hrRainfall                 1:32       0.22      
2hrRainfall                 1:33       0.21      
2hrRainfall                 1:34       0.2       
2hrRainfall                 1:35       0.2       
2hrRainfall                 1:36       0.19      
2hrRainfall                 1:37       0.18      
2hrRainfall                 1:38       0.18      
2hrRainfall                 1:39       0.18      
2hrRainfall                 1:40       0.17      
2hrRainfall                 1:41       0.17      
2hrRainfall                 1:42       0.16      
2hrRainfall                 1:43       0.16      
2hrRainfall                 1:44       0.15      
2hrRainfall                 1:45       0.15      
2hrRainfall                 1:46       0.15      
2hrRainfall                 1:47       0.15      
2hrRainfall                 1:48       0.14      
2hrRainfall                 1:49       0.14      
2hrRainfall                 1:50       0.14      
2hrRainfall                 1:51       0.14      
2hrRainfall                 1:52       0.13      
2hrRainfall                 1:53       0.13      
2hrRainfall                 1:54       0.13      
2hrRainfall                 1:55       0.13      
2hrRainfall                 1:56       0.13      
2hrRainfall                 1:57       0.12      
2hrRainfall                 1:58       0.12      
2hrRainfall                 1:59       0.12      
2hrRainfall                 2:00       0.11      

;Rainfall Data
ABM10yrs2hrs                0:00       0         
ABM10yrs2hrs                0:03       0.36      
ABM10yrs2hrs                0:06       0.38      
ABM10yrs2hrs                0:09       0.40      
ABM10yrs2hrs                0:12       0.42      
ABM10yrs2hrs                0:15       0.45      
ABM10yrs2hrs                0:18       0.48      
ABM10yrs2hrs                0:21       0.52      
ABM10yrs2hrs                0:24       0.56      
ABM10yrs2hrs                0:27       0.61      
ABM10yrs2hrs                0:30       0.67      
ABM10yrs2hrs                0:33       0.74      
ABM10yrs2hrs                0:36       0.82      
ABM10yrs2hrs                0:39       0.93      
ABM10yrs2hrs                0:42       1.08      
ABM10yrs2hrs                0:45       1.27      
ABM10yrs2hrs                0:48       1.54      
ABM10yrs2hrs                0:51       1.94      
ABM10yrs2hrs                0:54       2.58      
ABM10yrs2hrs                0:57       3.75      
ABM10yrs2hrs                1:00       6.33      
ABM10yrs2hrs                1:03       4.75      
ABM10yrs2hrs                1:06       3.07      
ABM10yrs2hrs                1:09       2.22      
ABM10yrs2hrs                1:12       1.71      
ABM10yrs2hrs                1:15       1.39      
ABM10yrs2hrs                1:18       1.16      
ABM10yrs2hrs                1:21       1.00      
ABM10yrs2hrs                1:24       0.88      
ABM10yrs2hrs                1:27       0.78      
ABM10yrs2hrs                1:30       0.70      
ABM10yrs2hrs                1:33       0.64      
ABM10yrs2hrs                1:36       0.58      
ABM10yrs2hrs                1:39       0.54      
ABM10yrs2hrs                1:42       0.50      
ABM10yrs2hrs                1:45       0.47      
ABM10yrs2hrs                1:48       0.44      
ABM10yrs2hrs                1:51       0.41      
ABM10yrs2hrs                1:54       0.39      
ABM10yrs2hrs                1:57       0.37      
ABM10yrs2hrs                2:00       0.35      

[REPORT]
INPUT      NO
CONTROLS   NO
SUBCATCHMENTS ALL
NODES ALL
LINKS ALL

[TAGS]

[MAP]
DIMENSIONS 0.000 0.000 10000.000 10000.000
Units      None

[COORDINATES]
;;Node           X-Coord            Y-Coord           
;;-------------- ------------------ ------------------
J8               5138.567           3802.918          
3                5955.766           4265.403          
4                5908.373           3491.311          
J12              5312.184           5063.248          

[VERTICES]
;;Link           X-Coord            Y-Coord           
;;-------------- ------------------ ------------------

[Polygons]
;;Subcatchment   X-Coord            Y-Coord           
;;-------------- ------------------ ------------------
E1               4045.528           2844.191          
E1               4199.349           3507.547          
E1               4266.646           3901.714          
E1               4162.095           3904.215          
E1               3499.311           3171.664          
E1               3403.382           2761.784          
1                5039.494           2669.826          
1                5481.833           1753.555          
1                6271.722           3033.175          
1                5560.821           3143.760          
2                7804.107           4660.348          
2                8688.784           4028.436          
2                7614.534           3112.164          
2                7061.611           4375.987          

[SYMBOLS]
;;Gage           X-Coord            Y-Coord           
;;-------------- ------------------ ------------------
Gage1            9936.709           6075.949          
"""

        
inputfile="""
[TITLE]

[OPTIONS]
FLOW_UNITS           LPS
INFILTRATION         CURVE_NUMBER
FLOW_ROUTING         DYNWAVE
START_DATE           10/28/2011
START_TIME           00:00:00
REPORT_START_DATE    10/28/2011
REPORT_START_TIME    00:00:00
END_DATE             10/28/2011
END_TIME             06:00:00
SWEEP_START          01/01
SWEEP_END            12/31
DRY_DAYS             0
REPORT_STEP          00:01:00
WET_STEP             00:01:00
DRY_STEP             00:01:00
ROUTING_STEP         0:00:01 
ALLOW_PONDING        NO
INERTIAL_DAMPING     PARTIAL
VARIABLE_STEP        0.75
LENGTHENING_STEP     0
MIN_SURFAREA         0
NORMAL_FLOW_LIMITED  SLOPE
SKIP_STEADY_STATE    NO
FORCE_MAIN_EQUATION  H-W
LINK_OFFSETS         DEPTH
MIN_SLOPE            0

[EVAPORATION]
;;Type       Parameters
;;---------- ----------
CONSTANT     0.0
DRY_ONLY     NO

[RAINGAGES]
;;               Rain      Time   Snow   Data      
;;Name           Type      Intrvl Catch  Source    
;;-------------- --------- ------ ------ ----------
Gage1            VOLUME    0:03   1.0    TIMESERIES ABM10yrs2hrs    

[SUBCATCHMENTS]
;;                                                 Total    Pcnt.             Pcnt.    Curb     Snow    
;;Name           Raingage         Outlet           Area     Imperv   Width    Slope    Length   Pack    
;;-------------- ---------------- ---------------- -------- -------- -------- -------- -------- --------
E1               Gage1            J8               120      42       16047.2742455 2.16142032087 0                        
1                Gage1            4                120      42       16047.2742455 2.16142032087 0                        
2                Gage1            3                120      42       16047.2742455 2.16142032087 0                        

[SUBAREAS]
;;Subcatchment   N-Imperv   N-Perv     S-Imperv   S-Perv     PctZero    RouteTo    PctRouted 
;;-------------- ---------- ---------- ---------- ---------- ---------- ---------- ----------
E1               0.156646244473 0.203077120449 1.64517849588 3.43542982182 25         OUTLET    
1                0.156646244473 0.203077120449 1.64517849588 3.43542982182 25         OUTLET    
2                0.156646244473 0.203077120449 1.64517849588 3.43542982182 25         OUTLET    

[INFILTRATION]
;;Subcatchment   CurveNum   HydCon     DryTime   
;;-------------- ---------- ---------- ----------
E1               70         0.5        7         
1                70         0.5        7         
2                70         0.5        7         

[JUNCTIONS]
;;               Invert     Max.       Init.      Surcharge  Ponded    
;;Name           Elev.      Depth      Depth      Depth      Area      
;;-------------- ---------- ---------- ---------- ---------- ----------
J8               23.459     3          0          0          0         
3                0          0          0          0          0         
4                0          0          0          0          0         

[OUTFALLS]
;;               Invert     Outfall    Stage/Table      Tide
;;Name           Elev.      Type       Time Series      Gate
;;-------------- ---------- ---------- ---------------- ----
J12              15.649     FREE                        NO

[CONDUITS]
;;               Inlet            Outlet                      Manning    Inlet      Outlet     Init.      Max.      
;;Name           Node             Node             Length     N          Offset     Offset     Flow       Flow      
;;-------------- ---------------- ---------------- ---------- ---------- ---------- ---------- ---------- ----------
T5               J8               J12              235        0.01       0          0          0          0         
1                J8               3                400        0.01       0          0          0          0         
2                J8               4                400        0.01       0          0          0          0         

[XSECTIONS]
;;Link           Shape        Geom1            Geom2      Geom3      Geom4      Barrels   
;;-------------- ------------ ---------------- ---------- ---------- ---------- ----------
T5               RECT_OPEN    .4               3          0          0          1                    
1                CIRCULAR     1                0          0          0          1                    
2                CIRCULAR     1                0          0          0          1                    

[LOSSES]
;;Link           Inlet      Outlet     Average    Flap Gate 
;;-------------- ---------- ---------- ---------- ----------

[TIMESERIES]
;;Name           Date       Time       Value     
;;-------------- ---------- ---------- ----------
;2hr
2hrRainfall                 0:00       0.00      
2hrRainfall                 0:01       0.12      
2hrRainfall                 0:02       0.12      
2hrRainfall                 0:03       0.12      
2hrRainfall                 0:04       0.12      
2hrRainfall                 0:05       0.12      
2hrRainfall                 0:06       0.13      
2hrRainfall                 0:07       0.13      
2hrRainfall                 0:08       0.13      
2hrRainfall                 0:09       0.14      
2hrRainfall                 0:10       0.13      
2hrRainfall                 0:11       0.14      
2hrRainfall                 0:12       0.15      
2hrRainfall                 0:13       0.15      
2hrRainfall                 0:14       0.14      
2hrRainfall                 0:15       0.16      
2hrRainfall                 0:16       0.16      
2hrRainfall                 0:17       0.16      
2hrRainfall                 0:18       0.17      
2hrRainfall                 0:19       0.17      
2hrRainfall                 0:20       0.17      
2hrRainfall                 0:21       0.17      
2hrRainfall                 0:22       0.18      
2hrRainfall                 0:23       0.19      
2hrRainfall                 0:24       0.19      
2hrRainfall                 0:25       0.2       
2hrRainfall                 0:26       0.2       
2hrRainfall                 0:27       0.2       
2hrRainfall                 0:28       0.21      
2hrRainfall                 0:29       0.22      
2hrRainfall                 0:30       0.23      
2hrRainfall                 0:31       0.23      
2hrRainfall                 0:32       0.24      
2hrRainfall                 0:33       0.25      
2hrRainfall                 0:34       0.26      
2hrRainfall                 0:35       0.27      
2hrRainfall                 0:36       0.28      
2hrRainfall                 0:37       0.29      
2hrRainfall                 0:38       0.3       
2hrRainfall                 0:39       0.31      
2hrRainfall                 0:40       0.33      
2hrRainfall                 0:41       0.35      
2hrRainfall                 0:42       0.37      
2hrRainfall                 0:43       0.39      
2hrRainfall                 0:44       0.41      
2hrRainfall                 0:45       0.43      
2hrRainfall                 0:46       0.46      
2hrRainfall                 0:47       0.5       
2hrRainfall                 0:48       0.53      
2hrRainfall                 0:49       0.57      
2hrRainfall                 0:50       0.62      
2hrRainfall                 0:51       0.67      
2hrRainfall                 0:52       0.74      
2hrRainfall                 0:53       0.81      
2hrRainfall                 0:54       0.91      
2hrRainfall                 0:55       1.02      
2hrRainfall                 0:56       1.17      
2hrRainfall                 0:57       1.34      
2hrRainfall                 0:58       1.58      
2hrRainfall                 0:59       1.89      
2hrRainfall                 1:00       2.34      
2hrRainfall                 1:01       2.1       
2hrRainfall                 1:02       1.73      
2hrRainfall                 1:03       1.45      
2hrRainfall                 1:04       1.24      
2hrRainfall                 1:05       1.08      
2hrRainfall                 1:06       0.96      
2hrRainfall                 1:07       0.86      
2hrRainfall                 1:08       0.78      
2hrRainfall                 1:09       0.7       
2hrRainfall                 1:10       0.65      
2hrRainfall                 1:11       0.59      
2hrRainfall                 1:12       0.55      
2hrRainfall                 1:13       0.51      
2hrRainfall                 1:14       0.48      
2hrRainfall                 1:15       0.45      
2hrRainfall                 1:16       0.43      
2hrRainfall                 1:17       0.39      
2hrRainfall                 1:18       0.38      
2hrRainfall                 1:19       0.36      
2hrRainfall                 1:20       0.34      
2hrRainfall                 1:21       0.33      
2hrRainfall                 1:22       0.32      
2hrRainfall                 1:23       0.3       
2hrRainfall                 1:24       0.29      
2hrRainfall                 1:25       0.27      
2hrRainfall                 1:26       0.26      
2hrRainfall                 1:27       0.26      
2hrRainfall                 1:28       0.24      
2hrRainfall                 1:29       0.24      
2hrRainfall                 1:30       0.23      
2hrRainfall                 1:31       0.22      
2hrRainfall                 1:32       0.22      
2hrRainfall                 1:33       0.21      
2hrRainfall                 1:34       0.2       
2hrRainfall                 1:35       0.2       
2hrRainfall                 1:36       0.19      
2hrRainfall                 1:37       0.18      
2hrRainfall                 1:38       0.18      
2hrRainfall                 1:39       0.18      
2hrRainfall                 1:40       0.17      
2hrRainfall                 1:41       0.17      
2hrRainfall                 1:42       0.16      
2hrRainfall                 1:43       0.16      
2hrRainfall                 1:44       0.15      
2hrRainfall                 1:45       0.15      
2hrRainfall                 1:46       0.15      
2hrRainfall                 1:47       0.15      
2hrRainfall                 1:48       0.14      
2hrRainfall                 1:49       0.14      
2hrRainfall                 1:50       0.14      
2hrRainfall                 1:51       0.14      
2hrRainfall                 1:52       0.13      
2hrRainfall                 1:53       0.13      
2hrRainfall                 1:54       0.13      
2hrRainfall                 1:55       0.13      
2hrRainfall                 1:56       0.13      
2hrRainfall                 1:57       0.12      
2hrRainfall                 1:58       0.12      
2hrRainfall                 1:59       0.12      
2hrRainfall                 2:00       0.11      

;Rainfall Data
ABM10yrs2hrs                0:00       0         
ABM10yrs2hrs                0:03       0.36      
ABM10yrs2hrs                0:06       0.38      
ABM10yrs2hrs                0:09       0.40      
ABM10yrs2hrs                0:12       0.42      
ABM10yrs2hrs                0:15       0.45      
ABM10yrs2hrs                0:18       0.48      
ABM10yrs2hrs                0:21       0.52      
ABM10yrs2hrs                0:24       0.56      
ABM10yrs2hrs                0:27       0.61      
ABM10yrs2hrs                0:30       0.67      
ABM10yrs2hrs                0:33       0.74      
ABM10yrs2hrs                0:36       0.82      
ABM10yrs2hrs                0:39       0.93      
ABM10yrs2hrs                0:42       1.08      
ABM10yrs2hrs                0:45       1.27      
ABM10yrs2hrs                0:48       1.54      
ABM10yrs2hrs                0:51       1.94      
ABM10yrs2hrs                0:54       2.58      
ABM10yrs2hrs                0:57       3.75      
ABM10yrs2hrs                1:00       6.33      
ABM10yrs2hrs                1:03       4.75      
ABM10yrs2hrs                1:06       3.07      
ABM10yrs2hrs                1:09       2.22      
ABM10yrs2hrs                1:12       1.71      
ABM10yrs2hrs                1:15       1.39      
ABM10yrs2hrs                1:18       1.16      
ABM10yrs2hrs                1:21       1.00      
ABM10yrs2hrs                1:24       0.88      
ABM10yrs2hrs                1:27       0.78      
ABM10yrs2hrs                1:30       0.70      
ABM10yrs2hrs                1:33       0.64      
ABM10yrs2hrs                1:36       0.58      
ABM10yrs2hrs                1:39       0.54      
ABM10yrs2hrs                1:42       0.50      
ABM10yrs2hrs                1:45       0.47      
ABM10yrs2hrs                1:48       0.44      
ABM10yrs2hrs                1:51       0.41      
ABM10yrs2hrs                1:54       0.39      
ABM10yrs2hrs                1:57       0.37      
ABM10yrs2hrs                2:00       0.35      

[REPORT]
INPUT      NO
CONTROLS   NO
SUBCATCHMENTS ALL
NODES ALL
LINKS ALL

[TAGS]

[MAP]
DIMENSIONS 0.000 0.000 10000.000 10000.000
Units      None

[COORDINATES]
;;Node           X-Coord            Y-Coord           
;;-------------- ------------------ ------------------
J8               5138.567           3802.918          
3                5955.766           4265.403          
4                5908.373           3491.311          
J12              5312.184           5063.248          

[VERTICES]
;;Link           X-Coord            Y-Coord           
;;-------------- ------------------ ------------------

[Polygons]
;;Subcatchment   X-Coord            Y-Coord           
;;-------------- ------------------ ------------------
E1               4045.528           2844.191          
E1               4199.349           3507.547          
E1               4266.646           3901.714          
E1               4162.095           3904.215          
E1               3499.311           3171.664          
E1               3403.382           2761.784          
1                5039.494           2669.826          
1                5481.833           1753.555          
1                6271.722           3033.175          
1                5560.821           3143.760          
2                7804.107           4660.348          
2                8688.784           4028.436          
2                7614.534           3112.164          
2                7061.611           4375.987          

[SYMBOLS]
;;Gage           X-Coord            Y-Coord           
;;-------------- ------------------ ------------------
Gage1            9936.709           6075.949          
"""




if __name__=="__main__":
    main_function()
        
