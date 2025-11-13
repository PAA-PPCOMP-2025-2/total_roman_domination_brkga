# brkga_trd.py
import random
import time
from typing import List

from dataset_reader import leitura_matriz_adjacencia
from brkga import BRKGA

THRESHOLD_1 = 1/3
THRESHOLD_2 = 2/3

def decode(chrom: List[float]) -> List[int]:
    return [0 if g < THRESHOLD_1 else 1 if g < THRESHOLD_2 else 2 for g in chrom]

def code(f_list: List[int]) -> List[float]:
    def random_float(min_val, max_val):
        # return min_val + (max_val - min_val) * random.random()
        return (min_val + max_val) / 2.0

    chrom = []
    for f in f_list:
        if f == 0:
            chrom.append(random_float(0, THRESHOLD_1))
        elif f == 1:
            chrom.append(random_float(THRESHOLD_1, THRESHOLD_2))
        else:
            chrom.append(random_float(THRESHOLD_2, 1))

    return chrom

def repair_graph(adjacencias):
    def repair(chrom):
        f_list = decode(chrom)
        n = len(adjacencias)

        checados = [False for _ in adjacencias]

        # F(v) = 2
        for v in range(n):
            if checados[v]: continue
            if f_list[v] == 2:
                checados[v] = True
                possui_vizinho_apoio = False
                for u in adjacencias[v]:
                    checados[u] = True
                    if (f_list[u] > 0):
                        possui_vizinho_apoio = True
                if not possui_vizinho_apoio:
                    f_list[u] = 1

        # F(v) = 1
        for v in range(n):
            if checados[v]: continue
            if f_list[v] == 1:
                checados[v] = True
                possui_vizinho_apoio = False
                for u in adjacencias[v]:
                    if f_list[u] > 0:
                        possui_vizinho_apoio = True
                        checados[u] = True
                if not possui_vizinho_apoio:
                    f_list[u] = 1
                    checados[u] = True

        # F(v) = 0
        for v in range(n):
            if checados[v]: continue
            if f_list[v] == 0:
                f_list[v] = 2
                checados[v] = True
                for u in adjacencias[v]:
                    checados[u] = True
                f_list[u] = 1

        return code(f_list)

    return repair

def fitness(chrom):
    return float(sum(decode(chrom)))

# HEURÍSTICA 1 (ARTIGO)
def heuristic_1(adjacencias, quantity):
    chrom_list = []

    for _ in range(quantity):
        f_list = [None for _ in adjacencias]

        while None in f_list:
            # seleciona aleatoriamente dos que ainda não foram marcados
            verticie_atual = random.choice([v for v,f in enumerate(f_list) if f == None])

            f_dict_vizinhos = {n: f_list[n] for n in adjacencias[verticie_atual]}

            if len([f for f in f_dict_vizinhos.values() if f == None]) > 0:
                # etapa 1
                vi = verticie_atual
                f_list[vi] = 2

                # etapa 2
                vj = random.choice(adjacencias[vi])
                f_list[vj] = 1
                for viz in adjacencias[vi]:
                    if f_list[viz] == None:
                        f_list[viz] = 0
                
                # etapa 3 nao foi necessaria nesta implementação, pois não é criado uma cópia do grafo
                
            # etapa 4
            else:
                f_list[verticie_atual] = 1
                
                if len([f for f in f_dict_vizinhos.values() if f in (1,2)]) == 0:
                    f_list[random.choice(adjacencias[verticie_atual])] = 1

        chrom_list.append(code(f_list))

    return chrom_list

# HEURÍSTICA 2 (ARTIGO)
def heuristic_2(adjacencias, quantity):
    chrom_list = []

    for _ in range(quantity):
        f_list = [None for _ in adjacencias]

        verticie_atual = 0
        while None in f_list:
            # seleciona o proximo que ainda nao foi marcado
            # como os vertices ja estão ordenados pelo seu grau, então vai selecionar o vértice de maior grau que ainda não foi marcado
            while f_list[verticie_atual] is not None:
                verticie_atual += 1

            f_dict_vizinhos = {n: f_list[n] for n in adjacencias[verticie_atual]}

            if len([f for f in f_dict_vizinhos.values() if f == None]) > 0:
                # etapa 1
                vi = verticie_atual
                f_list[vi] = 2

                # etapa 2
                vj = random.choice(adjacencias[vi])
                f_list[vj] = 1
                for viz in adjacencias[vi]:
                    if f_list[viz] == None:
                        f_list[viz] = 0
                
                # etapa 3 nao foi necessaria nesta implementação, pois não é criado uma cópia do grafo
                
            # etapa 4
            else:
                f_list[verticie_atual] = 1
                
                if len([f for f in f_dict_vizinhos.values() if f in (1,2)]) == 0:
                    f_list[random.choice(adjacencias[verticie_atual])] = 1

        chrom_list.append(code(f_list))

    return chrom_list

# HEURÍSTICA 3 (ARTIGO)
def heuristic_3(adjacencias, quantity):
    chrom_list = []

    for _ in range(quantity):
        f_list = [None for _ in adjacencias]

        verticie_atual = 0
        while None in f_list:
            # seleciona o proximo que ainda nao foi marcado
            # como os vertices ja estão ordenados pelo seu grau, então vai selecionar o vértice de maior grau que ainda não foi marcado
            while f_list[verticie_atual] is not None:
                verticie_atual += 1

            f_dict_vizinhos = {n: f_list[n] for n in adjacencias[verticie_atual]}

            if len([f for f in f_dict_vizinhos.values() if f == None]) > 0:
                # etapa 1
                vi = verticie_atual
                f_list[vi] = 2

                # etapa 2
                vj = random.choice(adjacencias[vi])
                f_list[vj] = 1
                for viz in adjacencias[vi]:
                    if f_list[viz] == None:
                        f_list[viz] = 0
                
                # etapa 3 nao foi necessaria nesta implementação, pois não é criado uma cópia do grafo
                
            # etapa 4
            else:
                f_list[verticie_atual] = 1
                
                if len([f for f in f_dict_vizinhos.values() if f in (1,2)]) == 0:
                    f_list[min(adjacencias[verticie_atual])] = 1

        chrom_list.append(code(f_list))

    return chrom_list

# HEURÍSTICA 4 (ARTIGO)
def heuristic_4(adjacencias, quantity):
    # Não está claro como foi implementada essa heurística no artigo original

    return heuristic_1(adjacencias, quantity)

# HEURÍSTICA 5 (ARTIGO)
def heuristic_5(adjacencias, quantity):
    chrom_list = []

    for _ in range(quantity):
        f_list = [1 for _ in adjacencias]

        chrom_list.append(code(f_list))

    return chrom_list

def generate_population_graph(adjacencias):
    def generate_population(quantity):
        proporcao_heuristica_1 = 0.6
        proporcao_heuristica_2 = 0.1
        proporcao_heuristica_3 = 0.1
        proporcao_heuristica_4 = 0.1
        proporcao_heuristica_5 = 0.1

        pop = []
        pop.extend(heuristic_1(adjacencias, int(quantity * proporcao_heuristica_1)))
        pop.extend(heuristic_2(adjacencias, int(quantity * proporcao_heuristica_2)))
        pop.extend(heuristic_3(adjacencias, int(quantity * proporcao_heuristica_3)))
        pop.extend(heuristic_4(adjacencias, int(quantity * proporcao_heuristica_4))) # Não implementada, utilizando a heurística 1
        pop.extend(heuristic_5(adjacencias, int(quantity * proporcao_heuristica_5)))

        # Devido arredondamentos, pode ser que a população gerada seja menor que o tamanho desejado
        while len(pop) < quantity:

            # Preenche o restante com soluções da heurística 1
            pop.extend(heuristic_1(adjacencias, quantity - len(pop)))

        return pop

    return generate_population

if __name__ == "__main__":
    graphs = {
        # "MANN-a81": leitura_matriz_adjacencia("datasets/DIMACS/MANN-a81.mtx"),            # melhor: 5
        "C1000-9": leitura_matriz_adjacencia("datasets/DIMACS/C1000-9.mtx"),              # melhor: 5
        # "johnson8-2-4": leitura_matriz_adjacencia("datasets/DIMACS/johnson8-2-4.mtx"),    # melhor: 7
        # "MANN-a9": leitura_matriz_adjacencia("datasets/DIMACS/MANN-a9.mtx"),              # melhor: 5
    }

    for name, graph in graphs.items():
        n = len(graph)

        ag = BRKGA(
            n = n,
            pop_size=int(n/4.4056), 
            elite_frac=0.2262, 
            mutant_frac=0.2, 
            generations=1000
        )

        ag.fitness = fitness
        ag.generate_population = generate_population_graph(graph)
        ag.repair = repair_graph(graph)

        t0 = time.time()
        w, sol = ag.run()
        t1 = time.time()
        print(f'Tempo de processamento: {t1-t0} segundos')

        print(f"{name}: γtR = {w}")

        ordem = sorted(range(n), key=lambda x: sol[x])
