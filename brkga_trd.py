# brkga_trd.py
import random
import time
import networkx as nx
from typing import List

from dataset_reader import leitura_matriz_adjacencia
from visualização_gráfica import plot_trdf

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
        return [0 if g < 1/3 else 1 if g < 2/3 else 2 for g in chrom]

    def is_valid_trdf(self, f_list: List[int]) -> bool:
        """Checa se a função f_list é uma TRDF total"""
        for i, val in enumerate(f_list):
            if val == 0:
                node = self.idx_to_node[i]
                if not any(f_list[self.node_to_idx[n]] == 2 for n in self.G.neighbors(node)):
                    return False
            elif val > 0:
                node = self.idx_to_node[i]
                if not any(f_list[self.node_to_idx[n]] > 0 for n in self.G.neighbors(node)):
                    return False
        return True
    
    def repair(self, f_list: List[int]) -> List[int]:
        f_dict = {self.idx_to_node[i]: f_list[i] for i in range(self.n)}
        for v in self.G.nodes():
            if f_dict[v] == 0:
                if not any(f_dict[u] == 2 for u in self.G.neighbors(v)):
                    # Escolhe primeiro vizinho que ainda não é 2
                    for u in self.G.neighbors(v):
                        if f_dict[u] != 2:
                            f_dict[u] = 2
                            break

            elif f_dict[v] > 0:
                if not any(f_dict[u] > 0 for u in self.G.neighbors(v)):
                    # Escolhe primeiro vizinho que ainda não é > 0
                    for u in self.G.neighbors(v):
                        if f_dict[u] <= 0:
                            f_dict[u] = 1
                            break
        return [f_dict[self.idx_to_node[i]] for i in range(self.n)]

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

    def heuristic_gamma_3(self):
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

    def heuristic_gamma_2(self):
        """Gera solução com γtR = 2: 1 f=2 + resto f=0"""
        f_list = [0] * self.n
        if self.n == 0: return f_list
        f_list[0] = 2
        return f_list

    def generate_population(self):
        pop = []
        while len(pop) < self.pop_size:
            chrom = [random.random() for _ in range(self.n)]
            f_list = self.decode(chrom)
            f_list = self.repair(f_list)
            pop.append(chrom)
        return pop

    def biased_crossover(self, p1: List[float], p2: List[float]) -> List[float]:
        return [p1[i] if random.random() < self.bias else p2[i] for i in range(self.n)]

    def mutate_population(self) -> List[List[float]]:
        return [[random.random() for _ in range(self.n)] for _ in range(self.mutant_size)]

    def run(self):
        pop = self.generate_population()
        for gen in range(self.generations):
            # Avaliar população
            scored = [(self.fitness(c), c) for c in pop]
            scored.sort(key=lambda x: x[0])
            elites = [c for _, c in scored[:self.elite_size]]

            # Reprodução
            new_pop = elites.copy()
            while len(new_pop) < self.pop_size - self.mutant_size:
                p1 = random.choice(elites)
                p2 = random.choice(pop)
                child = [p1[i] if random.random() < 0.7 else p2[i] for i in range(self.n)]
                new_pop.append(child)

            # Mutantes aleatórios
            for _ in range(self.mutant_size):
                new_pop.append([random.random() for _ in range(self.n)])

            pop = new_pop

            if gen % 100 == 0 or gen == self.generations-1:
                best_fit, best_chrom = min((self.fitness(c), c) for c in pop)
                print(f"Gen {gen:3d} | γtR ≈ {best_fit}")

                if self.G.number_of_nodes() >= 3 and best_fit <= 3:
                    print("Solução ótima encontrada!")
                    break

        # Melhor solução final
        best_fit, best_chrom = min((self.fitness(c), c) for c in pop)
        best_list = self.repair(self.decode(best_chrom))
        best_sol = {self.idx_to_node[i]: best_list[i] for i in range(self.n)}
        return best_fit, best_sol

if __name__ == "__main__":
    graphs = {
        # "C1000-9": leitura_matriz_adjacencia("datasets/DIMACS/C1000-9.mtx"),
        # "johnson8-2-4": leitura_matriz_adjacencia("datasets/DIMACS/johnson8-2-4.mtx"),
        "MANN-a9": leitura_matriz_adjacencia("datasets/DIMACS/MANN-a9.mtx"),
    }

    for name, G in graphs.items():
        brkga_trd = BRKGA_TRD(G, pop_size=300, elite_frac=0.2, mutant_frac=0.2, generations=1000)

        t0 = time.time()
        w, sol = brkga_trd.run()
        t1 = time.time()
        print(f'Tempo de processamento: {t1-t0} segundos')

        print(f"{name}: γtR = {w}, solução = {sol}")
        plot_trdf(G, sol, title=name)