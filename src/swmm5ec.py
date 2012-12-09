## How to freeze into a windows exe
## Open cmd prompt. 
## run setup.py as follows
## python E:\Urban_drainageI_II\2012\GA\inspyred\src\setup.py py2exe
## in ./src directory
## Copy the entire dist directory to the target computer. 
from random import Random
import numpy
from time import time, sleep
import os, errno
import inspyred
#import matplotlib
#matplotlib.use('GTKAgg')
#import matplotlib.pyplot as plt
#from subprocess import Popen,PIPE  
import math
import sys
import traceback
from PyQt4 import QtCore, QtGui

import swmm5 as sw


class dumb(object):
    def __init__(self):
        pass  


def evaluatorf(candidates, args):
    fitness = []
    # linestring=args.get('linestring','foo')
    parameters=args.get('parameters',None)
    linestring=parameters.linestring
    #print "thread: ", QtCore.QThread.currentThreadId()
    for cs in candidates:
        sys.stdout.write("|")
        tf=cs[0:parameters.num_inputs] # this is important when evolution strategy is implemented. 
        # above subsetting of the array [0:len(parameters.power_for_inputs)] is important when evolution strategy is used.     
        fitness.append(getFitness(tf,linestring,parameters))
        sys.stdout.write("-")
    return fitness

def getFitness(fillers, linestring,parameters):

    fitness=0.0
    try:
        scaled=scale(fillers,parameters)
        import  os
        from multiprocessing import current_process
        filename = parameters.projectdirectory+os.sep+"tmp"+os.sep+("%07d" % (current_process().pid))+".inp"
	make_sure_path_exists(os.path.dirname(filename))                
        dir = os.path.dirname(filename)
        try:
            os.stat(dir)
        except:
            os.mkdir(dir)    

        flood = swmmFlood(scaled, linestring, filename,parameters)
        #print "\tFlood : ", flood, sum(map(lambda fil: fil,scaled))

        import pyratemp
        costf=pyratemp.Template("@!"+parameters.cost_function+"!@")
        pp=parse_parameters(scale(fillers,parameters))
        cost1=float(costf(**(pp)))
        costf=pyratemp.Template("@!"+parameters.swmmout_cost_function+"!@")
        pp={"f": flood}
        cost2=float(costf(**(pp)))
        fitness=cost1+cost2
        
    except:
        
        print "\nError here: !!!!\n\n"
        try:
            tb = traceback.format_exc()  
            print tb
        except:
            print "\grave error!!!\n\n"
        fitness=None
    finally: 
        return fitness



def scale(fillers,parameters):
    #print fillers
    f=numpy.array(fillers)
    p=numpy.array(parameters.valuerange).T
    try:
        s=p[0]+(p[1]-p[0])*(f+1)
        #print p[0], p[1], f
    except:
        print "\nProblem scaling with valuerange array. Check it !"

        import sys, traceback
        traceback.print_exc(file=sys.stderr)
        traceback.print_stack(file=sys.stderr)
        sys.exit()
    return s

def swmmFlood(fillers, linestring, outfile,parameters):
    swmmWrite(fillers, linestring, outfile)
    binfile=outfile[:-3]+"bin"
    rptfile=outfile[:-3]+"rpt"
    cost=swmmRun(outfile,rptfile,binfile,parameters)
    deleteSWMMfiles(outfile, rptfile, binfile)
    return cost

def swmmRun(swmminputfile, rptfile, binfile,parameters):
    ret=sw.RunSwmmDll(swmminputfile,rptfile,binfile)
    err(ret)
    err(sw.OpenSwmmOutFile(binfile))
    results=[]
    t=0.0
    flood=0.0
    for i in range(sw.cvar.SWMM_Nperiods):
        ret,z=sw.GetSwmmResult(parameters.swmmResultCodes[0], parameters.swmmResultCodes[1],parameters.swmmResultCodes[2], i)
        t+=sw.cvar.SWMM_ReportStep
        flood+=z*sw.cvar.SWMM_ReportStep
    sw.CloseSwmmOutFile()
    return flood

def deleteSWMMfiles(swmminputfile, rptfile, binfile):
    import os
    os.unlink(swmminputfile)
    os.unlink(rptfile)
    os.unlink(binfile)

def swmmWrite(fillers, linestring, outfile):

    params = parse_parameters(fillers)
    import pyratemp
    pt=pyratemp.Template(linestring)
    linestring=pt(**params)
    make_sure_path_exists(os.path.dirname(outfile))
    f=open(outfile,'w')
    f.write(linestring)
    f.close()


    
def make_sure_path_exists(path):
    try:
	os.makedirs(path)
    except OSError as exception:
	if exception.errno != errno.EEXIST:
	    raise

def parse_parameters(fillers):
    ct=0
    params={}
    for filler in fillers:
        ct=ct+1
        word="v%(f)i"%{"f" : ct}
        params[word]=filler
    return params

def SwmmTemplate(templatefile):
    f=open(templatefile, 'r')
    linestring = f.read()
    f.close()
    return linestring

def err(e):
    if(e>0):
        print e, "Error!" #sw.ENgeterror(e,25)

class SwmmEA(QtCore.QThread):

    def __init__(self):
        QtCore.QThread.__init__(self) 
	#self.lock               = lock
	self.stopped            = False
	self.mutex              = QtCore.QMutex()
	self.completed          = False
	self.paused             = False       
    def log(self,logfile):
	import logging
	logger = logging.getLogger('inspyred.ec')
	logger.setLevel(logging.DEBUG)
	file_handler = logging.FileHandler(logfile, mode='w')
	file_handler.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)     

    def message(self,msg):
	self.emit( QtCore.SIGNAL('message(QString)'), msg )
	
    def stopterminator(self,population, num_generations, num_evaluations, args):
	if self.stopped: 
	    self.message( "... and stopped.")	    
	    return True
	else:
	    return False
    
    def swmm_best_observer(self,population, num_generations, num_evaluations, args):
        import os
        linestring=args.get('parameters','foo').linestring
        best=max(population)
        worst=min(population)
        parameters=args["parameters"]
        swmmfile=(parameters.projectdirectory+os.sep+parameters.resultsdirectory+os.sep+"Best_of_gen_%(#)03i" % {"#":num_generations})+".inp"
        binfile =(parameters.projectdirectory+os.sep+parameters.resultsdirectory+os.sep+"Best_of_gen_%(#)03i" % {"#":num_generations})+".bin"
        rptfile =(parameters.projectdirectory+os.sep+parameters.resultsdirectory+os.sep+"Best_of_gen_%(#)03i" % {"#":num_generations})+".rpt"
        p=best.candidate[0:parameters.num_inputs] # this is essential when handling evolution strategy in inspyred (due to double internal length of the array)
        swmmWrite(scale(p,parameters),linestring,swmmfile)
        #flood=swmmRun(swmmfile,rptfile,binfile)
        strb=map(lambda s: "{0:.3e}".format(s),scale(p,parameters))
        print '\nBest fitness %(fit).3e for values %(ind)s ' % {"fit": best.fitness,"ind": strb}
	while(self.paused):
	    QtCore.QThread.msleep(1000)
	    if not  self.paused_finally:
		self.paused_finally=True
		self.message("..and paused.")

    def observer_function(self,population, num_generations, num_evaluations, args):
        import time
        if num_generations % 1 != 0 : 
            return 
        parameters=args["parameters"]
        popn=sorted(population)
        #parameters.bestlist[0].append(num_generations)
        result=[num_generations,[]]
        for i in reversed(popn):
            result[1].append(i.fitness)
        self.emit( QtCore.SIGNAL('nextGeneration(PyQt_PyObject)'), result )
        if not parameters.multiprocessor:
            # otherwise this thread will starve the gui thread. However, when multiprocessing, python multiprocessing module will take care of this?
            self.msleep(500)
        
        """       
       
        #parameters.bestlist[1].append(popn[-1].fitness)
        #parameters.bestlist[2].append(popn[-2].fitness)
        #parameters.bestlist[3].append(popn[-3].fitness)
        #parameters.bestlist[4].append(popn[0].fitness)
        #plt.ion()

        #plt.plot(num_generations,soln.fitness,'ro')
        #plt.plot(num_generations,psln.fitness,'bo')
        l=int(len(parameters.bestlist[0])/2)
        lim=[ min(parameters.bestlist[0][l:])-1,
              max(parameters.bestlist[0][l:])+1,
              min(parameters.bestlist[1][l:])*.5,
              max(parameters.bestlist[3][l:])*1.5
              ]    
        ##plt.axis(lim)
        #gps=parameters.projectdirectory+os.sep+parameters.resultsdirectory+os.sep+parameters.gnuplotscript
        #gf=open(gps,"w")
        #gpd=parameters.projectdirectory+os.sep+parameters.resultsdirectory+os.sep+parameters.gnuplotdata
        #gd=open(gpd,"w")

        ##gf.write(b"# set terminal pngcairo  transparent enhanced font \"arial,10\" fontscale 1.0 size 660, 320 ")
        ##gf.write(b"# set output 'finance.1.png'")
        #gf.write(b"set key top left\n")
        #gf.write(b"set key box\n")

        #gf.write(b"set terminal windows\n")
        #gf.write(b"set ytics  norangelimit\n")
        #gf.write(b"#set ytics   (80.0000, 85.0000, 90.0000, 95.0000, 100.000, 105.000)")
        #gf.write(b"set title \"Demo of plotting financial data\n")
        #gf.write(b"set xrange [ %(x1)d : %(x2)d ] noreverse nowriteback\n\
                 #set yrange [ %(y1)d : %(y2)d ] noreverse nowriteback\n"
                 #% { "x1": lim[0], "x2" : lim[1], "y1" : lim[2], "y2" : lim[3] })
        #gf.write(b"set lmargin  9\n")
        #gf.write(b"set rmargin  2\n")
        #gf.write(b"set style line 1 lt 1 lw 2 pt 1 linecolor rgb \"red\"\n")
        #gf.write(b"set style line 2 lt 1 lw 1 pt 2 linecolor rgb \"blue\"\n")
        #gf.write(b"set style line 3 lt 1 lw 1 pt 3 linecolor rgb \"green\"\n")
        #gf.write(b"set style line 4 lt 1 lw 2 pt 4 linecolor rgb \"black\"\n")
        #gf.write(b"set style line 5 lt .5 lw .5 pt 5 linecolor rgb \"gray\"\n")
        #gf.write(b"plot ")
        #for i in range(5,parameters.pop_size):
            #gf.write(b" '%(dat)s' using  1:%(col)i title \"\" with points ls 5," %{ "dat": gpd, "col": i })
        #gf.write(b" '%(dat)s' using  1:2 title \"Best\" with linespoints ls 1," %{ "dat": gpd })
        #gf.write(b" '%(dat)s' using  1:3 title \"2nd Best\" with linespoints ls 2," %{ "dat": gpd })
        #gf.write(b" '%(dat)s' using  1:4 title \"3rd Best\" with linespoints ls 3," %{ "dat": gpd })    
        #gf.write(b" '%(dat)s' using  1:5 title \"Worst\" with linespoints ls 4" %{ "dat": gpd })
        #gf.write(b"\n")  


        for i in range(len(parameters.bestlist[0])):
            gd.write(str(parameters.bestlist[0][i])+"\t" +
                     str(parameters.bestlist[1][i])+"\t" +
                     str(parameters.bestlist[2][i])+"\t" +
                     str(parameters.bestlist[3][i])+"\t" +
                     str(parameters.bestlist[-1][i])+"\t"
                     )
            for j in range(5,parameters.pop_size+1):
                gd.write(str(parameters.bestlist[j][i])+"\t")
            gd.write("\n");

        #gf.close()
        #gd.close()    

        #self.plot.stdin.write(b"load \'%(gnu)s\'\n" % {"gnu" : gps})
        #self.plot.stdin.flush()
        #
        """
    def stop(self):
	with QtCore.QMutexLocker(self.mutex):
	    self.stopped    = True
	    sys.stdout.write( " Signelled to stop. Waiting this cycle to finish....")
	    
    

    def pause(self, theBool=True):
	self.paused_finally=False
	if(theBool):
	    sys.stdout.write( " Signelled to pause. Waiting this cycle to finish....")
	    self.paused=True
	    self.paused_finally=False
	else:
	    self.paused=False
	    self.paused_finally=True

	#if theBool == True:  # pause task
		#try:
			#self.mutex.lock()
			#self.paused     = True
		#finally:
			#self.mutex.unlock()

	#else: # resume processing
		#try:
			#self.mutex.lock()
			#self.paused     = False
			
		#finally:
			#self.mutex.unlock()
				
    def setParams(self,parameters=None,display=None, prng=None):
        self.parameters=parameters
        self.display=display
        self.prng=prng

    def run(self):
        #self.plot=Popen([self.parameters.gnuplot,'-persist'],stdin=PIPE,stdout=PIPE,stderr=PIPE, shell=False)          
        self.runOptimization()

    def runOptimization(self):
        parameters=self.parameters
        prng=self.prng
        display=self.display
        if parameters is None: 
            print "problem jim!"
            return None
        import pyratemp, os
        parameters.linestring=SwmmTemplate(parameters.projectdirectory+os.sep+parameters.datadirectory+os.sep+parameters.templatefile)

        if prng is None:
            prng = Random()
            prng.seed(time()) 

	

        @inspyred.ec.generators.strategize    
        def generatorf(random, args):
            bounds=args.get('bounds',[-1,1])
            size = args.get('num_inputs', 10)
            return [random.uniform(bounds[0],bounds[1]) for i in range(size)] 

        self.log(parameters.projectdirectory+os.sep+'swmm_ea.log')
        my_ec = inspyred.ec.EvolutionaryComputation(prng)
        my_ec.generator=generatorf
        my_ec.selector = inspyred.ec.selectors.tournament_selection
        #my_ec.selector=inspyred.ec.selectors.rank_selection
        my_ec.variator = [inspyred.ec.variators.arithmetic_crossover, inspyred.ec.variators.gaussian_mutation]
        my_ec.replacer = inspyred.ec.replacers.generational_replacement
        my_ec.observer = [self.observer_function,inspyred.ec.observers.file_observer, self.swmm_best_observer]
        my_ec.terminator = [inspyred.ec.terminators.evaluation_termination, 
                            inspyred.ec.terminators.diversity_termination,
	                    self.stopterminator]

        staf=open(parameters.projectdirectory+os.sep+u"stats.csv","w")
        indf=open(parameters.projectdirectory+os.sep+u"indis.csv","w")
        # parallel processing would not work if you pass these to the evolve method (see the log file, serializing these fail!)

        #linestring = SwmmTemplate()



        mp=False
	if parameters.num_cpus > 1: 
	    print "Setting parallel processing because num_cpus =", parameters.num_cpus
	    mp=True
        final_pop = my_ec.evolve(generator=generatorf, 
                                 parameters=parameters,
                                 evaluator=mp 
                                 and inspyred.ec.evaluators.parallel_evaluation_mp
                                 or evaluatorf,
                                 mp_evaluator=evaluatorf, 
                                 mp_nprocs=parameters.num_cpus, # inspyred doc is wrong. 
                                 pop_size=parameters.pop_size, 
                                 statistics_file=staf,
                                 individuals_file=indf,

                                 bounder=inspyred.ec.Bounder(-1,1),
                                 bounds=[-1,1],
                                 maximize=parameters.maximize,
                                 max_evaluations=parameters.max_evaluations, 
                                 crossover_rate=parameters.crossover_rate,
                                 num_crossover_points=parameters.num_crossover_points,
                                 mutation_rate=parameters.mutation_rate,
                                 #individuals_file=indf,
                                 #statistics_file=staf,
                                 num_inputs=parameters.num_inputs,
                                 num_selected=parameters.num_selected,
                                 num_elites =parameters.num_elites
                                 )


        if display:
            #   plt.figure()
            #   best = max(final_pop)
            #   
            #   
            #   inspyred.ec.analysis.allele_plot(u"indis.csv")
            #   
            #   plt.show()
            #   
            #   plt.figure()
            #   plt.yscale("log")
            #   inspyred.ec.analysis.generation_plot(u"stats.csv");          
            #  #plt.xlim(xmin=)
            #   plt.ioff()
            #   plt.show()        
            #   #plt.savefig(u"generations.png")
            #   #sleep(10)
            pass
        return my_ec


  

def ReadParameters():
    import os
    parameters=dumb()
    startfile=os.getcwd()+os.sep+'start.yaml'
    try:
        import yaml
        f = open(startfile)
        dataMap = yaml.load(f)
        f.close()

        for key in dataMap :
            setattr(parameters, key, dataMap[key])
    except: 
        print "Problem reading file '%s' " % startfile,sys.exc_info()[0]
        sys.exit()        

    parameterfile=os.getcwd()+os.sep+parameters.projectdirectory+os.sep+"param.yaml"    
    print "Using parameter file :" , parameterfile

    try:
        import yaml
        f = open(parameterfile)
        dataMap = yaml.load(f)
        f.close()

        for key in dataMap :
            setattr(parameters, key, dataMap[key])
    except: 
        print "Problem reading file '%s' " % parameterfile ,sys.exc_info()[0]
        sys.exit()
    #global plot
    #plot=Popen([parameters.gnuplot,'-persist'],stdin=PIPE,stdout=PIPE,stderr=PIPE, shell=False)     

    parameters.bestlist=[]
    for i in range(parameters.pop_size+1):
        parameters.bestlist.append([])     
    return parameters


def main_function():
    import sys, os
    import multiprocessing
    multiprocessing.freeze_support()
    #if ( len(sys.argv) > 1):
    #    t=sys.argv[1]
    #else:
    print "Working directory : %(n)s" % {"n": os.getcwd()}
        #t=raw_input("Enter the name of parameter  file (*.yaml) : ")
        #t=None

    parameters=ReadParameters()
    
    if not os.path.exists(parameters.projectdirectory):
        print "There is no directory named: "+parameters.projectdirectory+" under "+ prjroot+os.sep + " directory.\n"
        print "Please create one using the template (myproject) provided.\n"
        sys.exit() 
    if not os.path.exists(parameters.projectdirectory+os.sep+parameters.resultsdirectory):
        os.makedirs(parameters.projectdirectory+os.sep+parameters.resultsdirectory)    
    if not os.path.exists(parameters.projectdirectory+os.sep+parameters.datadirectory):
        print "Hell! there's no directory named : " +  parameters.projectdirectory+os.sep+parameters.datadirectory +"\n"
        print "I quit. Check param.yaml file and try again"
        sys.exit()
    import cProfile, pstats


    app = QtGui.QApplication(sys.argv)    
    swmmea=SwmmEA()
    swmmea.setParams(parameters=parameters, display=True)
    swmmea.start()
    app.exec_()

if __name__ == '__main__':
    main_function()


