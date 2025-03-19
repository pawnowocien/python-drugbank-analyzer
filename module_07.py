# Utworzyć ramkę danych zawierającą informacje o białkach, z którymi poszczególne leki
# wchodzą w interakcje. Białka te to tzw. targety. Ramka danych powinna zawierać
# przynajmniej DrugBank ID targetu, informację o zewnętrznej bazie danych (ang. *source*,
# np. Swiss-Prot), identyfikator w zewnętrznej bazie danych, nazwę polipeptydu, nazwę genu
# kodującego polipeptyd, identyfikator genu GenAtlas ID, numer chromosomu, umiejscowienie
# w komórce.
import pandas as pd

from utils import get_drugs, normalize_to_list, get_targets, get_ext_ids


def solution_7(data=None):
    # Aby informacje nie powtarzały się, składowane są w secie
    targ_set = set()
    columns = ['Target id',
        'Source',
        'Foreign Id',
        'Polypeptide name',
        'Gene name',
        'Gene GenAtlas id',
        'Chromosome Location',
        'Cellular location']

    for drug in get_drugs(data):
        # Uwaga, dla przykładu DB00027 nie ma targetów w bazie,
        # choć na stronie wyświetla się takowy
        targets = get_targets(drug)
        if targets is None:
            continue

        for target in targets:
            if 'polypeptide' not in target.keys():  # Niektóre targety nie są białkami
                continue
            for polypeptide in normalize_to_list(target['polypeptide']):
                gen_atlas_id = None

                ext_ids = get_ext_ids(polypeptide)
                if ext_ids is not None:
                    for ext_id in ext_ids:
                        if ext_id['resource'] == 'GenAtlas':
                            gen_atlas_id = ext_id['identifier']
                            break

                targ_set.add((target['id'],
                              polypeptide['@source'],
                              polypeptide['@id'],
                              polypeptide['name'],
                              polypeptide['gene-name'],
                              gen_atlas_id,                 # Dopuszczam wartość None
                              polypeptide['chromosome-location'],
                              polypeptide['cellular-location']))
    return pd.DataFrame(targ_set, columns=columns)