# Utworzyć wykres kołowy prezentujący procentowe występowanie targetów w różnych
# częściach komórki.
from matplotlib import pyplot as plt

from utils import get_drugs, normalize_to_list, get_targets


# Zwraca słownik lokalizacja - zbiór targetów
def get_all_targets(data=None):
    sets_dict = {}

    for drug in get_drugs(data):
        targets = get_targets(drug)
        if targets is None:
            continue
        for target in targets:
            if 'polypeptide' not in target.keys():          # Niektóre targety nie są białkami
                continue
            for polypeptide in normalize_to_list(target['polypeptide']):
                loc = polypeptide['cellular-location']
                if loc not in sets_dict.keys():
                    sets_dict[loc] = set()
                sets_dict[loc].add(polypeptide['@id'])
    return sets_dict


def solution_8(data=None, save_path=None, show=True):
    labels = []
    count = []

    # Zliczanie dla każdej lokalizacji jej popularności
    targets = get_all_targets(data)
    for loc in targets.keys():
        if loc is not None:
            labels.append(loc)
        else:
            labels.append('Not specified')      # Dla lepszej czytelności
        count.append(len(targets[loc]))

    # Generacja pożądanego wykresu
    fig, ax = plt.subplots(figsize=(10, 6))
    wedges, _, _ = ax.pie(
        count, autopct='%1.1f%%', textprops={'fontsize': 9}, pctdistance=1.1
    )

    plt.legend(wedges, labels, title="Cellular Location",
               bbox_to_anchor=(0.9, 1.1), loc="upper left",
               fontsize=8, title_fontsize=15)
    plt.subplots_adjust(right=0.75)
    plt.tight_layout()

    if show:
        plt.show()
    if save_path is not None:
        plt.savefig(save_path)

    plt.close()