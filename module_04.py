# Utworzyć ramkę danych zawierającą informacje o wszystkich szlakach (sygnałowych,
# metabolicznych) z jakimi jakikolwiek lek wchodzi w interakcje. Podać całkowitą liczbę tych
# szlaków.
import pandas as pd

from utils import get_drugs, get_pathways


def solution_4(data=None):
    # Żeby ścieżki nie powtarzały się, trzymane są w secie
    path_set = set()

    drugs = get_drugs(data)
    for drug in drugs:
        pathways = get_pathways(drug)
        if pathways is None:
            continue
        for pathway in pathways:
            path_set.add((pathway['smpdb-id'], pathway['name'], pathway['category']))

    return pd.DataFrame(path_set, columns=['Smpdb id', 'Name', 'Category'])