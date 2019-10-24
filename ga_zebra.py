#-------------------------------IMPORTS------------------------------------#
import random
import math
import time
import curses
import os
#--------------------------------------------------------------------------#

#--------------------------GENERATE INITIAL POP----------------------------#
def gen_initial(pop_size):
    pop = []
    for i in range(pop_size):
        pop.append(generate_genome())
    return pop
#--------------------------------------------------------------------------#

#--------------------------GENERATE MATING POOL----------------------------#
def selection(population,target):
    mating_pool = []
    max_fitness = 0
    for i,indv in enumerate(population):
        fitness = calcFitness(indv, target)
        if fitness > max_fitness:
            max_fitness = fitness
    min_fitness = max_fitness / 2
    
    for i,indv in enumerate(population):
        fitness = calcFitness(indv, target)/max_fitness
        n = math.floor(math.pow(fitness * 10, 2))
        for j in range(n):
            mating_pool.append(indv)
    return mating_pool
#--------------------------------------------------------------------------#
    
#-------------------------GENERATE NEW POPULATION--------------------------#
def generate(population,mating_pool, mutation_rate):
    for i in range(0,len(population),2):
        parent1 = random.choice(mating_pool)
        parent2 = random.choice(mating_pool)
        parent3 = random.choice(mating_pool)

        [child1,child2] = crossover(parent1, parent2, parent3)
        
        population[i] = mutate(child1, mutation_rate)
        population[i+1] = mutate(child2, mutation_rate)
    return population
    
#--------------------------------------------------------------------------#
      
#-------------------------------EVALUATE-----------------------------------#
def evaluate(population,target):
    best_score, total_score, total_pop = 0,0,0
    best = []
    for i,indv in enumerate(population):
        fitness = calcFitness(indv,target)
        total_score += fitness
        total_pop += 1
        if fitness > best_score:
            best = indv
            best_score = fitness
            
    return (best, best_score, total_score/total_pop)
#--------------------------------------------------------------------------#

#--------------------------------GENOME------------------------------------#
def generate_genome():
    cars            = ['Toyota Camry',  'Hyundai Accent',   'Holden Barina',    'Nissan X-Trail', 'Honda Civic']
    colors          = ['black',         'blue',             'green',            'red',            'white']
    people          = ['British',       'French',           'Chinese',          'Indian',         'Canadian']
    destinations    = ['Gold Coast',    'Sydney',           'Newcastle',        'Tamworth',       'Port Macquarie']
    times           = ['6am',           '9am',              '5am',              '7am',            '8am']
    order           = ['1st',           '2nd',              '3rd',              '4th',            '5th']


    random.shuffle(cars)
    random.shuffle(colors)
    random.shuffle(people)
    random.shuffle(destinations)
    random.shuffle(times)
    #random.shuffle(order)

    attributes = [colors, cars, people, destinations, times, order]

    dna = []
    for i in range(5):
        gene = []
        for j in range(len(attributes)):
            gene.append(attributes[j][i])
        dna.append(gene)
    return dna
#--------------------------------------------------------------------------#

#---------------------------------CLUES------------------------------------#
def questions(dna):
    color,car,people,dest,time = tuple(range(5))
    score = 0
    for index, attr in enumerate(dna):
        score += sum([
        attr[people] == 'British' and attr[time] == '6am', 
        attr[people] == 'British' and attr[car] == 'Toyota Camry',
        attr[car] == 'Toyota Camry' and attr[time] == '6am',
        
        index == 2 and attr[color] == 'black',
        
        attr[car] == 'Hyundai Accent' and attr[time] == '9am',
        
        attr[car] == 'Holden Barina' and attr[color] == 'blue',
        index < 4 and attr[color] == 'blue' and dna[index + 1][people] == 'British',
        index < 4 and attr[car] == 'Holden Barina' and dna[index + 1][people] == 'British',

        index > 0 and attr[dest] == 'Gold Coast' and dna[index - 1][people] == 'French',
        
        attr[car] == 'Nissan X-Trail' and attr[dest] == 'Sydney',
        
        index > 0 and attr[color] == 'green' and dna[index - 1][people] == 'Chinese',
        
        attr[dest] == 'Newcastle' and attr[time] == '5am',
        
        index > 0 and attr[car] == 'Honda Civic' and dna[index - 1][dest] == 'Gold Coast',
        index > 0 and attr[time] == '7am' and dna[index - 1][dest] == 'Gold Coast',
        attr[car] == 'Honda Civic' and dna[index - 1][dest] == 'Gold Coast',
        
        attr[color] == 'red' and attr[dest] == 'Tamworth',
        
        index < 4 and attr[color] == 'white' and dna[index + 1][time] == '7am',
        
        index == 4 and attr[people] == 'Indian',
        
        attr[color] == 'black' and attr[time] == '8am',
        
        index > 0 and attr[people] == 'Indian' and dna[index - 1][people] == 'Chinese',
        
        attr[dest] == 'Tamworth' and attr[time] == '6am',
        ])
    return score
#--------------------------------------------------------------------------#

#--------------------------------FITNESS-----------------------------------#
def calcFitness(dna, target):
    return questions(dna) / target
#--------------------------------------------------------------------------#

#-------------------------------CROSSOVER----------------------------------#
def crossover(parent1,parent2, parent3):
    child1 = generate_genome()
    child2 = generate_genome()

    # multipoint sampling
    for i in range(3):
        for j in range(len(child1)):
            child1[j][i] = parent1[j][i]
            child2[j][i] = parent2[j][i]
    
    for i in range(2,4):
        for j in range(len(child1)):
            child2[j][i] = parent1[j][i]
            child1[j][i] = parent2[j][i]

    for i in range(4,5):
        for j in range(len(child1)):
            child1[j][i] = parent1[j][i]
            child2[j][i] = parent2[j][i]
            
    return [child1, child2]
#--------------------------------------------------------------------------#

#--------------------------------MUTATE------------------------------------#
def mutate(dna,mutation_rate):
    m = generate_genome()
    r = random.randint(0,4)
    rng = random.random()
    for i in range(len(dna)):
            if rng < mutation_rate:
                dna[i][r] = m[i][r]
    return dna
#--------------------------------------------------------------------------#

#-------------------------------DISPLAY------------------------------------#
def display(stdscr, restarts, generations, avg_fitness, pop_size, rate, best, best_score, startTime):
    space = [0,9,26,38,55,62]
    
    stdscr.addstr(1, 2, "Best So Far:")
    if best:
        for i in range(0,5):
            stdscr.addstr(i+2, 1,"{}".format('│'))
            stdscr.addstr(i+2, 69,"{}".format('│'))
            for j in range(0,6):
                stdscr.addstr(i+2, 3 + space[j], "{}".format(best[i][j]))
    stdscr.addstr(2, 1,"{}".format('┌'))
    stdscr.addstr(6, 1,"{}".format('└'))

    stdscr.addstr(2, 69,"{}".format('┐'))
    stdscr.addstr(6, 69,"{}".format('┘'))

    stdscr.addstr(8, 2, "{:<19}{}".format('Generations:',generations))
    stdscr.addstr(9, 2, "{:<19}{:.2f}%".format('Average fitness:',avg_fitness*100))
    stdscr.addstr(10, 2,"{:<19}{:.2f}%".format('Best Score:',best_score*100))
    stdscr.addstr(11, 2,"{:<19}{}".format('Population Size:',pop_size))
    stdscr.addstr(12, 2,"{:<19}{:.3f}".format('Mutation rate:', rate))
    stdscr.addstr(14, 2,"{:<19}{}".format('Restarts:',restarts))
    stdscr.addstr(15, 2,"{:<19}{:.1f}{}".format('Run time:',time.time() - startTime, ' Seconds'))
# -------------------------------------------------------------------------#

# ----------------------------BUILD GRAPH----------------------------------#
def buildGraph(stdscr, avg_fitness, generations, best_score, time, times):
    rows, cols = stdscr.getmaxyx()
    if cols < 149:
        return

    #  build axis
    for i in range (2,15):
        stdscr.addstr(i, 90,"{}".format('│'))
    stdscr.addstr(8, 90,"{}".format('┼'))
    stdscr.addstr(2, 90,"{}".format('┬'))
    stdscr.addstr(1, 87,"{:.0f}".format(100))
    stdscr.addstr(8, 87,"{:.0f}".format(50))
    stdscr.addstr(15, 90,"{}".format('└────────────────────────────────────────────────────'))
    stdscr.addstr(16, 90,"{}".format('0                    Generations                  100'))
    stdscr.addstr(5, 85,"Avg")
    stdscr.addstr(6, 82,"Fitness")

    fit = avg_fitness
    if(generations % 2 == 0):
        times.append(fit)
    
    #  Live Graph
    for i,time in enumerate(times):
        stdscr.addstr(15 - math.floor(time*15), 91+i,"{}".format('*'))
    
    #  Equaliser display
    stdscr.addstr(8, 30,"{}".format('[                                                  ]'))
    stdscr.addstr(9, 30,"{}".format('[                                                  ]'))
    stdscr.addstr(10,30,"{}".format('[                                                  ]'))

    for i in range(0, math.floor(generations/2)):
        stdscr.addstr(8, 31+i,"{}".format('■'))
    for i in range(0, math.floor(avg_fitness*100/2)):
        stdscr.addstr(9, 31+i,"{}".format('■'))
    for i in range(0, math.floor(best_score *100/2)):
        stdscr.addstr(10, 31+i,"{}".format('■'))
# -------------------------------------------------------------------------#

# -------------------------INTRO INFORMATION-------------------------------#
def showInfo(stdscr, mutation_rate, pop_size):    
   
    stdscr.addstr(2, 2,"{}".format('The Zebra Puzzle'))
    stdscr.addstr(4, 2,"{}".format('This program is a genetic algorithm writen to solve a variation of the zebra puzzle.'))
    stdscr.addstr(5, 2,"{}{}{}{}".format('The population is set at ',str(pop_size), ', with a fairly high mutation of ', mutation_rate))
    stdscr.addstr(6, 2,"{}".format('The GA tends to get stuck in a local optima, and i found that if its stuck by generation 100 it will tend to stay'))
    stdscr.addstr(7, 2,"{}".format('in that local optima. Therefore, every 100th generation, the population is cleared and the program is restarted.'))
    stdscr.addstr(8, 2,"{}".format('The amount of restarts can be found on the information pannel while the program is running. '))
    stdscr.addstr(9, 2,"{}".format('Selection is based off Roulette Wheel Selection with the mating pool being seeded by (individual_fitness/highest_fitness*10)^2'))
    stdscr.addstr(10, 2,"{}".format('of each induvidual in the population, which allows the fittest individuals a greater chance of selection when generating the'))
    stdscr.addstr(11, 2,"{}".format('next genration of individuals, while allowing some of the less fit individuals a chance. This is in an attempt to alleviate'))
    stdscr.addstr(12, 2,"{}".format('local optima. The new generation\'s population are generated from the previous generation, with 3 parents providing genetic'))
    stdscr.addstr(13, 2,"{}".format('material for two children. The crossover function is based on multipoint sampling, with entire columns of attributes being'))
    stdscr.addstr(14, 2,"{}{}".format('sampled at a time to avoid duplicate values in the resulting offspring. The offspring are mutated based on a probability of ', mutation_rate))
    stdscr.addstr(15, 2,"{}".format('and again entire attribute columns are mutated to avoid duplicates'))
    stdscr.addstr(16, 2,"{}".format('eg more that one red X-Trail.'))
    stdscr.addstr(20, 2,"{}".format('Program written by Adam Austin'))

# -------------------------------------------------------------------------#

# ---------------------------MAIN PROGRAM----------------------------------#
def run():

    # Display stuff
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    # Adjustables
    target = 21
    population_size = 600
    mutation_rate = 0.045
    restarts = -1

    times = []
    gen_times = []

    finished = False

    try:
        # Check screen dimensions
        while(True):
            rows, cols = stdscr.getmaxyx()
            if cols < 149 or rows < 29:
                stdscr.addstr(0, 0, "....Please resize the terminal window to 150x30 for optimal output....")
            else:
                break
            stdscr.refresh()

        # Show program introduction
        while(True):

            stdscr.clear()
            showInfo(stdscr, mutation_rate, population_size) 
            stdscr.addstr(22, 2, "Press the <S> key to start the program")   
            
            k = stdscr.getch()     
            if k == ord('s') or k == ord('S'):
                break
            stdscr.refresh()


        startTime = time.time()
        generations = 0

        
        while not finished:

            if generations % 100 == 0:
                restarts += 1
                generations = 0
                pop = gen_initial(population_size)
                times = []

            mating_pool = selection(pop,target)
            pop = generate(pop, mating_pool, mutation_rate)
            [best_indv, best_score, avg_score] = evaluate(pop,target)     
            
            stdscr.clear()
            display(stdscr,restarts, generations, avg_score, len(pop), mutation_rate, best_indv, best_score, startTime )
            buildGraph(stdscr, avg_score, generations, best_score, time.time()-startTime, times)
            stdscr.refresh()
            generations += 1
            if(best_score == 1):
                finished = True    
        
        # When solution is found, display it
        for i in range(len(best_indv)):
            stdscr.addstr(18+i, 2,"The {} {} was hired by the {} people, who left for {} at {} and took the {} car".format(best_indv[i][0], best_indv[i][1], best_indv[i][2], best_indv[i][3], best_indv[i][4], best_indv[i][5]))
        
        stdscr.addstr(25, 0, "....Program Ended. Press <Enter> key to exit or <S> to restart....")
            
        while(True):
            c = stdscr.getch()
            if c == ord('\n'):
                break;
            if c == ord('s') or c == ord('S'):
                run()
            stdscr.refresh()
            
    except (KeyboardInterrupt, SystemExit):
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()
        exit()
    except Exception as e:
        pass
    finally:
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()
# -------------------------------------------------------------------------#


if(__name__ == '__main__'):
    run()

