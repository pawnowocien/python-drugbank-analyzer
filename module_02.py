# Utworzyć ramkę danych pozwalającą na wyszukiwanie po DrugBank ID informacji o
# wszystkich synonimach pod jakimi dany lek występuje. Napisać funkcję, która dla podanego
# DrugBank ID utworzy i wyrysuje graf synonimów za pomocą biblioteki NetworkX. Należy
# zadbać o czytelność generowanego rysunku.
from default_display import COLOR_BACKGROUND, get_default_colors, COLOR_DEFAULT, COLOR_EDGE
from utils import get_drugs, get_id, get_synonyms
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


# Zwraca ramkę leków i ich synonimów
def get_all_drugs_synonyms(data=None):
    syn_dict = {
        'Drug': [],
        'Synonym': []
    }
    for drug in get_drugs(data):
        synonyms = get_synonyms(drug)
        if synonyms is None:
            continue
        for syn in synonyms:
            syn_dict['Drug'].append(get_id(drug))
            syn_dict['Synonym'].append(syn['#text'])
    return pd.DataFrame(syn_dict)


# Generuje pożądany graf
def gen_syn_graph(drug_id, data=None, save_path=None, show=True):
    graph = nx.Graph()

    synonyms = list()

    # W zależności od formy danych synonimy są zbierane w różny sposób
    if isinstance(data, pd.DataFrame):
        synonyms = list(data.loc[data['Drug'] == drug_id, 'Synonym'])
    else:
        drug_dict = get_drugs(data)
        for drug in drug_dict:
            if get_id(drug) == drug_id:
                tmp = get_synonyms(drug)
                synonyms = []
                if tmp is None:
                    break
                for syn in tmp:
                    synonyms.append(syn['#text'])
                break

    # Definiowanie powiązań w grafie
    drug_node = drug_id
    graph.add_node(drug_node, category='drug')
    if synonyms is None:
        return
    for syn in synonyms:
        syn_node = syn.replace(' ', '\n')       # potrzebne do lepszego wyświetlania się długich nazw
        if drug_node != syn_node:
            graph.add_node(syn_node, category='synonym')
            graph.add_edge(drug_node, syn_node)

    # Generacja grafu:
    fig, ax = plt.subplots(figsize=(12, 8))
    pos = nx.spring_layout(graph)

    color_dict = get_default_colors(['drug', 'synonym'])
    node_colors = [color_dict.get(graph.nodes[n].get("category", COLOR_DEFAULT)) for n in graph.nodes]

    node_sizes = []
    for node in graph.nodes:
        if graph.nodes[node].get('category') == 'drug':  # Larger size for the gene node
            node_sizes.append(2000)
        else:
            node_sizes.append(1300)

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_size=node_sizes,
        node_color=node_colors,
        edge_color=COLOR_EDGE,
        edgecolors=COLOR_EDGE,
        width=1,
        font_size="10",
        font_weight="bold"
    )
    fig.patch.set_facecolor(COLOR_BACKGROUND)
    if show:
        plt.show()
    if save_path is not None:
        plt.savefig(save_path)
    plt.close()


def solution_2(drug_id, data=None, save_path=None, show=True):
    df = get_all_drugs_synonyms(data)
    gen_syn_graph(drug_id, df, save_path, show)
    return df