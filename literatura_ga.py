import random
from typing import List
from utils_tdr import adjacency_list_is_valid_trdf

STEP_GENS = 10

# HEURÍSTICA 1 (LITERATURA)
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

        chrom_list.append(f_list)

    return chrom_list

# HEURÍSTICA 2 (LITERATURA)
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

        chrom_list.append(f_list)

    return chrom_list

# HEURÍSTICA 3 (LITERATURA)
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

        chrom_list.append(f_list)

    return chrom_list

# HEURÍSTICA 4 (LITERATURA)
def heuristic_4(adjacencias, quantity):
    chrom_list = []
    for _ in range(quantity):
        f_list = [None for _ in adjacencias]
        verticie_atual = 0

        # === ETAPA 1: Construir solução inicial com Heurística 3 ===
        while None in f_list:
            while verticie_atual < len(adjacencias) and f_list[verticie_atual] is not None:
                verticie_atual += 1
            if verticie_atual >= len(adjacencias):
                break

            f_dict_vizinhos = {n: f_list[n] for n in adjacencias[verticie_atual]}
            unmarked_neighbors = [n for n in adjacencias[verticie_atual] if f_list[n] is None]

            if unmarked_neighbors:
                # Etapa 1: f(vi) = 2
                vi = verticie_atual
                f_list[vi] = 2

                # Etapa 2: Escolher vizinho com maior grau entre os não marcados
                vj = max(unmarked_neighbors, key=lambda x: len(adjacencias[x]))
                f_list[vj] = 1

                # Etapa 3: Marcar outros vizinhos com 0
                for viz in adjacencias[vi]:
                    if f_list[viz] is None:
                        f_list[viz] = 0
            else:
                # Se não tem vizinho não marcado → coloca f=1 e garante apoio
                f_list[verticie_atual] = 1
                if all(f_list[n] == 0 for n in adjacencias[verticie_atual]):
                    # Escolhe o vizinho de menor índice para apoio
                    f_list[min(adjacencias[verticie_atual])] = 1

        # === ETAPA 2: MELHORIA PARA VÉRTICES ISOLADOS (Heurística 4) ===
        # Identificar vértices com f(v) = 0 (isolados)
        isolados = [i for i, f in enumerate(f_list) if f == 0]
        if len(isolados) > 0:
            # Para cada isolado, garantir que tenha um vizinho com f=2
            for v in isolados:
                vizinhos = adjacencias[v]
                # Se nenhum vizinho tem f=2 → escolher um com maior grau
                if not any(f_list[u] == 2 for u in vizinhos):
                    # Escolher vizinho com maior grau
                    u = max(vizinhos, key=lambda x: len(adjacencias[x]))
                    f_list[u] = 2  # Mover ou adicionar f=2

                    # Garantir que o novo f=2 tenha apoio (f>0)
                    apoio = [n for n in adjacencias[u] if f_list[n] > 0]
                    if not apoio:
                        # Escolher um vizinho qualquer para apoio
                        apoio_candidato = random.choice(adjacencias[u])
                        f_list[apoio_candidato] = max(f_list[apoio_candidato] or 0, 1)

        # === ETAPA 3: TENTAR REDUZIR PESO (substituir f=2 por dois f=1) ===
        for i in range(len(f_list)):
            if f_list[i] == 2:
                vizinhos = adjacencias[i]
                candidatos_f1 = [u for u in vizinhos if f_list[u] <= 1]
                if len(candidatos_f1) >= 2:
                    u1, u2 = sorted(candidatos_f1, key=lambda x: len(adjacencias[x]), reverse=True)[:2]
                    # Testar substituição
                    temp = f_list.copy()
                    temp[i] = 0
                    temp[u1] = max(temp[u1], 1)
                    temp[u2] = max(temp[u2], 1)
                    # Verificar se ainda é TRDF
                    if adjacency_list_is_valid_trdf(adjacencias, temp) and sum(temp) < sum(f_list):
                        f_list = temp

        chrom_list.append(f_list)
    return chrom_list

# HEURÍSTICA 5 (LITERATURA)
def heuristic_5(adjacencias, quantity):
    chrom_list = []

    for _ in range(quantity):
        f_list = [1 for _ in adjacencias]

        chrom_list.append(f_list)

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
        pop.extend(heuristic_4(adjacencias, int(quantity * proporcao_heuristica_4)))
        pop.extend(heuristic_5(adjacencias, int(quantity * proporcao_heuristica_5)))

        # Devido arredondamentos, pode ser que a população gerada seja menor que o tamanho desejado
        while len(pop) < quantity:

            # Preenche o restante com soluções da heurística 1
            pop.extend(heuristic_1(adjacencias, quantity - len(pop)))

        return pop

    return generate_population

def repair_graph(adjacencias):
    def repair(chrom):
        f_list = chrom
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

        return f_list

    return repair
