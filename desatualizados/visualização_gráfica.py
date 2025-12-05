import networkx as nx
import matplotlib.pyplot as plt

# Função para desenhar grafo com TRDF
def plot_trdf(G, trdf_sol, title="Grafo TRDF"):
    """
    G: grafo NetworkX
    trdf_sol: dicionário {vértice: valor TRDF (0,1,2)}
    """
    pos = nx.spring_layout(G, seed=42)  # layout consistente
    colors = []
    labels = {}
    
    for node in G.nodes():
        val = trdf_sol[node]
        labels[node] = str(val)
        if val == 0:
            colors.append('lightgray')
        elif val == 1:
            colors.append('skyblue')
        else:  # val == 2
            colors.append('orange')
    
    plt.figure(figsize=(5,5))
    nx.draw(G, pos, with_labels=True, labels=labels, node_color=colors, node_size=800, font_size=14)
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    # Grafos de exemplo
    graphs = {
        "C5": nx.cycle_graph(5),
        "P5": nx.path_graph(5),
        "K4": nx.complete_graph(4),
        "Star": nx.star_graph(4)
    }

    # Soluções exatas da TRDF
    trdf_solutions = {
        "C5": {0:0, 1:0, 2:2, 3:0, 4:2},
        "P5": {0:0, 1:2, 2:0, 3:0, 4:2},
        "K4": {0:0, 1:0, 2:0, 3:2},
        "Star": {0:2, 1:0, 2:0, 3:0, 4:0}
    }

    # Plotando todos
    for name, G in graphs.items():
        plot_trdf(G, trdf_solutions[name], title=f"{name} - TRDF ótimo")
