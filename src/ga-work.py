from random import Random
from time import time, sleep
import inspyred
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import math

import array
import os
os.environ['PYTHONPATH'] = os.getcwd() + ';' + os.environ['PYTHONPATH'] 
import swmm5 as sw

bestlist=[[],[],[]]
def observer_function(population, num_generations, num_evaluations, args):
    if num_generations % 1 != 0 : 
        return 
    soln=max(population)    
    psln=min(population)
    bestlist[0].append(num_generations)
    bestlist[1].append(soln.fitness)
    bestlist[2].append(psln.fitness)
    plt.ion()
    
    #plt.plot(num_generations,soln.fitness,'ro')
    #plt.plot(num_generations,psln.fitness,'bo')
    try:
        p1,=plt.plot([bestlist[0][-1],bestlist[0][-2]],
             [bestlist[1][-1],bestlist[1][-2]],
             'r-o'
             )
        p2,=plt.plot([bestlist[0][-1],bestlist[0][-2]],
             [bestlist[2][-1],bestlist[2][-2]],
             'b-o'
             )    
        plt.legend([p2, p1], ["Worst", "Best"])
        l=int(len(bestlist[0])/2)

        lim=[ min(bestlist[0][l:])-1,
              max(bestlist[0][l:])+1,
              min(bestlist[1][l:])*.1,
              max(bestlist[2][l:])*1.5
            ]    
        plt.axis(lim)  

    except:
        None
    
    plt.ylabel('Fitness')
    plt.xlabel('Generation')
    print bestlist[0][-1], bestlist[1][-1], bestlist[2][-1]
    #plt.yscale('log')

    plt.draw()

def generatorf(random, args):
    bounds=args.get('bounds',[0,10])
    size = args.get('num_inputs', 10)
    return [random.uniform(bounds[0],bounds[1]) for i in range(size)]    

def evaluatorf(candidates, args):
    fitness = []
    for cs in candidates:
        fitness.append(swmmrun(cs))
    return fitness

def swmmrun(fillers):
    outfile="ex1.inp"
    linestring = SwmmTemplate()
    flood = swmmFlood(fillers, linestring, outfile)
    return sum(map(lambda fil: fil**2,fillers)) +flood*100

def swmmFlood(fillers, linestring, outfile):
    swmmWrite(fillers, linestring, outfile)
    binfile=outfile[:-3]+"bin"
    rptfile=outfile[:-3]+"rpt"
    return swmmRun(outfile,rptfile,binfile)

def swmmRun(swmminputfile, rptfile, binfile):
    ret=sw.RunSwmmDll(swmminputfile,rptfile,binfile)
    err(ret)
    err(sw.OpenSwmmOutFile(binfile))
    results=[]
    t=0.0
    flood=0.0
    for i in range(sw.cvar.SWMM_Nperiods):
        ret,z=sw.GetSwmmResult(3,0,10,i)
        t+=sw.cvar.SWMM_ReportStep
        flood+=z*sw.cvar.SWMM_ReportStep
    sw.CloseSwmmOutFile()
    return flood

def swmmWrite(fillers, linestring, outfile):
    ct=0
    for filler in fillers:
        ct=ct+1
        word="#INP"+str(ct)+"#"
        #print word
        linestring=linestring.replace(word,str(filler))
    f=open(outfile,'w')
    f.write(linestring)
    f.close()

def SwmmTemplate():
    f=open('ex.inp', 'r')
    linestring = f.read()
    f.close()
    return linestring
        
def err(e):
    if(e>0):
        print e, "Error!" #sw.ENgeterror(e,25)
    
def swmm_best_observer(population, num_generations, num_evaluations, args):
    best=max(population)
    worst=min(population)
    temp=SwmmTemplate()
    swmmfile=("Best_of_gen_%(#)03i" % {"#":num_generations})+".inp"
    binfile =("Best_of_gen_%(#)03i" % {"#":num_generations})+".bin"
    rptfile =("Best_of_gen_%(#)03i" % {"#":num_generations})+".rpt"
    swmmWrite(best.candidate,temp,swmmfile)
    flood=swmmRun(swmmfile,rptfile,binfile)
    print best.candidate
    

def main(prng=None, display=False):    
    
    import os

    if prng is None:
        prng = Random()
        prng.seed(time()) 
        
    
    my_ec = inspyred.ec.EvolutionaryComputation(prng)
    my_ec.selector = inspyred.ec.selectors.tournament_selection
    my_ec.variator = [inspyred.ec.variators.uniform_crossover, inspyred.ec.variators.gaussian_mutation]
    my_ec.replacer = inspyred.ec.replacers.generational_replacement
    my_ec.observer = [observer_function,inspyred.ec.observers.file_observer, swmm_best_observer]
    my_ec.terminator = [inspyred.ec.terminators.evaluation_termination, 
                     inspyred.ec.terminators.diversity_termination]
    
    staf=open(u"stats.csv","w")
    indf=open(u"indis.csv","w")
    #.
    final_pop = my_ec.evolve(generator=generatorf, 
                          evaluator=evaluatorf, 
                          pop_size=50, 
                          bounder=inspyred.ec.Bounder(0.01,10),
                          maximize=False,
                          max_evaluations=1000, 
                          crossover_rate=.5,
                          num_crossover_points=2,
                          mutation_rate=.025,
                          individuals_file=indf,
                          statistics_file=staf,
                          num_inputs=5,
                          num_elites =5, 
                          num_selected=25
                          )

    
    if display:
        plt.figure()
        best = max(final_pop)
        
        print('Best Solution: \n{0}'.format(str(best)))
        inspyred.ec.analysis.allele_plot(u"indis.csv")
        #plt.savefig(u"allele.png")
        plt.show()
        
        plt.figure()
        plt.yscale("log")
        plt.axis('image')  
        plt.show()
        inspyred.ec.analysis.generation_plot(u"stats.csv");          
        #plt.xlim(xmin=)
        plt.ioff()
        plt.show()        
        #plt.savefig(u"generations.png")
        #sleep(10)
    return ea
            
if __name__ == '__main__':
    main(display=True)
    
    
