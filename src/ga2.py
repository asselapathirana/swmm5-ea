from random import Random
from time import time, sleep
import inspyred
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

import array

bestlist=[[],[],[]]
def observer_function(population, num_generations, num_evaluations, args):
    if num_generations % 10 != 0 : 
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
    #plt.yscale('log')

    plt.draw()




def main(prng=None, display=False):    
    if prng is None:
        prng = Random()
        prng.seed(time()) 
        
    problem = inspyred.benchmarks.Rosenbrock(2)
    ea = inspyred.ec.ES(prng)
    ea.observer=[observer_function,inspyred.ec.observers.file_observer]
    ea.terminator = [inspyred.ec.terminators.evaluation_termination, 
                     inspyred.ec.terminators.diversity_termination]
    
    staf=open(u"stats.csv","w")
    indf=open(u"indis.csv","w")
    #.
    final_pop = ea.evolve(generator=problem.generator, 
                          evaluator=problem.evaluator, 
                          pop_size=5, 
                          bounder=problem.bounder,
                          maximize=problem.maximize,
                          max_evaluations=80, 
                          mutation_rate=.25,
                          individuals_file=indf,
                          statistics_file=staf
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