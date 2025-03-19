# Stworzyć symulator, który generuje testową bazę 20000 leków. Wartości generowanych
# 19900 leków w kolumnie “DrugBank Id” powinny mieć kolejne numery, a w pozostałych
# kolumnach wartości wylosowane spośród wartości istniejących 100 leków. Zapisz wyniki w
# pliku drugbank_partial_and_generated.xml. Przeprowadź analizę według punktów 1-12
# testowej bazy
import random
import xmltodict

from utils import get_drugs, get_dict_from_xml, get_id

# Ponieważ baza 20000 leków generuje się bardzo długo i zajmuje dużo przestrzeni na dysku,
# wygenerowałem bazę 5000 leków
# Analiza wg pkt. 1-12 jest możliwa w main.py
# korzysta z bieżąco generowanej bazy 20000 leków przechowywanej w pamięci podręcznej


# Tworzy prosty szkielet bazy danych (wszystko poza lekami)
def gen_skeleton(original_dict):
    result = {'drugbank': {}}

    for key in original_dict:
        if key != 'drugbank':
            result[key] = original_dict[key]

    for key in original_dict['drugbank'].keys():
        if key != 'drug':
            result['drugbank'][key] = original_dict['drugbank'][key]

    result['drugbank']['drug'] = []
    return result


# Generuje id leku w odpowiedniej postaci dla danego numeru id
def gen_drugbank_id(num):
    assert num >= 0, 'Id must be positive'
    assert num < 100000, "Id too big (>=100000)"
    _id = str(num)
    _id = '0' * (5 - len(_id)) + _id
    db_id = 'DB' + _id
    btd_id = 'GBTD' + _id   # 'generated BTD
    biod_id = 'GBIOD' + _id # 'generated BIOD
    return [{'@primary': 'true', '#text': db_id}, btd_id, biod_id]


# Zwraca:
#   możliwe atrybuty leków (attr)
#       np. products[...]
#   możliwe zestawy owych atrybutów (attr_types)
#       np. [state, groups, products, ...]
#       (nie wszystkie leki mają te same kombinacje atrybutów)
def get_value_pool(original_dict):
    res_attrs = {}
    attr_types = []

    for drug in original_dict['drugbank']['drug']:
        attributes = drug.keys()
        cur_attr = []

        # Wyznaczenie zestawu atrybutów (i samych możliwych atrybutów)
        for attr in attributes:
            if attr not in res_attrs:
                res_attrs[attr] = []
            res_attrs[attr].append((drug[attr]))

            cur_attr.append(attr)
        cur_attr = tuple(cur_attr)
        attr_types.append(cur_attr)
    return res_attrs, attr_types


# Generuje lek w oparciu na możliwe atrybuty i ich zestawy
def generate_drug(attrs, attr_types, i):
    # Losowanie zestawu atrybutów
    attr_set = attr_types[random.randint(0, len(attr_types) - 1)]
    drug = {}

    # Dla każdego atrybutu z zestawu losowanie jego wartości
    for attr in attr_set:
        if attr == 'drugbank-id':
            drug[attr] = gen_drugbank_id(i)
        else:
            drug[attr] = random.choice(attrs[attr])
    return drug


# Wyznacza liczbowe id z domyślnego
def strip_id(drug_id):
    return int(drug_id[2:7])
# Wyznacza maksymalne id wśród leków
def get_max_id(drugs):
    _max = 0
    for drug in drugs:
        _max = max(_max, strip_id(get_id(drug)))
    return _max


# Generuje bazę danych z możliwością zapisu
def generate_dict(original_xml = None, imported=100, target_size=20000, save=None):
    if original_xml is None:
        original_xml = get_dict_from_xml()

    new_dict = gen_skeleton(original_xml)

    attr, attr_types = get_value_pool(original_xml)

    # Przeniesienie leków z bazy
    for i in range(0, imported):
        new_dict['drugbank']['drug'].append(original_xml['drugbank']['drug'][i])

    # Niektóre id są w bazie pominięte
    # Zatem, mimo że w domyślnej bazie jest 100 leków, istnieje już lek z id > 100
    # Wystarczy więc kolejne id generować od (max_id + 1)
    max_id = get_max_id(get_drugs(new_dict))
    # Generacja nowych leków
    for i in range (max_id + 1, max_id + 1 + target_size - imported):
        new_dict['drugbank']['drug'].append(generate_drug(attr, attr_types, i))

    if save is not None:
        xml = xmltodict.unparse(new_dict, pretty=True)
        with open(save, 'w', encoding='utf-8') as f:
            f.write(xml)

    return new_dict