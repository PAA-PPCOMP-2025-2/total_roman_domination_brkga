def adjacency_list_is_valid_trdf(adjacency, f_list, print_debug=False):
    n = len(adjacency)

    for v in range(n):
        # F(v) = 2 ou F(v) = 1
        if f_list[v] == 2 or f_list[v] == 1:
            possui_vizinho_apoio = False
            for u in adjacency[v]:
                if (f_list[u] >= 1):
                    possui_vizinho_apoio = True
            if not possui_vizinho_apoio:
                if print_debug:
                    print(f'v = {v} => F(v) = {f_list[v]} => vizinhos(v) = {[f_list[k] for k in adjacency[v]]}')
                return False

        # F(v) = 0
        if f_list[v] == 0:
            possui_vizinho_apoio = False
            for u in adjacency[v]:
                try:
                    if f_list[u] == 2:
                        possui_vizinho_apoio = True
                except:
                    print(u)
                    print(len(adjacency))
                    print(len(f_list))
                    print(f_list)
                    exit(1)
            if not possui_vizinho_apoio:
                if print_debug:
                    print(f'v = {v} => F(v) = {f_list[v]} => vizinhos(v) = {[f_list[k] for k in adjacency[v]]}')
                return False

    return True

def adjacency_list_is_valid_trdf_optim(adjacency, f_list, print_debug=False):
    n = len(adjacency)

    checados = [False for _ in adjacency]

    for v in range(n):
        if checados[v]: continue

        # F(v) = 2
        if f_list[v] == 2:
            checados[v] = True
            possui_vizinho_apoio = False
            for u in adjacency[v]:
                checados[u] = True
                if (f_list[u] >= 1):
                    possui_vizinho_apoio = True
            if not possui_vizinho_apoio:
                if print_debug:
                    print(f'v = {v} => F(v) = {f_list[v]} => vizinhos(v) = {[f_list[k] for k in adjacency[v]]}')
                return False
            
        # F(v) = 1
        elif f_list[v] == 1:
            checados[v] = True
            possui_vizinho_apoio = False
            for u in adjacency[v]:
                if (f_list[u] >= 1):
                    possui_vizinho_apoio = True
                    checados[u] = True
            if not possui_vizinho_apoio:
                if print_debug:
                    print(f'v = {v} => F(v) = {f_list[v]} => vizinhos(v) = {[f_list[k] for k in adjacency[v]]}')
                return False

        # F(v) = 0
        else:
            checados[v] = True
            possui_vizinho_apoio = False
            for u in adjacency[v]:
                try:
                    if f_list[u] == 2:
                        possui_vizinho_apoio = True
                        break
                except:
                    print(u)
                    print(len(adjacency))
                    print(len(f_list))
                    print(f_list)
                    exit(1)
            if not possui_vizinho_apoio:
                if print_debug:
                    print(f'v = {v} => F(v) = {f_list[v]} => vizinhos(v) = {[f_list[k] for k in adjacency[v]]}')
                return False
    
    # if adjacency_list_is_valid_trdf(adjacency, f_list) != (not False in checados):
    #     print(adjacency_list_is_valid_trdf(adjacency, f_list))
    #     print(not False in checados)
    #     print(f_list)
    #     print([1 if c else 0 for c in checados])
    #     print(checados[checados.index(0)])
    #     print(adjacency[checados.index(0)])
    #     print(adjacency[11])
    #     exit(1)

    if False in checados:
        return False
    else:
        return True