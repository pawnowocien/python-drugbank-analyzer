# Dla każdego leku w bazie danych podać liczbę szlaków, z którymi dany lek wchodzi w
# interakcje. Przedstawić wyniki w postaci histogramu z odpowiednio opisanymi osiami.
from default_display import default_bar_graph
from utils import get_name
from utils import get_drugs, get_id, get_pathways


def solution_6(data=None, save_path=None, show=True, ids=False):
    # Zliczanie szlaków dla każdego leku
    path_count = {}
    for drug in get_drugs(data):
        pathways = get_pathways(drug)
        if pathways is not None:    # Pomijamy leki bez szlaków dla wyższej czytelności
            if ids:
                x_lab = get_id(drug)
            else:
                x_lab = get_name(drug)
            path_count[x_lab] = len(pathways)

    # Generacja odpowiedniego wykresu
    names = list(path_count.keys())
    values = list(path_count.values())

    default_bar_graph(names, values,
                      xlab='Drugs', ylab='Number of Pathways', title='Pathways per Drug',
                      save_path=save_path, show=show)