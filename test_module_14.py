import os
from unittest.mock import mock_open, patch
import pytest
from pandas import DataFrame
from pathlib import Path

import module_02
import module_09
import utils
from module_01 import solution_1
from module_03 import solution_3
from module_05 import get_all_pathways
from module_07 import solution_7
from module_09 import solution_9a
from module_10 import solution_10
from module_13 import generate_dict


SHOW_PLOTS = False   # Testy będą pokazywały również wykresy/grafy

PLOTS_PATH = Path('tmp')
if not os.path.exists(PLOTS_PATH):
    os.makedirs(PLOTS_PATH)



def gen_drug(drug_id, name):
    return {
        'drugbank-id': [{'@primary': 'true', '#text': drug_id}],
        'name': name
    }
def simple_drug_list(size):
    _list = []
    for i in range(size):
        _list.append(gen_drug('id_' + str(i), 'drug ' + str(i)))
    return _list



#   +-------------------------------------------------------------------------------------------------------------+
#   |--------------------------------------------------- UTILS ---------------------------------------------------|
#   +-------------------------------------------------------------------------------------------------------------+

@pytest.fixture()
def simple_dict():
    return {
        'drugbank': {
            'drug': simple_drug_list(100)
        }
    }

@pytest.fixture
def simple_xml_file():
    # Aby get_id() poprawnie się wczytywało potrzebna jest lista id
    # Stąd drugie id 'filler'
    return """<?xml version="1.0" encoding="UTF-8"?>
    <drugbank>
        <drug>
            <drugbank-id primary="true">id_0</drugbank-id>
            <drugbank-id>filler</drugbank-id>
            <name>drug 0</name>
        </drug>
        <drug>
            <drugbank-id primary="true">id_1</drugbank-id>
            <drugbank-id>filler</drugbank-id>
            <name>drug 1</name>
        </drug>
    </drugbank>"""

@pytest.fixture
def atr_dicts():
    return [{},
            { 'attrs': None },
            { 'attrs': {'attr': {'name': 'attr1'} } },
            { 'attrs': {'attr': [{'name': 'attr1'}, {'name': 'attr2'}] } } ]


# Podstawowe funkcje z utils
def test_utils(simple_dict, simple_xml_file, atr_dicts):
    assert len(utils.get_drugs()) == 100
    assert utils.get_id(utils.get_drugs()[0]) == 'DB00001'
    assert utils.get_id(utils.get_drugs()[99]) == 'DB00108' # W oryginalnej bazie 100. lek ma id 108
    assert utils.get_name(utils.get_drugs()[0]) == 'Lepirudin'
    assert utils.get_name(utils.get_drugs()[99]) == 'Natalizumab'

    assert len(utils.get_drugs(simple_dict)) == 100
    assert utils.get_name(utils.get_drugs(simple_dict)[0]) == 'drug 0'
    assert utils.get_name(utils.get_drugs(simple_dict)[99]) == 'drug 99'
    assert utils.get_id(utils.get_drugs(simple_dict)[0]) == 'id_0'
    assert utils.get_id(utils.get_drugs(simple_dict)[99]) == 'id_99'

    with patch("builtins.open", mock_open(read_data=simple_xml_file)):
        _dict = utils.get_drugs("file.xml")
        assert len(utils.get_drugs(_dict)) == 2
        assert utils.get_name(utils.get_drugs(_dict)[0]) == 'drug 0'
        assert utils.get_name(utils.get_drugs(_dict)[1]) == 'drug 1'
        assert utils.get_id(utils.get_drugs(_dict)[0]) == 'id_0'
        assert utils.get_id(utils.get_drugs(_dict)[1]) == 'id_1'

    assert utils.get_list_of_atr(atr_dicts[0], 'attr') is None
    assert utils.get_list_of_atr(atr_dicts[1], 'attr') is None
    assert utils.get_list_of_atr(atr_dicts[2], 'attr')[0]['name'] == 'attr1'
    assert utils.get_list_of_atr(atr_dicts[3], 'attr')[0]['name'] == 'attr1'
    assert utils.get_list_of_atr(atr_dicts[3], 'attr')[1]['name'] == 'attr2'


# DataFrame Maker
@pytest.mark.parametrize("columns, rows, df",[
    (['col1', 'col2'], [ [1, 1], [2, 2] ], DataFrame({'col1': [1, 2], 'col2': [1, 2]})),
    (['col1', 'col2'], [ ['1', '1'], ['2', '2'] ], DataFrame({'col1': ['1', '2'], 'col2': ['1', '2']})),
    (['col1', 'col2', 'col3'], [ [1, 2, 3], [4, 5, 6], [7, 8, 9], [0, 0, 0] ],
        DataFrame({'col1': [1, 4, 7, 0], 'col2': [2, 5, 8, 0], 'col3': [3, 6, 9, 0]}))
])
def test_dfm(columns, rows, df):
    dfm = utils.DfMaker(columns)
    for row in rows:
        dfm.add_row(row)
    assert dfm.make().equals(df)



#   +-------------------------------------------------------------------------------------------------------------+
#   |------------------------------------------------- SOLUTIONS -------------------------------------------------|
#   +-------------------------------------------------------------------------------------------------------------+


@pytest.fixture()
def drugs_wtih_pathways():
    return {
        'drugbank': {
            'drug': [
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_1'}, 'filler'],
                 'name': 'drug_1',
                 'pathways': {'pathway':
                                  [{'smpdb-id': 'pth_id_1', 'name': 'pathway_1',
                                    'drugs': {'drug': {'drugbank-id': 'id_1', 'name': 'drug_1'}}},
                                   {'smpdb-id': 'pth_id_2', 'name': 'pathway_2',
                                    'drugs': {'drug': {'drugbank-id': 'id_1', 'name': 'drug_1'}}},
                                   {'smpdb-id': 'pth_id_3', 'name': 'pathway_3',
                                    'drugs': {'drug': [{'drugbank-id': 'id_1', 'name': 'drug_1'},
                                                       {'drugbank-id': 'id_2', 'name': 'drug_2'}]}}]}
                 },{
                'drugbank-id': [{'@primary': 'true', '#text': 'id_2'}, 'filler'],
                'name': 'drug_2',
                'pathways': {'pathway':
                             [{'smpdb-id': 'pth_id_3', 'name': 'pathway_3',
                               'drugs': {'drug': [{'drugbank-id': 'id_1', 'name': 'drug_1'},
                                                  {'drugbank-id': 'id_2', 'name': 'drug_2'}]}},
                              {'smpdb-id': 'pth_id_4', 'name': 'pathway_4',
                               'drugs': {'drug': [{'drugbank-id': 'id_2', 'name': 'drug_2'},
                                                  {'drugbank-id': 'id_999', 'name': 'drug_999'}]}}]}
                },{
                'drugbank-id': [{'@primary': 'true', '#text': 'id_3'}, 'filler'],
                'name': 'drug_3'
                }
            ]
        }
    }


def test_module_05a(drugs_wtih_pathways):
    df1 = DataFrame({'Pathway': ['pathway_1', 'pathway_2', 'pathway_3', 'pathway_3', 'pathway_4', 'pathway_4'],
                     'Drug':    ['id_1',     'id_1',     'id_1',     'id_2',     'id_2',     'id_999']})
    df2 = DataFrame({'Pathway': ['pth_id_1', 'pth_id_2', 'pth_id_3', 'pth_id_3', 'pth_id_4', 'pth_id_4'],
                     'Drug':    ['id_1',     'id_1',     'id_1',     'id_2',     'id_2',     'id_999']})
    res1 = get_all_pathways(drugs_wtih_pathways, ids=False)
    res1 = res1.sort_values(['Pathway', 'Drug'])[['Pathway', 'Drug']].reset_index(drop=True)

    res2 = get_all_pathways(drugs_wtih_pathways, ids=True)
    res2 = res2.sort_values(['Pathway', 'Drug'])[['Pathway', 'Drug']].reset_index(drop=True)

    assert df1.equals(res1)
    assert df2.equals(res2)


target1 = {
     'id': 'id_1',
     'polypeptide': {
         '@source': 'source_A',
         '@id': 'poly_id_1',
         'name': 'poly_1',
         'gene-name': 'gene_1',
         'chromosome-location': 'ch_loc_1',
         'cellular-location': 'ce_loc_1',
         'external-identifiers': {
             'external-identifier': [
                 {
                     'resource': 'filler',
                     'identifier': 'filler'
                 },{
                     'resource': 'GenAtlas',
                     'identifier': 'ga_id_1'
                 }
             ]
         }
     }
}
target2 = {
     'id': 'id_2',
     'polypeptide': {
         '@source': 'source_A',
         '@id': 'poly_id_2',
         'name': 'poly_2',
         'gene-name': 'gene_2',
         'chromosome-location': 'ch_loc_2',
         'cellular-location': 'ce_loc_2',
         'external-identifiers': {
             'external-identifier': [
                 {
                     'resource': 'filler',
                     'identifier': 'filler'
                 }
             ]
         }
     }
}
target3 = {
    'id': 'id_3'
}

@pytest.fixture()
def drugs_with_targets():
    return {
        'drugbank': {
            'drug': [
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_1'}, 'filler'],
                 'name': 'drug_1',
                 'targets': {'target': target1 }
                 },
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_2'}, 'filler'],
                 'name': 'drug_2',
                 'targets': {'target': [ target1, target2 ]}
                 },
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_3'}, 'filler'],
                 'name': 'drug_3',
                 'targets': {'target': [ target1, target2, target3 ]}
                 },
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_4'}, 'filler'],
                 'name': 'drug_4'
                 }
            ]
        }
    }


def test_module_7(drugs_with_targets):
    df = DataFrame({'Target id': ['id_1', 'id_2'],
                     'Source': ['source_A', 'source_A'],
                     'Foreign Id': ['poly_id_1', 'poly_id_2'],
                     'Polypeptide name': ['poly_1', 'poly_2'],
                     'Gene name': ['gene_1', 'gene_2'],
                     'Gene GenAtlas id': ['ga_id_1', None],
                     'Chromosome Location': ['ch_loc_1', 'ch_loc_2'],
                     'Cellular location': ['ce_loc_1', 'ce_loc_2']})
    res = solution_7(drugs_with_targets).sort_values(['Target id']).reset_index(drop=True)
    assert df.equals(res)


@pytest.fixture()
def drugs_with_groups():
    return {
        'drugbank': {
            'drug': [
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_1'}, 'filler'],
                 'name': 'drug_1',
                 'groups': {'group': ['approved']}
                 },
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_2'}, 'filler'],
                 'name': 'drug_2',
                 'groups': {'group': ['approved', 'experimental']}
                 },
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_3'}, 'filler'],
                 'name': 'drug_3',
                 'groups': {'group': ['approved', 'withdrawn']}
                 },
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_4'}, 'filler'],
                 'name': 'drug_4',
                 'groups': {'group': ['approved', 'experimental', 'withdrawn']}
                 },
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_5'}, 'filler'],
                 'name': 'drug_5',
                 'groups': {'group': ['approved', 'vet_approved']}
                 },
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_6'}, 'filler'],
                 'name': 'drug_6',
                 'groups': {'group': ['approved', 'experimental', 'investigational']}
                 }
            ]
        }
    }


def test_module_9a(drugs_with_groups):
    df = DataFrame({
        'Id': ['id_1',
               'id_2', 'id_2',
               'id_3', 'id_3',
               'id_4', 'id_4', 'id_4',
               'id_5', 'id_5',
               'id_6', 'id_6', 'id_6'],
        'State': ['approved',
                  'approved', 'experimental',
                  'approved', 'withdrawn',
                  'approved', 'experimental', 'withdrawn',
                  'approved', 'vet_approved',
                  'approved', 'experimental', 'investigational']
    })
    res = solution_9a(drugs_with_groups).sort_values(['Id', 'State']).reset_index(drop=True)
    assert df.equals(res)


@pytest.fixture()
def drugs_with_interactions():
    return {
        'drugbank': {
            'drug': [
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_1'}, 'filler'],
                 'name': 'drug_1',
                 'drug-interactions': {'drug-interaction': [
                     {
                        'drugbank-id': 'id_2',
                         'description': 'desc_1_2'
                     },{
                        'drugbank-id': 'id_3',
                         'description': 'desc_1_3'
                     },{
                        'drugbank-id': 'id_999',
                         'description': 'desc_1_999'
                     }]}
                 },
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_2'}, 'filler'],
                 'name': 'drug_2',
                 'drug-interactions': {'drug-interaction':
                     {
                        'drugbank-id': 'id_1',
                         'description': 'desc_1_2'
                     }}
                 },
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_3'}, 'filler'],
                 'name': 'drug_3',
                 'drug-interactions': {'drug-interaction':
                     {
                        'drugbank-id': 'id_1',
                         'description': 'desc_1_3'
                     }}
                 },
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_4'}, 'filler'],
                 'name': 'drug_4'
                 }
            ]
        }
    }


def test_module_10(drugs_with_interactions):
    df = DataFrame({
        "Id 1": ['id_1', 'id_1', 'id_1'],
        "Id 2": ['id_2', 'id_3', 'id_999'],
        "Description": ['desc_1_2', 'desc_1_3', 'desc_1_999']
    })
    res = solution_10(drugs_with_interactions).sort_values(['Id 1', 'Id 2']).reset_index(drop=True)
    assert df.equals(res)


def test_module_13():
    # Poprawna kopia oryginalnej bazy
    original_dict = generate_dict(imported=100, target_size=100)
    assert solution_1().equals(solution_1(original_dict))
    assert solution_3().equals(solution_3(original_dict))

    # Odpowiednia liczba leków
    dict_1000_drugs = generate_dict(imported=100, target_size=1000)
    assert len(utils.get_drugs(dict_1000_drugs)) == 1000

    # Działająca baza bez importowanych leków
    dict_pure_gen = generate_dict(imported=0, target_size=1000)
    assert len(utils.get_drugs(dict_pure_gen)) == 1000
    assert utils.get_id(utils.get_drugs(dict_pure_gen)[0]) == 'DB00001'

    # Brak duplikacji id
    used_ids = set()
    for drug in utils.get_drugs(dict_1000_drugs):
        assert utils.get_id(drug) not in used_ids
        used_ids.add(utils.get_id(drug))
    used_ids = set()
    for drug in utils.get_drugs(dict_pure_gen):
        assert utils.get_id(drug) not in used_ids
        used_ids.add(utils.get_id(drug))



#   +-------------------------------------------------------------------------------------------------------------+
#   |---------------------------------------------- DEFAULT DISPLAY ----------------------------------------------|
#   +-------------------------------------------------------------------------------------------------------------+


def test_default_display():
    from default_display import get_default_colors
    for i in [0, 5, 10, 20, 100]:
        tmp_list = list(range(i))
        assert len(get_default_colors(tmp_list)) == i

    if not SHOW_PLOTS:
        return
    from default_display import default_bar_graph

    path = PLOTS_PATH / 'dd_test.png'
    assert not os.path.exists(path)

    labels = ['lab_1', 'lab_2', 'lab_3']
    values = [1, 10, 100]
    xlab = ['x_labels']
    ylab = ['y_labels']
    title = ['title']

    default_bar_graph(labels, values, xlab, ylab, title, path)
    assert os.path.exists(path)
    os.remove(path)

    default_bar_graph(labels, values, show=False)
    default_bar_graph(labels, values)



#   +-------------------------------------------------------------------------------------------------------------+
#   |--------------------------------------------------- PLOTS ---------------------------------------------------|
#   +-------------------------------------------------------------------------------------------------------------+


@pytest.fixture()
def drugs_with_synonyms():
    return {
        'drugbank': {
            'drug': [
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_1'}, 'filler'],
                 'name': 'drug_1',
                 'synonyms': {'synonym': {'#text': 'synonym_1'}}
                 },
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_2'}, 'filler'],
                 'name': 'drug_2',
                 'synonyms': {'synonym': [{'#text': 'synonym_1'}, {'#text': 'synonym_2'}]}
                 },
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_3'}, 'filler'],
                 'name': 'drug_3'
                 },
                {'drugbank-id': [{'@primary': 'true', '#text': 'id_4'}, 'filler'],
                 'name': 'drug_4',
                 'synonyms': {'synonym': {'#text': 'drug_4'}}
                 }
            ]
        }
    }


def test_module_2(drugs_with_synonyms):
    if not SHOW_PLOTS:
        return
    # 1 synonim
    module_02.gen_syn_graph('id_1', data=drugs_with_synonyms)
    # 2 synonimy
    module_02.gen_syn_graph('id_2', data=drugs_with_synonyms)
    # 0 synonimów
    module_02.gen_syn_graph('id_3', data=drugs_with_synonyms)
    # 0 synonimów (mimo że sam jest swoim synonimem)
    module_02.gen_syn_graph('id_4', data=drugs_with_synonyms)


def test_module_9b():
    if not SHOW_PLOTS:
        return

    groups = ['approved', 'experimental', 'investigational', 'vet_approved', 'withdrawn']
    def add_group(drug, group_name):
        if 'groups' not in drug.keys():
            drug['groups'] = {'group': group_name}
        elif not isinstance(drug['groups']['group'], list):
            drug['groups']['group'] = [drug['groups']['group'], group_name]
        else:
            drug['groups']['group'].append(group_name)
        return drug

    data = {
        'drugbank': {
            'drug': []
        }
    }
    _ = ''
    tmp = gen_drug(_, _)
    for group in groups:
        add_group(tmp, group)
    data['drugbank']['drug'].append(tmp)
    module_09.solution_9b(data)
    for group in groups:
        if group != 'investigational':
            module_09.solution_9b(data, show_one=group)
    tmp = gen_drug(_, _)
    add_group(tmp, 'approved')
    add_group(tmp, 'experimental')
    data['drugbank']['drug'].append(tmp)

    tmp = gen_drug(_, _)
    add_group(tmp, 'approved')
    add_group(tmp, 'withdrawn')
    data['drugbank']['drug'].append(tmp)

    module_09.solution_9b(data)
    module_09.solution_9b(data, simplified=True)
    for group in groups:
        if group != 'investigational':
            module_09.solution_9b(data, show_one=group)


