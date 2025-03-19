# Utworzyć ramkę danych o produktach farmaceutycznych zawierających dany lek
# (substancję leczniczą). Ramka powinna zawierać informacje o ID leku, nazwie produktu,
# producencie, kod w narodowym rejestrze USA (ang. *National Drug Code*), postać w jakiej
# produkt występuje, sposób aplikacji, informacje o dawce, kraju i agencji rejestrującej
# produkt.
from utils import get_drugs, get_id, DfMaker, get_products


def solution_3(data=None):
    columns = ['Drug id',
        'Product Name',
        'Labeller',
        'NDC',
        'Product form',
        'Route',
        'Dosage',
        'Country',
        'Regulatory Agency']
    dfm = DfMaker(columns)

    for drug in get_drugs(data):
        products = get_products(drug)
        if products is None:
            continue
        for product in products:
            row = [
                get_id(drug),
                product['name'],
                product['labeller'],
                product['ndc-product-code'],
                product['dosage-form'],
                product['route'],
                product['strength'],
                product['country'],
                product['source']
            ]
            dfm.add_row(row)

    return dfm.make()