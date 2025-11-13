import random
from typing import List

STEP_GENS = 10

class GA:
    def __init__(
            self, 
            n, 
            pop_size, 
            elite_frac, 
            taxa_mutacao, 
            generations,
            tam_torneio, 
            max_gens_without_improvement=100, 
            max_optimal_solution=None, 
            print_generations=False
        ):

        self.n = n
        self.pop_size = pop_size
        self.elite_size = int(pop_size * elite_frac)
        self.taxa_mutacao = taxa_mutacao
        self.generations = generations
        self.tam_torneio = tam_torneio
        self.max_gens_without_improvement = max_gens_without_improvement
        self.max_optimal_solution = max_optimal_solution
        self.print_generations = print_generations

    def repair(self, chrom: List[int]) -> List[int]:
        return chrom

    def fitness(self, chrom: List[int]) -> int:
        return sum(chrom)
    
    def generate_population(self, quantity: int) -> List[List[float]]:
        pop = [[random.random() for _ in range(self.n)] for _ in range(quantity)]

        return pop

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
            while len(new_pop) < self.pop_size:
                # k-tournament selection
                candidatos = random.sample(pop, self.tam_torneio)
                candidatos.sort(key=lambda x: self.fitness(x))
                p1 = candidatos[0]
                
                # k-tournament selection
                p2 = None
                while p2 == None or p2 == p1:
                    candidatos = random.sample(pop, self.tam_torneio)
                    candidatos.sort(key=lambda x: self.fitness(x))
                    p2 = candidatos[0]

                # one-point crossover
                ponto_corte = random.randint(1, len(p1)-1)
                child = p1[:ponto_corte] + p2[ponto_corte:]

                # reparo
                child = self.repair(child)

                new_pop.append(child)
            
            # Mutantes
            for i,chrom in enumerate(new_pop):
                gene_alterado = False
                for j,gene in enumerate(chrom):
                    r = random.random()
                    if r < self.taxa_mutacao:
                        chrom[j] = 0
                        gene_alterado = True
                
                if gene_alterado:
                    new_pop[i] = self.repair(chrom)

            pop = new_pop

            current_scored = [(self.fitness(c), c) for c in pop]

            new_best_fit, new_best_chrom = min(current_scored)

            if best_fit is None or new_best_fit < best_fit:
                best_fit = new_best_fit
                best_chrom = new_best_chrom
                gens_without_improvement = 0
            elif new_best_fit == best_fit:
                gens_without_improvement += 1

            if gens_without_improvement >= self.max_gens_without_improvement:
                print(f"Não foi encontrada uma solução melhor em {self.max_gens_without_improvement} gerações.")
                print("Finalizando o código.")
                break

            if best_fit <= self.max_optimal_solution:
                print("Solução ótima encontrada!")
                break

            if self.print_generations and gen % STEP_GENS == 0 or gen == self.generations-1:
                print(f"Gen {gen:3d} | best fit = {best_fit}")
        
        if self.print_generations:
            print(f"Gen {gen:3d} | best fit = {best_fit}")

        return best_fit, best_chrom