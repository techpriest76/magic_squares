import random

# problema de optimizacao
#
# representacao como uma lista de ordena de inteiros sem repeticao (permutacao)
# mutacao de inversaio
#
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
#
# numero de somas = (columnas + filas + diagonales) = (2*n)+2
# resultao da soma = n((n**2)+1)/2

def gerar(N,L):
    pop = []
    while len(pop)<N:
        individuo=[]
        while len(individuo)<(L**2):
            valor = random.randint(1,(L**2))
            while valor not in individuo:
                individuo.append(valor)
        x0=[]
        cromossomo=[]
        for i in individuo:
            x0.append(i)
            if len(x0)==L:
                cromossomo.append(x0)
                x0=[]
        pop.append(cromossomo)
    return(pop)

# mudar para fitness baseado em distancia e nao em bloco
def calc_fitness(cromossomo,L):
    fitness=(2*L)+2
    x1=[]
    #filas e colunas
    for i in range(len(cromossomo)):
        x1.append(cromossomo[i])
        xs1 = []
        for j in range(L):
               xs1.append(cromossomo[j][i])
        x1.append(xs1)
    #diagonais
    while len(x1)<fitness:
        diagonal1 = []
        diagonal2 = []
        for i in range(L):
            diagonal1.append(cromossomo[i][i])
            diagonal2.append(cromossomo[i][L-1-i])
        x1.append(diagonal1)
        x1.append(diagonal2)
# resultado da soma = n((n**2)+1)/2
    for i in x1:
        soma=0
        for j in i:
            soma+=j
        if soma == L*(1+(L**2))/2:
            fitness-=1
    return(fitness)     

def torneio(participantes,L):
    ganhadores = []
    while len(ganhadores) < len(participantes):
        concursantes=[]
        fitness_concursantes=[]
        pos1=random.randint(0,len(participantes)-1)
        pos2=random.randint(0,len(participantes)-1)
        concursantes.append(participantes[pos1])
        concursantes.append(participantes[pos2])
        for i in concursantes:
            fitness_concursantes.append(calc_fitness(i,L))
        indice=fitness_concursantes.index(min(fitness_concursantes))
        ganhadores.append(concursantes[indice])
    return ganhadores

def recombinacao(participantes,pc): #recombinacao PMX
    recombinados=[]
    for i in participantes:
        probabilidade=random.random()
        if probabilidade<=pc:
            filho=[]
            scp=[]
            ncp=[]
            pai=participantes[random.randint(0,len(participantes)-1)]
            ##### 2D TO 1D ##########
            pai1=[]
            pai2=[]
            for j in i:
                for k in j:
                    pai1.append(k)
            for j in pai:
                for k in j:
                    pai2.append(k)
            #########################
            ponto1=random.randint(0,len(pai1)-1)
            ponto2=random.randint(ponto1,len(pai1)-1)
            filho[0:ponto1]=[0]*ponto1
            filho[ponto1:ponto2]=pai1[ponto1:ponto2]
            scp[ponto1:ponto2]=pai1[ponto1:ponto2]
            filho[ponto2:len(pai1)]=[0]*(len(pai1)-ponto2)
            ncp[ponto1:ponto2]=pai2[ponto1:ponto2]
            for i in range(len(ncp)):
                if ncp[i] not in scp or ncp[i] not in filho:
                    pos=pai2.index(scp[i])
                    if filho[pos]==0:
                        filho[pos]=ncp[i]
                    else:
                        r=pai2[pai1.index(ncp[i])]
                        pos2=pai1.index(r)
                        pos3=pai2.index(ncp[i])
                        filho[pos2]=pai2[pos3]
            filho.reverse()
            for i in range(len(filho)):
                if filho[i]==0:
                    for j in pai2:
                        if j not in filho:
                            filho[i]=j
            filho.reverse()
            recombinados.append(filho)
        else:
            pai1=[]
            for j in i:
                for k in j:
                    pai1.append(k)
            recombinados.append(pai1)
    return recombinados

def mutar(participantes,pm,L):
    mutados=[]
    for i in participantes:
        mutado=[]
        mutado2=[]
        probabilidade=random.random()
        if probabilidade<=pm:
            pos1=random.randint(0,len(i)-1)
            pos2=random.randint(0,len(i)-1)
            segmento=i[pos1:pos2]
            segmento.reverse()
            mutado[0:pos1]=i[0:pos1]
            mutado[pos1:pos2]=segmento[0:len(segmento)]
            mutado[pos2:len(i)]=i[pos2:len(i)]
        else:
            mutado=i
        for j in range(0,len(mutado),L):
            x=j
            mutado2.append((mutado[j:j+L]))
            if len(mutado2)==L:
                mutados.append(mutado2)
    return(mutados)

def melhor(participantes,L):
    melhor =calc_fitness(participantes[0],L)
    indice = 0
    for i in range(len(participantes)):
        if calc_fitness(participantes[i],L)<melhor:
            melhor=calc_fitness(participantes[i],L)
            indice = i
    return(participantes[indice],melhor)

def elitismo(pop1,fitness1,pop2,fitness2,elite):
    fi=[]
    fi2=[]
    purga=[]
    for i in range(len(pop1)):
        sfi=[]
        sfi2=[]
        sfi.append(fitness1[i])
        sfi.append(i)
        sfi2.append(fitness2[i])
        sfi2.append(i)
        fi.append(sfi)
        fi2.append(sfi2)
    fi.sort(key=lambda sfi:sfi[0])
    fi2.sort(reverse=True, key=lambda sfi2:sfi2[0])
    k=int(len(pop1)*elite)
    purga[0:k]=pop1[0:k]
    purga[k:len(pop1)]=pop2[k:len(pop1)]
    return purga


###############################################################################
###############################################################################
###############################################################################
###############################################################################

L=3
N=200
pc=0.8
pm=0.5
semente=1729
rodada=0
geracoes=500
elite=0.05

melhores=[]
melhores_fit=[]
num_gera=[]

while rodada<10:
    random.seed(semente+rodada)
    melhor_r=0
    melhor_r_fit=(L*((L**2)+1))/2
    best_gera=0
    rodada+=1
    populacao=gerar(N,L)
    for i in populacao:
        geracao=0
    while geracao<geracoes:
        print('rodada: ',rodada)
        ganhadores=torneio(populacao,L) 
        recombinados=recombinacao(ganhadores,pc)
        mutados=mutar(recombinados,pm,L)
        fitness_pop=[]
        fitness_mut=[]
        for i in range(len(populacao)): 
            fitness_pop.append(calc_fitness(populacao[i],L))
            fitness_mut.append(calc_fitness(mutados[i],L))
        populacao=elitismo(populacao,fitness_pop,mutados,fitness_mut,elite)
        best=melhor(populacao,L)
        print(best[0],'-------',' geracao: ',(geracao+1),'-------','fitness:',(calc_fitness(best[0],L)))
        if best[1]==0:
            melhor_r=best[0]
            melhor_r_fit=best[1]
            best_gera=geracao
            break
        if melhor_r_fit>best[1]:
            melhor_r_fit=best[1]
            melhor_r=best[0]
            best_gera=geracao
        geracao+=1
    num_gera.append(best_gera)
    melhores.append(melhor_r)
    melhores_fit.append(melhor_r_fit)
    print(' ')

print('################## Melhor de cada rodada #########################')
print(' ')
for i in range(len(melhores)):
    for j in melhores[i]:
        print(j)
    print('fit ---',melhores_fit[i],'geracao ---',num_gera[i]) 
    print(' ')

