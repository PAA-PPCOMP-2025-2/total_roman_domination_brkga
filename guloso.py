import time

from dataset_reader import leitura_matriz_adjacencia
from brkga import BRKGA

def fitness_guloso(adjacencias):
    def guloso(chrom):
        ordem = sorted(range(n), key=lambda x: chrom[x])

        rotulos = [None for _ in adjacencias]

        for i in ordem:
            if rotulos[i] is not None: continue

            rotulos[i] = 2
            vizinhos = adjacencias[i]
            vizinhos_ordenados = sorted(vizinhos, key=lambda x: ordem[x])

            rotulos[vizinhos_ordenados[0]] = 1

            for vizinho in vizinhos_ordenados[1:]:
                rotulos[vizinho] = 0

        return sum(rotulos)
    
    return guloso

if __name__ == "__main__":
    graphs = {
        "MANN-a81": leitura_matriz_adjacencia("datasets/DIMACS/MANN-a81.mtx"),            # melhor: 5
        # "C1000-9": leitura_matriz_adjacencia("datasets/DIMACS/C1000-9.mtx"),              # melhor: 5
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

        ag.fitness = fitness_guloso(graph)

        t0 = time.time()
        w, sol = ag.run()
        t1 = time.time()
        print(f'Tempo de processamento: {t1-t0} segundos')

        print(f"{name}: γtR = {w}")

        ordem = sorted(range(n), key=lambda x: sol[x])

        # print(guloso(graph, ordem))