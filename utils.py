import pandas as pd
import xmltodict

# Biblioteka z podstawowymi funkcjami


DEFAULT_FILENAME = "drugbank_partial.xml"

# Dla spamiętywania danych w obrębie uruchomienia programu
dicts = {}

# Zwraca słownik będący odpowiednikiem pliku xml
def get_dict_from_xml(xml_file = DEFAULT_FILENAME):
    if str(xml_file) not in dicts.keys():
        with open(xml_file, 'r', encoding='utf-8') as file:
            dicts[str(xml_file)] = xmltodict.parse(file.read())
    return dicts[str(xml_file)]

# Dla słownika z danymi/ścieżki do pliku zawierającego dane zwraca listę wszystkich leków
def get_drugs(source=None):
    if source is None:
        return get_dict_from_xml()['drugbank']['drug']
    elif isinstance(source, dict):
        return source['drugbank']['drug']
    else:
        return get_dict_from_xml(source)['drugbank']['drug']

def normalize_to_list(data):
    if isinstance(data, list):
        return data
    return [data]

def get_id(drug):
    return drug['drugbank-id'][0]['#text']
def get_name(drug):
    return drug['name']
# Dla podanego atrybutu zwraca listę wszystkich takowych dla danego leku lub None
# Np. dla atrybutu 'product' zwraca listę wszystkich produktów
def get_list_of_atr(drug, atr):
    if (atr+'s') not in drug.keys():
        return None
    if drug[atr+'s'] is None:
        return None
    return normalize_to_list(drug[atr + 's'][atr])

# Funkcje dla standardowych atrybutów
def get_food_interactions(drug):
    return get_list_of_atr(drug, 'food-interaction')
def get_synonyms(drug):
    return get_list_of_atr(drug, 'synonym')
def get_products(drug):
    return get_list_of_atr(drug, 'product')
def get_pathways(drug):
    return get_list_of_atr(drug, 'pathway')
def get_path_drugs(pathway):
    return get_list_of_atr(pathway, 'drug')
def get_targets(drug):
    return get_list_of_atr(drug, 'target')
def get_ext_ids(polypeptide):
    return get_list_of_atr(polypeptide, 'external-identifier')
def get_groups(drug):
    return get_list_of_atr(drug, 'group')
def get_drug_interactions(drug):
    return get_list_of_atr(drug, 'drug-interaction')

# Wspomagająca klasa tworząca ramkę zbierając dane do słownika
class DfMaker:
    _dict = {}
    columns = []

    # W konstruktorze należy zdefiniować nazwy kolumn
    def __init__(self, columns):
        self.columns = columns
        for column in self.columns:
            self._dict[column] = []

    # Dodawanie wiersza odbywa się poprzez podanie listy
    def add_row(self, row):
        assert(len(row) == len(self.columns))
        for i in range(0, len(self.columns)):
            self._dict[self.columns[i]].append(row[i])

    def make(self):
        return pd.DataFrame(self._dict, columns=self.columns)