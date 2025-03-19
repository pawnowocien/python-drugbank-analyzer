# Dla każdego szlaku sygnałowego/metabolicznego w bazie danych podać leki, które
# wchodzą z nim w interakcje. Wyniki należy przedstawić w postaci ramki danych jak i w
# opracowanej przez siebie formie graficznej. Przykładem takiej grafiki może być graf
# dwudzielny, gdzie dwa rodzaje wierzchołków to szlaki sygnałowe i leki, a poszczególne
# krawędzie reprezentują interakcję danego leku z danym szlakiem sygnałowym. Należy
# zadbać o czytelność i atrakcyjność prezentacji graficznej. (4 pkt)
import pandas as pd
import matplotlib.colors as mcolors
import networkx as nx
import matplotlib.pyplot as plt

from default_display import COLOR_BETWEEN, COLOR_BACKGROUND
from utils import get_drugs, get_pathways, get_path_drugs


# Zwraca ramkę lek - szlak
# Można określić, czy ścieżki powinny być w formie id, czy nazwy
def get_all_pathways(data=None, ids=False):
    path_set = set()
    drugs = get_drugs(data)

    for drug in drugs:
        pathways = get_pathways(drug)
        if pathways is None:
            continue

        for pathway in pathways:
            if ids:
                path_name = pathway['smpdb-id']
            else:
                path_name = pathway['name']

            path_drugs = get_path_drugs(pathway)
            if path_drugs is None:
                continue
            for pth_drug in path_drugs:
                path_set.add((path_name, pth_drug['drugbank-id']))

    return pd.DataFrame(path_set, columns=['Pathway', 'Drug'])


# Generuje graf dwudzielny na podstawie ramki
def gen_path_graph(df, save_path=None, show=True):
    df.sort_values(by=['Pathway', 'Drug'], ascending=False, inplace=True)

    graph = nx.Graph()
    # Generacja zależności pomiędzy wierzchołkami grafu
    for row in df.itertuples():
        graph.add_node(row[1], bipartite=0)
        graph.add_node(row[2], bipartite=1)
        graph.add_edge(row[1], row[2])

    # Sortowanie obu stron dla lekkiego zwięszkenia czytelności
    left_set = sorted({node for node, attr in graph.nodes(data=True) if attr["bipartite"] == 0})
    right_set = sorted(set(graph) - set(left_set))

    fig, ax = plt.subplots(figsize=(12, 8))

    # Ustawienie pozycji
    pos = {n: (1, i) for i, n in enumerate(left_set)}
    pos.update({n: (2, i) for i, n in enumerate(right_set)})

    # Zdefiniowanie kolorów dla krawędzi
    # Każde dwie krawędzie kończące się w tym samym leku mają te same kolory
    colors = list(mcolors.TABLEAU_COLORS.values())
    edge_colors = []
    right_to_color = {right_node: colors[i % len(colors)] for i, right_node in enumerate(right_set)}

    for edge in graph.edges():
        if edge[1] in right_to_color:
            edge_colors.append(right_to_color[edge[1]])
        elif edge[0] in right_to_color:
            edge_colors.append(right_to_color[edge[0]])

    # Odpowiednia generacja grafu
    nx.draw(
        graph,
        pos=pos,
        with_labels=True,
        node_size=500,
        node_color=COLOR_BETWEEN,
        font_size=7,
        edge_color=edge_colors,  # Set edge colors
        edgecolors='black',
        width=1.5,
        bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3")
    )

    plt.title("Pathway-drug Connections", fontsize=20) #TODO dobra nazwa?
    fig.patch.set_facecolor(COLOR_BACKGROUND)

    if show:
        plt.show()
    if save_path is not None:
        plt.savefig(save_path)

    plt.close()


def solution_5(data=None, save_path=None, show=True, ids = False):
    df = get_all_pathways(data, ids)
    gen_path_graph(df, save_path, show)
    return df