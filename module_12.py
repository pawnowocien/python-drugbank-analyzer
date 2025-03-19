# Zaproponować własną analizę i prezentację danych dotyczących leków. Można w tym
# celu pozyskiwać dodatkowe informacje z innych biomedycznych i bioinformatycznych baz
# danych dostępnych online. Należy jednak upewnić się, czy dana baza danych pozwala na
# zautomatyzowane pobieranie danych przez program. Na przykład baza danych GeneCards
# wprost tego zabrania, co zostało na czerwono podkreślone na tej stronie. Przykładowe bazy
# danych to: UniProt (https://www.uniprot.org/), Small Molecule Pathway Database
# (https://smpdb.ca/), The Human Protein Atlas (https://www.proteinatlas.org/).
import requests

from default_display import default_bar_graph
from utils import get_drugs, normalize_to_list, get_id, get_targets, get_name
from bs4 import BeautifulSoup

# Moim rozwiązaniem jest wykres, który
# dla podanej subst. leczniczej pokazuje w ilu kategoriach znajdują się geny z jego targetów,
# dla każdej kategorii pokazuje ile procent genów z targetów w niej występuje
# Korzystam z The Human Protein Atlas (https://www.proteinatlas.org/)


# Zwraca geny ze wszystkich targetów danego leku
def get_genes(drug):
    # Żeby geny nie powtarzały się, są przetrzymywane w secie
    genes = set()
    targets = get_targets(drug)
    if targets is None:
        return genes
    for target in targets:
        if 'polypeptide' not in target.keys():      # niektóre targety nie są białkami
            continue
        for polypeptide in normalize_to_list(target['polypeptide']):
            genes.add(polypeptide['gene-name'])
    return genes


# Dla danego genu zwraca tekst ze strony, która go opisuje
def get_site(gene):
    # Generuje wyniki wyszukiwania
    site = "https://www.proteinatlas.org/search/" + gene
    response = requests.get(site)
    website = BeautifulSoup(response.text, 'html.parser')

    # Znajduje odpowiedni link wśród wszystkich na stronie
    links = website.find_all('a')
    href_links = [link['href'] for link in links if 'href' in link.attrs]
    for href_link in href_links:
        if href_link.endswith("-" + gene):
            gene_site = 'https://www.proteinatlas.org' + href_link
            response = requests.get(gene_site)
            return BeautifulSoup(response.text, 'html.parser')


# Zwraca klasy z podanej tabeli
def get_classes(table):
    for row in table.find_all('tr'):
        header = row.find("th")
        cell = row.find("td")
        if header and "Protein class" in header.get_text(strip=True):
            return [item.strip() for item in cell.stripped_strings]


# Generuje wykres dla danego leku
def gen_plot_for_drug(drug, save_path=None, show=True):
    count_dict = {}
    genes = get_genes(drug)

    # Zliczanie klas dla każdego genu
    for gene in genes:
        website = get_site(gene)
        table = website.find('table', attrs={'class': 'summary_info'})
        protein_classes = get_classes(table)
        for prot_class in protein_classes:
            count_dict[prot_class] = count_dict.get(prot_class, 0) + 1

    # Wyznaczenie danych
    classes = list(count_dict.keys())
    values = list(count_dict.values())
    ratios = [100 * v / len(genes) for v in values]

    default_bar_graph(classes, ratios,
                      xlab='Protein Classes',
                      ylab='Procentage of Genes',
                      title='Distribution of Genes from Targets Across Protein Classes for ' + get_name(drug),
                      save_path=save_path, show=show)


def solution_12(drug_id, data=None, save_path=None, show=True):
    # Znajduje lek o podanym id i generuje dla niego wykres
    for drug in get_drugs(data):
        if get_id(drug) == drug_id:
            gen_plot_for_drug(drug, save_path, show)
            return