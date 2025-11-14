from dataset_reader import *
from brkga import BRKGA
from ga import GA
import guloso_brkga
import artigo_brkga
import artigo_ga
from utils_tdr import adjacency_list_is_valid_trdf

import time

def run_algoritmo_genetico(grafo, metodo):
    print()
    print(f"Database: {name}")

    n = len(grafo)

    print(f"Metodo utilizado: {metodo}")

    if metodo == "artigo_brkga":
        ag = BRKGA(
            n = n,
            pop_size=50, 
            elite_frac=0.2, 
            mutant_frac=0.5, 
            generations=1000,
            max_gens_without_improvement=100,
            max_optimal_solution=3,
            print_generations=False
        )
        ag.fitness = artigo_brkga.fitness
        ag.generate_population = artigo_brkga.generate_population_graph(grafo)
        ag.repair = artigo_brkga.repair_graph(grafo)
    elif metodo == "guloso_brkga":
        ag = BRKGA(
            n = n,
            pop_size=50, 
            elite_frac=0.2, 
            mutant_frac=0.5, 
            generations=1000,
            max_gens_without_improvement=100,
            max_optimal_solution=3,
            print_generations=False
        )
        ag.fitness = guloso_brkga.fitness_guloso(grafo)
    elif metodo == "artigo_ga":
        ag = GA(
            n = n,
            pop_size=50, 
            elite_frac=0.2262, 
            taxa_mutacao=0.057,
            tam_torneio=6, 
            generations=586,
            max_gens_without_improvement=363,
            max_optimal_solution=3,
            print_generations=False
        )
        ag.generate_population = artigo_ga.generate_population_graph(grafo)
        ag.repair = artigo_ga.repair_graph(grafo)
    else:
        print(f'Método não reconhecido: {metodo}')
        exit(1)

    t0 = time.time()
    w, sol = ag.run()
    t1 = time.time()

    print(f"γtR = {w}")
    print(f'Tempo de processamento: {t1-t0} segundos')

    if not adjacency_list_is_valid_trdf(grafo, sol):
        print("solucao invalida")
        print(sol)
        exit(1)

    return {
        'fit': int(w),
        'solucao': sol, 
        'time': t1-t0
    }

if __name__ == "__main__":

    graphs = listar_arquivos_diretorio("datasets/random")

    # metodos = ["artigo_ga"]
    metodos = ["artigo_ga", "artigo_brkga", "guloso_brkga"]
    # metodos = ["artigo_brkga", "guloso_brkga"]

    texto_export = ""

    linha_export = "grafo"

    for metodo in metodos:
        linha_export += f",{metodo}_fit"
    for metodo in metodos:
        linha_export += f",{metodo}_tempo"

    texto_export += linha_export + '\n'

    for name, graph in graphs.items():

        resultados_metodos = [run_algoritmo_genetico(graph, metodo) for metodo in metodos]

        linha_export = f"{name}"
        for resultados in resultados_metodos:
            linha_export += f",{resultados['fit']}"
        for resultados in resultados_metodos:
            linha_export += f",{resultados['time']}"

        texto_export += linha_export + '\n'

        # break
    
    with open('output.csv', 'w') as output_file:
        output_file.write(texto_export)