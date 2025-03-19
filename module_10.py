# Utworzyć ramkę danych zawierającą informacje dotyczące potencjalnych interakcji
# danego leku z innymi lekami.
from utils import get_drugs, get_id, get_drug_interactions, DfMaker


def solution_10(data=None):
    # Żeby pary nie powtarzały się są trzymane w secie
    interactions_set = set()

    for drug in get_drugs(data):
        drug_interactions = get_drug_interactions(drug)
        if drug_interactions is None:
            continue
        for interaction in drug_interactions:
            id_1 = get_id(drug)
            id_2 = interaction['drugbank-id']
            desc = interaction['description']

            # Przeciwdziałanie pojawieniu się par (a, b, desc) i (b, a, desc)
            if id_1 < id_2:
                row = (id_1, id_2, desc)
            else:
                row = (id_2, id_1, desc)

            interactions_set.add(row)

    columns = ['Id 1',
               'Id 2',
               'Description']
    dfm = DfMaker(columns)

    for row in interactions_set:
        dfm.add_row(row)
    return dfm.make()
