# Utworzyć ramkę danych, która dla każdego leku zawiera następujące informacje: unikalny
# identyfikator leku w bazie DrugBank, nazwę leku, jego typ, opis, postać w jakiej dany lek
# występuje, wskazania, mechanizm działania oraz informacje z jakimi pokarmami dany lek
# wchodzi w interakcje.
from utils import get_id, get_drugs, DfMaker, get_food_interactions


# Infromacje o interakcjach z pokarmami zostały przedstawione w formach list (sprowadzonych do typu string)

def solution_1(data=None):
    columns = ['Drugbank ID',
        'Name',
        'Type',
        'Description',
        'State',
        'Indications',
        'Mechanism of Action',
        'Food interactions']
    dfm = DfMaker(columns)

    for drug in get_drugs(data):
        drug_id = get_id(drug)

        food_interactions = get_food_interactions(drug)
        food_interactions = str(food_interactions).replace('[', '').replace(']', '')

        row = [
            drug_id,
            drug['name'],
            drug['@type'],
            drug['description'],
            drug['state'],
            drug['indication'],
            drug['mechanism-of-action'],
            food_interactions
        ]
        dfm.add_row(row)
    return dfm.make()