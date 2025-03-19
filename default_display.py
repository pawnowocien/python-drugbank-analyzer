from matplotlib import pyplot as plt

# Biblioteka z definicjami i  podstawowymi funkcjami dla grafów i wykresów


COLOR_MAIN = 'teal'
COLOR_SECONDARY = 'aquamarine'
COLOR_BETWEEN = 'lightseagreen'
DEFINED_COLORS = [COLOR_MAIN, COLOR_SECONDARY, COLOR_BETWEEN]
COLOR_DEFAULT = COLOR_SECONDARY
COLOR_EDGE = 'gray'
COLOR_BACKGROUND = 'lightgray'

# Listę nazw przemienia na słownik nazwa-kolor
# Przydatne przy podawaniu kolorów dla kategorii wierzchołków grafu
def get_default_colors(_list):
    assert isinstance(_list, list)
    assert len(_list) == len(set(_list))

    _dict = {}
    for i in range(0, len(_list)):
        if i < len(DEFINED_COLORS):
            _dict[_list[i]] = DEFINED_COLORS[i]
        else:
            _dict[_list[i]] = COLOR_DEFAULT

    return _dict


def default_bar_graph(labels, values, xlab=None, ylab=None, title=None, save_path=None, show=True):
    assert isinstance(labels, list)
    assert isinstance(values, list)

    plt.figure(figsize=(12, 6))

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.bar(labels, values, color=COLOR_MAIN, zorder=3)
    plt.xticks(rotation=45, ha='right', fontsize=10)

    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(title)

    plt.tight_layout()

    if show:
        plt.show()
    if save_path:
        plt.savefig(save_path)

    plt.close()