# brkga_trd.py
import random
import time
import networkx as nx
from typing import List

from dataset_reader import leitura_matriz_adjacencia
from visualização_gráfica import plot_trdf

STEP_GENS = 10
MAX_GENS_WITHOUT_IMPROVEMENT = 100 # no artigo utilizou 363
THRESHOLD_1 = 1/3
THRESHOLD_2 = 2/3
DEBUG = 0

class BRKGA_TRD:
    def __init__(self, G: nx.Graph, pop_size=300, elite_frac=0.2, mutant_frac=0.2, generations=1000):
        self.G = G
        self.n = len(G.nodes())
        self.idx_to_node = list(G.nodes())
        self.pop_size = pop_size
        self.elite_size = int(pop_size * elite_frac)
        self.mutant_size = int(pop_size * mutant_frac)
        self.generations = generations

    def decode(self, chrom: List[float]) -> List[int]:
        return [0 if g < THRESHOLD_1 else 1 if g < THRESHOLD_2 else 2 for g in chrom]

    def code(self, f_list: List[int]) -> List[float]:
        def random_float(min_val, max_val):
            return min_val + (max_val - min_val) * random.random()

        chrom = []
        for v,f in f_list.items():
            if f == 0:
                chrom.append(random_float(0, THRESHOLD_1))
            elif f == 1:
                chrom.append(random_float(THRESHOLD_1, THRESHOLD_2))
            else:
                chrom.append(random_float(THRESHOLD_2, 1))

        return chrom

    def is_valid_trdf(self, f_list: List[int]) -> bool:
        checados = [False for _ in range(self.n)]

        # F(v) = 2
        for v in self.G.nodes():
            if checados[v]: continue
            if f_list[v] == 2:
                checados[v] = True
                possui_vizinho_apoio = False
                for u in self.G.neighbors(v):
                    checados[u] = True
                    if (f_list[u] > 0):
                        possui_vizinho_apoio = True
                if not possui_vizinho_apoio:
                    return False

        # F(v) = 1
        for v in self.G.nodes():
            if checados[v]: continue
            if f_list[v] == 1:
                checados[v] = True
                possui_vizinho_apoio = False
                for u in self.G.neighbors(v):
                    if f_list[u] > 0:
                        possui_vizinho_apoio = True
                        checados[u] = True
                if not possui_vizinho_apoio:
                    return False

        # F(v) = 0
        for v in self.G.nodes():
            if checados[v]: continue
            return False

        return True

    def repair(self, f_list: List[int]) -> List[int]:
        checados = [False for _ in range(self.n)]

        # F(v) = 2
        for v in self.G.nodes():
            if checados[v]: continue
            if f_list[v] == 2:
                checados[v] = True
                possui_vizinho_apoio = False
                for u in self.G.neighbors(v):
                    checados[u] = True
                    if (f_list[u] > 0):
                        possui_vizinho_apoio = True
                if not possui_vizinho_apoio:
                    f_list[u] = 1

        # F(v) = 1
        for v in self.G.nodes():
            if checados[v]: continue
            if f_list[v] == 1:
                checados[v] = True
                possui_vizinho_apoio = False
                for u in self.G.neighbors(v):
                    if f_list[u] > 0:
                        possui_vizinho_apoio = True
                        checados[u] = True
                if not possui_vizinho_apoio:
                    f_list[u] = 1
                    checados[u] = True

        # F(v) = 0
        for v in self.G.nodes():
            if checados[v]: continue
            if f_list[v] == 0:
                f_list[v] = 2
                checados[v] = True
                for u in self.G.neighbors(v):
                    checados[u] = True
                f_list[u] = 1

        return f_list

    def fitness(self, chrom: List[float]) -> float:
        f_list = self.decode(chrom)
        f_list = self.repair(f_list)
        total = sum(f_list)
        penalty = 0
        
        # Muito custoso esse calculo de penalidade, tem diferença no resultado final?

        # f_dict = {self.idx_to_node[i]: f_list[i] for i in range(self.n)}
        # for v in self.G.nodes():
        #     val = f_dict[v]
        #     neighbors = list(self.G.neighbors(v))
        #     if val == 0:
        #         if not any(f_dict[u] == 2 for u in neighbors):
        #             penalty += 10  # forte penalidade
        #     else:
        #         if not any(f_dict[u] > 0 for u in neighbors):
        #             penalty += 10

        return total + penalty
    
    # HEURÍSTICA 1 (ARTIGO)
    def heuristic_1(self, quantity):
        chrom_list = []

        for i in range(quantity):
            f_list = {self.idx_to_node[i]: None for i in range(self.n)}

            while None in f_list.values():
                # seleciona aleatoriamente dos que ainda não forma marcados
                verticie_atual = random.choice([v for v,f in f_list.items() if f == None])

                f_list_vizinhos = {n: f_list[n] for n in self.G.neighbors(verticie_atual)}

                if len([f for f in f_list_vizinhos.values() if f == None]) > 0:
                    # etapa 1
                    vi = verticie_atual
                    f_list[vi] = 2

                    # etapa 2
                    vj = random.choice(list(self.G.neighbors(vi)))
                    f_list[vj] = 1
                    for viz in self.G.neighbors(vi):
                        if f_list[viz] == None:
                            f_list[viz] = 0
                    
                    # etapa 3 nao foi necessaria nesta implementação, pois não é criado uma cópia do grafo
                    
                # etapa 4
                else:
                    f_list[verticie_atual] = 1
                    
                    if len([f for f in f_list_vizinhos.values() if f in (1,2)]) == 0:
                        f_list[random.choice(list(self.G.neighbors(verticie_atual)))] = 1

            chrom_list.append(self.code(f_list))

        return chrom_list
    
    # HEURÍSTICA 2 (ARTIGO)
    def heuristic_2(self, quantity):
        chrom_list = []

        for i in range(quantity):
            f_list = {self.idx_to_node[i]: None for i in range(self.n)}

            verticie_atual = 0
            while None in f_list.values():
                # seleciona o proximo que ainda nao foi marcado
                # como os vertices ja estão ordenados pelo seu grau, então vai selecionar o vértice de maior grau que ainda não foi marcado
                while f_list[verticie_atual] is not None:
                    verticie_atual += 1

                f_list_vizinhos = {n: f_list[n] for n in self.G.neighbors(verticie_atual)}

                if len([f for f in f_list_vizinhos.values() if f == None]) > 0:
                    # etapa 1
                    vi = verticie_atual
                    f_list[vi] = 2

                    # etapa 2
                    vj = random.choice(list(self.G.neighbors(vi)))
                    f_list[vj] = 1
                    for viz in self.G.neighbors(vi):
                        if f_list[viz] == None:
                            f_list[viz] = 0
                    
                    # etapa 3 nao foi necessaria nesta implementação, pois não é criado uma cópia do grafo
                    
                # etapa 4
                else:
                    f_list[verticie_atual] = 1
                    
                    if len([f for f in f_list_vizinhos.values() if f in (1,2)]) == 0:
                        f_list[random.choice(list(self.G.neighbors(verticie_atual)))] = 1

            chrom_list.append(self.code(f_list))

        return chrom_list
    
    # HEURÍSTICA 3 (ARTIGO)
    def heuristic_3(self, quantity):
        chrom_list = []

        for i in range(quantity):
            f_list = {self.idx_to_node[i]: None for i in range(self.n)}

            verticie_atual = 0
            while None in f_list.values():
                # seleciona o proximo que ainda nao foi marcado
                # como os vertices ja estão ordenados pelo seu grau, então vai selecionar o vértice de maior grau que ainda não foi marcado
                while f_list[verticie_atual] is not None:
                    verticie_atual += 1

                f_list_vizinhos = {n: f_list[n] for n in self.G.neighbors(verticie_atual)}

                if len([f for f in f_list_vizinhos.values() if f == None]) > 0:
                    # etapa 1
                    vi = verticie_atual
                    f_list[vi] = 2

                    # etapa 2
                    vj = random.choice(list(self.G.neighbors(vi)))
                    f_list[vj] = 1
                    for viz in self.G.neighbors(vi):
                        if f_list[viz] == None:
                            f_list[viz] = 0
                    
                    # etapa 3 nao foi necessaria nesta implementação, pois não é criado uma cópia do grafo
                    
                # etapa 4
                else:
                    f_list[verticie_atual] = 1
                    
                    if len([f for f in f_list_vizinhos.values() if f in (1,2)]) == 0:
                        f_list[min(list(self.G.neighbors(verticie_atual)))] = 1

            chrom_list.append(self.code(f_list))

        return chrom_list
    
    # HEURÍSTICA 4 (ARTIGO)
    def heuristic_4(self, quantity):
        # Não está claro como foi implementada essa heurística no artigo original

        return self.heuristic_1(quantity)
    
    # HEURÍSTICA 5 (ARTIGO)
    def heuristic_5(self, quantity):
        chrom_list = []

        for i in range(quantity):
            f_list = {self.idx_to_node[i]: 1 for i in range(self.n)}

            chrom_list.append(self.code(f_list))

        return chrom_list
    
    # HEURÍSTICA 2 (ALTERNATIVA)
    def heuristic_2_alt(self, quantity) -> List[float]:
        f_list = [self.decode(chrom) for chrom in self.heuristic_1(quantity)]
        for i in range(quantity):
            if f_list[i] == 2:
                neighbors = list(self.G.neighbors(self.idx_to_node[i]))
                if len(neighbors) >= 2:
                    u1, u2 = neighbors[0], neighbors[1]
                    u1_idx, u2_idx = self.node_to_idx[u1], self.node_to_idx[u2]
                    if f_list[u1_idx] <= 1 and f_list[u2_idx] <= 1:
                        temp = f_list.copy()
                        temp[i] = 0
                        temp[u1_idx] = max(temp[u1_idx], 1)
                        temp[u2_idx] = max(temp[u2_idx], 1)
                        if self.is_valid_trdf(temp) and sum(temp) < sum(f_list):
                            f_list = temp
        return [self.code(chrom) for chrom in f_list]

    # HEURÍSTICA 3 (ALTERNATIVA)
    def heuristic_3_alt(self, quantity) -> List[float]:
        f_list = self.decode(self.heuristic_1(quantity))
        for i in range(quantity):
            if f_list[i] == 1:
                v = self.idx_to_node[i]
                neighbors = list(self.G.neighbors(v))
                if any(f_list[self.node_to_idx[u]] == 2 for u in neighbors):
                    temp = f_list.copy()
                    temp[i] = 0
                    if self.is_valid_trdf(temp):
                        f_list = temp
        return self.code(f_list)

    # HEURÍSTICA 4 (ALTERNATIVA)
    def heuristic_4_alt(self, quantity) -> List[float]:
        f_list = self.decode(self.heuristic_1(quantity))
        for i in range(quantity):
            if f_list[i] == 2:
                v = self.idx_to_node[i]
                for u in self.G.neighbors(v):
                    u_idx = self.node_to_idx[u]
                    if f_list[u_idx] == 0:
                        temp = f_list.copy()
                        temp[i] = 0
                        temp[u_idx] = 2
                        if self.is_valid_trdf(temp) and sum(temp) <= sum(f_list):
                            f_list = temp
        return self.code(f_list)

    # HEURÍSTICA 5 (ALTERNATIVA)
    def heuristic_5_alt(self, quantity) -> List[float]:
        chrom = self.heuristic_1(quantity)
        for h in [self.heuristic_2, self.heuristic_3, self.heuristic_4]:
            candidate = h()
            if self.fitness(candidate) < self.fitness(chrom):
                chrom = candidate
        return chrom
    
    # HEURÍSTICA 6 (ALTERNATIVA)
    def heuristic_6_alt(self):
        """Gera solução com γtR = 3: 1 f=2 + 2 f=1 + 2 f=0"""
        f_list = [0] * self.n
        if self.n < 5: return f_list
        
        # C5: vértices 0-1-2-3-4-0
        # P5: vértices 0-1-2-3-4
        # Estratégia: f(2)=2, f(1)=1, f(3)=1, f(0)=0, f(4)=0
        f_list[self.node_to_idx[0]] = 0
        f_list[self.node_to_idx[1]] = 1
        f_list[self.node_to_idx[2]] = 2
        f_list[self.node_to_idx[3]] = 1
        f_list[self.node_to_idx[4]] = 0
        
        return f_list

    # HEURÍSTICA 7 (ALTERNATIVA)
    def heuristic_7_alt(self):
        """Gera solução com γtR = 2: 1 f=2 + resto f=0"""
        f_list = [0] * self.n
        if self.n == 0: return f_list
        f_list[0] = 2
        return f_list

    def generate_population(self, quantity):
        proporcao_heuristica_1 = 0.6
        proporcao_heuristica_2 = 0.1
        proporcao_heuristica_3 = 0.1
        proporcao_heuristica_4 = 0.1
        proporcao_heuristica_5 = 0.1

        pop = []
        pop.extend(self.heuristic_1(int(quantity * proporcao_heuristica_1)))
        pop.extend(self.heuristic_2(int(quantity * proporcao_heuristica_2)))
        pop.extend(self.heuristic_3(int(quantity * proporcao_heuristica_3)))
        pop.extend(self.heuristic_4(int(quantity * proporcao_heuristica_4))) # Não implementada, utilizando a heurística 1
        pop.extend(self.heuristic_5(int(quantity * proporcao_heuristica_5)))

        # Devido arredondamentos, pode ser que a população gerada seja menor que o tamanho desejado
        while len(pop) < quantity:

            # Preenche o restante com soluções da heurística 1
            pop.extend(self.heuristic_1(quantity - len(pop)))

        return pop

    def biased_crossover(self, p1: List[float], p2: List[float]) -> List[float]:
        return [p1[i] if random.random() < self.bias else p2[i] for i in range(self.n)]

    def mutate_population(self) -> List[List[float]]:
        return [[random.random() for _ in range(self.n)] for _ in range(self.mutant_size)]

    def run(self):
        best_fit = None
        best_chrom = None
        gens_without_improvement = 0
        pop = self.generate_population(self.pop_size)

        # avaliação da primeira geração
        if self.generations > 0:
            current_scored = [(self.fitness(c), c) for c in pop]

        for gen in range(self.generations):
            current_scored.sort(key=lambda x: x[0])
            elites = [c for _, c in current_scored[:self.elite_size]]

            # Reprodução
            new_pop = elites.copy()
            while len(new_pop) < self.pop_size - self.mutant_size:
                p1 = random.choice(elites)
                p2 = random.choice(pop)
                child = [p1[i] if random.random() < 0.7 else p2[i] for i in range(self.n)]
                new_pop.append(child)

            # Mutantes
            new_pop.extend(self.generate_population(self.mutant_size))

            pop = new_pop

            if gen % STEP_GENS == 0 or gen == self.generations-1:
                current_scored = [(self.fitness(c), c) for c in pop]
                new_best_fit, new_best_chrom = min(current_scored)
                print(f"Gen {gen:3d} | γtR ≈ {new_best_fit}")

                if not best_chrom is None and  new_best_fit == best_fit:
                    gens_without_improvement += STEP_GENS

                    if gens_without_improvement >= MAX_GENS_WITHOUT_IMPROVEMENT:
                        print(f"Não foi encontrada uma solução melhor em {MAX_GENS_WITHOUT_IMPROVEMENT} gerações.")
                        print("Interrompendo o processamento.")
                        break
                else:
                    best_fit = new_best_fit
                    best_chrom = new_best_chrom
                    gens_without_improvement = 0

                if self.G.number_of_nodes() >= 3 and best_fit <= 3:
                    print("Solução ótima encontrada!")
                    break

        # Melhor solução final
        best_fit, best_chrom = min(current_scored)
        best_list = self.repair(self.decode(best_chrom))
        best_sol = {self.idx_to_node[i]: best_list[i] for i in range(self.n)}
        return best_fit, best_sol

if __name__ == "__main__":
    graphs = {
        # "MANN-a81": leitura_matriz_adjacencia("datasets/DIMACS/MANN-a81.mtx"),
        # "C1000-9": leitura_matriz_adjacencia("datasets/DIMACS/C1000-9.mtx"),
        # "johnson8-2-4": leitura_matriz_adjacencia("datasets/DIMACS/johnson8-2-4.mtx"),
        "MANN-a9": leitura_matriz_adjacencia("datasets/DIMACS/MANN-a9.mtx"),
    }

    for name, G in graphs.items():
        brkga_trd = BRKGA_TRD(
            G, 
            pop_size=int(G.number_of_nodes()/4.4056), 
            elite_frac=0.2262, 
            mutant_frac=0.2, 
            generations=586
        )

        t0 = time.time()
        w, sol = brkga_trd.run()
        t1 = time.time()
        print(f'Tempo de processamento: {t1-t0} segundos')

        print(f"{name}: γtR = {w}")
        # print(f"solução = {sol.values()}")

        # plot_trdf(G, sol, title=name)
