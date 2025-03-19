# Utworzyć ramkę danych, pokazującą ile leków zostało zatwierdzonych, wycofanych, ile
# jest w fazie eksperymentalnej (ang. *experimental* lub *investigational*) i dopuszczonych w
# leczeniu zwierząt. Przedstawić te dane na wykresie kołowym. Podać liczbę zatwierdzonych
# leków, które nie zostały wycofane.
import pandas as pd
from matplotlib import pyplot as plt

from utils import get_drugs, get_id, get_groups

# Zwraca ramkę
def solution_9a(data=None):
    data_set = set()

    drugs = get_drugs(data)
    for drug in drugs:
        for group in get_groups(drug):      # Zakładam że zawsze jakieś grupy istnieją
            data_set.add((get_id(drug), group))

    return pd.DataFrame(data_set, columns=['Id', 'State'])


# Generuje podstawowy wykres kołowy dla podpunktu 9
def default_graph_09(proc, labels, save_path=None, show=True):
    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, _, _ = ax.pie(
        proc, autopct='%1.1f%%', textprops={'fontsize': 10}, pctdistance=1.1
    )

    plt.legend(wedges, labels, title="Drug states",
               bbox_to_anchor=(0.9, 1), loc="upper left", fontsize=8)
    plt.subplots_adjust(right=0.75)
    plt.tight_layout()

    if show:
        plt.show()
    if save_path is not None:
        plt.savefig(save_path)

    plt.close()


# Generuje wykres, który pokazuje ile procent targetów zawiera w swoich grupach podaną
def gen_singular_graph(displayed_state, data=None, save_path=None, show=True):
    count = 0
    drug_sum = 0
    for drug in get_drugs(data):
        if displayed_state in get_groups(drug):
            count += 1
        drug_sum += 1

    text = displayed_state.capitalize().replace('_', ' ')
    labels = [text, 'Not ' + text]
    proc = [count, drug_sum - count]

    default_graph_09(proc, labels, save_path, show)


# Zlicza dla każdej grupy, w ilu targetach się pojawia
# Następnie generuje wykres pokazujący stosunek owych liczebności
def gen_simplified_graph(data=None, save_path=None, show=True):
    txt = {
        'approved': 0,
        'experimental': 0,
        'investigational': 0,
        'vet_approved': 0,
        'withdrawn': 0
    }

    for drug in get_drugs(data):
        for key in txt.keys():
            if key in get_groups(drug):
                txt[key] = txt[key] + 1

    labels = []
    proc = []
    for key in txt.keys():
        labels.append(key.capitalize().replace('_', ' '))
        proc.append(txt[key])

    default_graph_09(proc, labels, save_path, show)

# Generuje najsensowniejszy wykres
# Pokazuje w ilu procentach targetów pojawia się każda z występujących kombinacji
def gen_detailed_graph(data=None, save_path=None, show=True):
    # Dla każdego możliwego stanu przypisujemy jeden z pięciu bitów
    txt_to_id = {
        'approved': 1,
        'experimental': 2,
        'investigational': 4,
        'vet_approved': 8,
        'withdrawn': 16
    }
    id_to_txt = {
        1: 'Approved',
        2: 'Experimental',
        4: 'Investigational',
        8: 'Vet approved',
        16: 'Withdrawn'
    }

    # Wyliczamy wszystkie możliwe kombinacje stanów
    # i tworzymy nazwę dla każdego z nich - połączenie nazw stanów
    combinations = {}
    for i in range(1, 32):
        text = ""
        for k in range(0, 5):
            if 2 ** k & i != 0:
                text += id_to_txt[2 ** k] + " "
        combinations[i] = text

    # Liczymy wystąpienie każdego stanu
    count = [0] * 32

    for drug in get_drugs(data):
        i = 0
        for group in get_groups(drug):
            i += txt_to_id[group]
        count[i] += 1

    # Generujemy wykres
    proc = []
    labels = []
    for i in range(1, 32):
        if count[i] != 0:
            proc.append(count[i])
            labels.append(combinations[i])

    default_graph_09(proc, labels, save_path, show)


# Generuje graf
def solution_9b(data=None, save_path=None, show=True, show_one = None, simplified = False):
    assert show_one in [None, 'approved', 'experimental', 'investigational', 'vet_approved', 'withdrawn'], "Wrong state"
    assert show_one is None or simplified is False, "'show_one' shouldn't be set when 'simplified' is True"

    if show_one is not None:
        gen_singular_graph(show_one, data, save_path, show)
    elif simplified:
        gen_simplified_graph(data, save_path, show)
    else:
        gen_detailed_graph(data, save_path, show)


def solution_9(data=None, save_path=None, show=True, show_one = None, simplified = False):
    solution_9b(data, save_path, show, show_one, simplified)
    return solution_9a(data)