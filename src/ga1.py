from random import Random
from time import time, sleep
import inspyred
import math
import matplotlib.pyplot as plt



def generator_function(random, args):
    size = args.get('num_inputs', 10)
    return [random.uniform(-5.12, 5.12) for i in range(size)]

def observer_function(population, num_generations, num_evaluations, args):
    if num_generations % 10 != 0 : 
        return 
    plt.ion()
    soln=max(population)
    plt.plot(num_generations,soln.fitness,'ro')
    plt.plot(num_generations,min(population).fitness,'bo')
    plt.ylabel('some numbers')
    plt.draw()
    #sleep(0.01)
    
def evaluator_function(candidates, args):
    fitness = []
    for cs in candidates:
        fit =  10 * len(cs) + sum([((x - 1)**2 - 10 * math.cos(2 * math.pi * (x - 1))) for x in cs])
        fitness.append(fit)
    return fitness

def main(prng=None, display=False): 
    if prng is None:
        prng = Random()
        prng.seed(time()) 

    ea = inspyred.ec.ES(prng)
    #ea.terminator = inspyred.ec.terminators.generation_termination
    ea.terminator = inspyred.ec.terminators.evaluation_termination
    #ea.terminator  = inspyred.ec.terminators.diversity_termination    
    ea.observer=observer_function
   # ea.selector=inspyred.ec.selectors.tournament_selection
    #ea.variator = inspyred.ec.variators.uniform_crossover
    final_pop = ea.evolve(generator=generator_function,
                          evaluator=evaluator_function,
                          pop_size=100,
                          maximize=False,
                          bounder=inspyred.ec.Bounder(-5.12,5.12),
                          max_evaluations=50000,
                          mutation_rate=.025,
                          num_inputs=3,
                          #max_generations=1000
                          )
                          
    if display:
        best = max(final_pop)
        print('Best Solution: \n{0}'.format(str(best)))
    return ea
            
if __name__ == '__main__':
    main(display=True)
    plt.show(block=True)
    