# Opracować według własnego pomysłu graficzną prezentację zawierającą informacje o
# konkretnym genie lub genach, substancjach leczniczych, które z tym genem/genami
# wchodzą w interakcje, oraz produktach farmaceutycznych, które zawierają daną substancję
# leczniczą. Wybór dotyczący tego, czy prezentacja graficzna jest realizowana dla
# konkretnego genu, czy wszystkich genów jednocześnie pozostawiamy Państwa decyzji.
# Przy dokonywaniu wyboru należy kierować się czytelnością i atrakcyjnością prezentacji
# graficznej.
from default_display import COLOR_BACKGROUND, COLOR_EDGE, get_default_colors
from utils import get_drugs, normalize_to_list, get_products, get_targets

import networkx as nx
import matplotlib.pyplot as plt

# Moim rozwiązaniem jest graf, który w centrum zawiera gen,
# następnie gen połączony jest w subst. leczniczych, z którymi wchodzi w interakcję,
# zaś te połączone są z produktami farmaceutycznymi, w których występują


# Wyznacza zbiór produktów farmaceutycznych dla danego leku
def get_brand_names(drug):
    _set = set()
    products = get_products(drug)
    if products is None:
        return _set
    for product in products:
        _set.add(product['name'])
    return _set

# Generuje graf
def solution_11(gene, data=None, save_path=None, show=True, display_text=True, small_nodes=False):
    graph = nx.Graph()

    # Główny wierzchołek grafu
    graph.add_node(gene, category='gene')

    # Wyznaczenie leków, które w targetach mają szukany gen
    for drug in get_drugs(data):
        targets = get_targets(drug)
        if targets is None:
            continue

        for target in targets:
            if 'polypeptide' not in target.keys():
                continue
            for polypeptide in normalize_to_list(target['polypeptide']):
                if polypeptide['gene-name'] == gene:
                    drug_name = drug['name'].replace(' ', '\n')     # Dla zwiększenia czytelności

                    # Konstrułowanie powiązania gen - lek
                    graph.add_node(drug_name, category='drug')
                    graph.add_edge(gene, drug_name)

                    for name in get_brand_names(drug):
                        name = name.replace(' ', '\n')              # Dla zwiększenia czytelności
                        if name == drug_name:       # Zdarza się, że produkt ma identyczną nazwę do subst. lecz.
                            name += "\n(brand name)"

                        # Konstrułowanie powiązań lek - produkty
                        graph.add_node(name, category='brand_name')
                        graph.add_edge(drug_name, name)

    # ---------- Projektowanie grafu ----------


    fig, ax = plt.subplots(figsize=(20, 15))

    fig.patch.set_facecolor(COLOR_BACKGROUND)
    ax.set_facecolor(COLOR_BACKGROUND)
    ax.set_axis_off()

    # Zdefiniowanie kolorów wierzchołków i krawędzi
    color_dict = get_default_colors(['gene', 'brand_name', 'drug'])
    node_colors = [color_dict.get(graph.nodes[n].get("category", "gray")) for n in graph.nodes]

    # Zdefiniowanie wielkości wierzchołków
    node_sizes = []
    for node in graph.nodes:
        if node == gene:
            if small_nodes:
                node_sizes.append(80)
            else:
                node_sizes.append(2000)
        elif graph.nodes[node].get('category') == 'drug':
            if small_nodes:
                node_sizes.append(40)
            else:
                node_sizes.append(1500)
        else:
            if small_nodes:
                node_sizes.append(10)
            else:
                node_sizes.append(900)

    # Zmiana wyglądu w zależności od opcji
    width = 1
    alpha = 1
    edge_color = COLOR_EDGE
    if small_nodes:
        width = 0.1
        alpha = 0.3
        edge_color = 'black'

    edgecolors = COLOR_EDGE
    if not display_text:
        edgecolors = 'black'

    # Generacja wierzchołków i krawędzi
    pos = nx.kamada_kawai_layout(graph)
    nx.draw_networkx_nodes(
        graph,
        pos,
        node_size=node_sizes,
        node_color=node_colors,
        edgecolors=edgecolors
    )
    nx.draw_networkx_edges(
        graph,
        pos,
        edge_color=edge_color,
        alpha=alpha,
        width=width
    )

    # Generacja ewentualnego tekstu
    if display_text:
        gene_label = {gene: gene}
        drug_labels = {n: n for n in graph.nodes if graph.nodes[n].get('category') == 'drug'}
        other_labels = {n: n for n in graph.nodes if graph.nodes[n].get('category') == 'brand_name'}
        nx.draw_networkx_labels(graph, pos, labels=other_labels, font_size=7)
        nx.draw_networkx_labels(graph, pos, labels=drug_labels,font_size=10, font_weight='bold')
        nx.draw_networkx_labels(graph, pos, labels=gene_label, font_size=14, font_weight='bold')

    plt.title(f"Gene-Drug-Brand Mapping ({gene})", fontsize=40)
    if show:
        plt.show()
    if save_path is not None:
        plt.savefig(save_path)

    plt.close()