import random
# optimization problem
#
# representation as an ordered integer list with no repetition (permutation)

#
#               += 15   |                   +=  34
#   2 | 7 | 6   += 15   |   1 | 14 | 4 | 15     +=34
#   9 | 5 | 1   += 15   |   8 | 11 | 5 | 10     +=34
#   4 | 3 | 8   += 15   |   13|  2 | 16| 3      +=34
#   +=  +=  +=  +=      |   12|  7 | 9 | 6      +=34
#   15  15  15  15      |   +=  +=  +=  +=  +=
#                       |   34  34  34  34      34
#                       |
#
# number of sums = (columns + rows + diagonals) = (2*n)+2
# magic number = n((n**2)+1)/2


def generate(population_size, square_size):
    pop=[]
    while len(pop)<population_size:
        extended_chromosome=[]
        while len(extended_chromosome)<square_size**2:
            value = random.randint(1,(square_size**2))
            while value not in extended_chromosome:
                extended_chromosome.append(value)
        chromosome=[]
        sub_chromosome=[]
        for element in extended_chromosome:
            sub_chromosome.append(element)
            if len(sub_chromosome)==square_size:
                chromosome.append(sub_chromosome)
                sub_chromosome=[]
        pop.append(chromosome)
    return pop

def calc_fitness(chromosome, square_size):
    fitness=(2*square_size)+2
    sub_chromosome=[]
    #rows and columns
    for i in range(len(chromosome)):
        sub_chromosome.append(chromosome[i])
        temp1=[]
        for j in range(square_size):
            temp1.append(chromosome[i][j])
        sub_chromosome.append(temp1)
    #diagonals
    while len(sub_chromosome)<fitness:
        diagonal1=[]
        diagonal2=[]
        for i in range(len(chromosome)):
            diagonal1.append(chromosome[i][i])
            diagonal2.append(chromosome[i][square_size-1-i])
        sub_chromosome.append(diagonal1)
        sub_chromosome.append(diagonal2)
    #fitnes calculation
    for element in sub_chromosome:
        sum = 0
        for i in element:
            sum+=i
        if sum == square_size*(1+(square_size**2))/2:
            fitness-=1
    return fitness

def binary_tournament(contestants, square_size):
    winners=[]
    while len(winners)<len(contestants):
        participants=[]
        participants_fitness=[]
        position1=random.randint(0,len(contestants)-1)
        position2=random.randint(0,len(contestants)-1)
        participants.append(contestants[position1])
        participants.append(contestants[position2])
        for i in participants:
            participants_fitness.append(calc_fitness(i,square_size))
        index =  participants_fitness.index(min(participants_fitness))
        winners.append(participants[index])
    return winners

def crossover_PMX(participants, crossover_rate):
    offspring=[]
    for i in participants:
        probability=random.random()
        if probability<=crossover_rate:
            child=[]
            scp=[]
            ncp=[]
            parent0=participants[random.randint(0,len(participants)-1)]
            # transform from 2D to 1D
            parent1=[]
            parent2=[]
            for j in i:
                for k in j:
                    parent1.append(k)
            for j in parent0:
                for k in j:
                    parent2.append(k)
            #PMX
            point1=random.randint(0,len(parent1)-1)
            point2=random.randint(point1,len(parent1)-1)
            child[0:point1]=[0]*point1
            child[point1:point2]=parent1[point1:point2]
            child[point2:len(parent1)]=[0]*(len(parent1)-point2)
            scp[point1:point2]=parent1[point1:point2]
            scp[point1:point2]=parent2[point1:point2]
            for i in range(len(ncp)):
                if ncp[i] not in scp or ncp[i] not in filho:
                    position=parent2.index(scp[i])
                    if child[position]==0:
                        child[position]=ncp[i]
                    else:
                        r=parent2[parent1.index(ncp[i])]
                        position1=parent1.index(r)
                        position2=parent2.index(ncp[i])
                        child[position1]=parent2[position2]
            child.reverse()
            for i in range(len(child)):
                if child[i]==0:
                    for j in parent2:
                        if j not in child:
                            child[i]=j
            child.reverse()
            offspring.append(child)
        else:
            parent0=[]
            for j in i:
                for k in j:
                    parent0.append(k)
            offspring.append(parent0)
    return offspring

def mutate(participants, mutation_rate, square_size):
    mutants=[]
    for i in participants:
        mutant=[]
        for j in range(len(i)):
            probability=random.random()
            if probability<=mutation_rate:
                position1=random.randint(0,len(i)-1)
                position2=random.randint(0,len(i)-1)
                i[position1],i[position2]=i[position2],i[position1]
        #back to 2D from 1D
        for j in range(0,len(i),square_size):
            mutant.append((i[j:j+square_size]))
            if len(mutant)==square_size:
                mutants.append(mutant)
    return mutants

def best(participants,square_size):
    best=calc_fitness(participants[0],square_size)
    index=0
    for i in range(len(participants)):
        if calc_fitness(participants[i],square_size)<best:
            best=calc_fitness(participants[i],square_size)
            index=i
    return (participants[index],best)

def elitism(pop1, fitness1, pop2, fitness2, elite_size):
    fitness_index1 = []
    fitness_index2 = []
    purged = []
    for i in range(len(pop1)):
        sub_fitness_index1 = [fitness1[i], i]
        sub_fitness_index2 = [fitness2[i], i]
        fitness_index1.append(sub_fitness_index1)
        fitness_index2.append(sub_fitness_index2)
    fitness_index1.sort(key=lambda sfi: sfi[0])
    fitness_index2.sort(reverse=True, key=lambda sfi2: sfi2[0])
    cut_point = int(len(pop1) * elite_size)
    purged = pop1[:cut_point] + pop2[cut_point:]
    return purged


##########################################################

random_seed=1729
population_size=500
square_size=4
crossover_rate=0.8
mutation_rate=1/(square_size**2)
max_generations=2000
elite_size=0.01
max_cycles=10
current_cycle=0

best_individuals_overall=[]
best_fitness_overall=[]
number_of_generations=[]


while (current_cycle<max_cycles):
    random.seed(random_seed+current_cycle)
    best_individual=[]
    best_generation_number=0
    best_from_cycle=[]
    best_fitness_from_cycle=(square_size*((square_size**2)+1))/2
    current_generation=0
    pop = generate(population_size,square_size)
    #old_pop=pop.copy()
    while(current_generation<max_generations):
        print('Cycle number: ', current_cycle+1)
        winners=binary_tournament(pop,square_size)
        offspring=crossover_PMX(winners,crossover_rate)
        mutants=mutate(offspring,mutation_rate,square_size)
        fitness_pop=[]
        fitness_mutants=[]
        for i in range(len(pop)):
            fitness_pop.append(calc_fitness(pop[i],square_size))
            fitness_mutants.append(calc_fitness(mutants[i],square_size))
        pop=elitism(pop,fitness_pop,mutants,fitness_mutants,elite_size)
        best_individual=best(pop,square_size)
        print(best_individual[0],'-------',' generation: ',(current_generation+1),'-------','fitness:',(calc_fitness(best_individual[0],square_size)))
        if best_individual[1]==0:
            best_from_cycle=best_individual[0]
            best_fitness_from_cycle=best_individual[1]
            best_generation_number=current_generation
            break
        if best_fitness_from_cycle>best_individual[1]:
            best_fitness_from_cycle=best_individual[1]
            best_from_cycle=best_individual[0]
            best_generation_number=current_generation
        current_generation+=1
    number_of_generations.append(best_generation_number)
    best_individuals_overall.append(best_from_cycle)
    best_fitness_overall.append(best_fitness_from_cycle)
    print("")
    current_cycle+=1
print('####### best from each cycle: #######')
print(' ')
for i in range(len(best_individuals_overall)):
    for j in best_individuals_overall[i]:
        print(j)
    print('fit ---',best_fitness_overall[i],'generation ---',number_of_generations[i])
    print(' ')
