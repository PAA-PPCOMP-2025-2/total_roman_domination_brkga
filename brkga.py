import random
from typing import List

STEP_GENS = 10

class BRKGA:
    def __init__(self, n, pop_size, elite_frac, mutant_frac, generations, max_gens_without_improvement=100, optimal_solution=None):
        self.n = n
        self.pop_size = pop_size
        self.elite_size = int(pop_size * elite_frac)
        self.mutant_size = int(pop_size * mutant_frac)
        self.generations = generations
        self.max_gens_without_improvement = max_gens_without_improvement
        self.optimal_solution = optimal_solution

    # def decode(self, chrom):
    #     return chrom

    # def code(self, chrom):
    #     return chrom

    def repair(self, chrom: List[float]) -> List[float]:
        return chrom

    def fitness(self, chrom: List[float]) -> float:
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
            while len(new_pop) < self.pop_size - self.mutant_size:
                p1 = random.choice(elites)
                p2 = random.choice(pop)
                child = [p1[i] if random.random() < 0.7 else p2[i] for i in range(self.n)]
                child = self.repair(child)
                new_pop.append(child)
            
            # Mutantes
            new_pop.extend(self.generate_population(self.mutant_size))

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

            if best_fit == self.optimal_solution:
                print("Solução ótima encontrada!")
                break

            if gen % STEP_GENS == 0 or gen == self.generations-1:
                print(f"Gen {gen:3d} | best fit = {best_fit}")
        
        print(f"Gen {gen:3d} | best fit = {best_fit}")

        return best_fit, best_chrom

if __name__ == "__main__":
    brkga = BRKGA(
        n=10,
        pop_size=100,
        elite_frac=0.2,
        mutant_frac=0.2,
        generations=10000,
        optimal_solution=0.0
    )

    best_fit, best_chrom = brkga.run()
    print("Best fitness:", best_fit)
    print("Best chromosome:", best_chrom)