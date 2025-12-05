from dataset_reader import *
from brkga import BRKGA
from ga import GA
import guloso_brkga
import literatura_ga
from utils_tdr import adjacency_list_is_valid_trdf

import time

def run_algoritmo_genetico(grafo, metodo):
    print()
    print(f"Database: {name}")

    n = len(grafo)

    print(f"Metodo utilizado: {metodo}")

    if metodo == "guloso_brkga":
        ag = BRKGA(
            n = n,
            pop_size=400, 
            elite_frac=0.2, 
            mutant_frac=0.2, 
            generations=1000,
            max_gens_without_improvement=300,
            max_optimal_solution=3,
            print_generations=False
        )
        ag.fitness = guloso_brkga.fitness_guloso(grafo)
    elif metodo == "literatura_ga":
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
        ag.generate_population = literatura_ga.generate_population_graph(grafo)
        ag.repair = literatura_ga.repair_graph(grafo)
    else:
        print(f'Método não reconhecido: {metodo}')
        exit(1)

    t0 = time.time()
    w, sol = ag.run()
    t1 = time.time()

    if metodo == "guloso_brkga":
        sol = guloso_brkga.decode(grafo, sol)

    print(f"γtR = {w}")
    print(f'Tempo de processamento: {t1-t0} segundos')

    if not adjacency_list_is_valid_trdf(grafo, sol, print_debug=True):
        print("solucao invalida")
        print(sol)
        return {
            'fit': -1,
            'solucao': -1, 
            'time': t1-t0
        }

    return {
        'fit': int(w),
        'solucao': sol, 
        'time': t1-t0
    }

if __name__ == "__main__":

    graphs = listar_arquivos_diretorio("grafos")

    # metodos = ["literatura_ga", "guloso_brkga"]
    # metodos = ["literatura_ga"]
    metodos = ["guloso_brkga"]

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