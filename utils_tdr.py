def adjacency_list_is_valid_trdf(adjacency, f_list):
    n = len(adjacency)

    for v in range(n):
        # F(v) = 2 ou F(v) = 1
        if f_list[v] == 2 or f_list[v] == 1:
            possui_vizinho_apoio = False
            for u in adjacency[v]:
                if (f_list[u] >= 1):
                    possui_vizinho_apoio = True
            if not possui_vizinho_apoio:
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
                print(f'v = {v} => F(v) = {f_list[v]} => vizinhos(v) = {[f_list[k] for k in adjacency[v]]}')
                return False

    return True