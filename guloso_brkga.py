from utils_tdr import adjacency_list_is_valid_trdf

def decode_old(adjacencias, chrom):
    ordem = sorted(range(len(adjacencias)), key=lambda x: chrom[x])

    rotulos = [None for _ in adjacencias]

    for i in ordem:
        if rotulos[i] is not None: continue

        rotulos[i] = 2
        vizinhos = adjacencias[i]
        vizinhos_ordenados = sorted(vizinhos, key=lambda x: ordem[x])

        rotulos[vizinhos_ordenados[0]] = 2

        vizinhos2 = adjacencias[vizinhos_ordenados[0]]
        vizinho_marcado = False
        for vizinho2 in vizinhos2:
            if rotulos[vizinho2] is None:
                rotulos[vizinho2] = 0
                vizinho_marcado = True
        
        if not vizinho_marcado:
            rotulos[vizinhos_ordenados[0]] = 1

        vizinho_marcado = False
        for vizinho in vizinhos_ordenados[1:]:
            if rotulos[vizinho] is None:
                rotulos[vizinho] = 0
                vizinho_marcado = True
        
        if not vizinho_marcado:
            rotulos[i] = 1
    
    return rotulos

def decode(adjacencias, chrom):
    ordem = sorted(range(len(adjacencias)), key=lambda x: chrom[x])

    rotulos = [0 for _ in chrom]

    for i in range(len(chrom)):
        rotulos[ordem[i]] = 2
        if adjacency_list_is_valid_trdf(adjacencias, rotulos):
            break
    
    for j in range(i,-1,-1):
        rotulos[ordem[j]] = 1
        if not adjacency_list_is_valid_trdf(adjacencias, rotulos):
            rotulos[ordem[j]] = 2
            break
    
    return rotulos

def decode_ordem(adjacencias, ordem):
    rotulos = [0 for _ in ordem]

    for i in range(len(ordem)):
        rotulos[ordem[i]] = 2
        if adjacency_list_is_valid_trdf(adjacencias, rotulos):
            break
    
    for j in range(i,-1,-1):
        rotulos[ordem[j]] = 1
        if not adjacency_list_is_valid_trdf(adjacencias, rotulos):
            rotulos[ordem[j]] = 2
            break
    
    return rotulos

def fitness_guloso(adjacencias):
    def guloso(chrom):
        return sum(decode(adjacencias, chrom))
    
    return guloso
