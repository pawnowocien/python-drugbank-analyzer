import argparse
import importlib
import re
from pathlib import Path

from module_13 import generate_dict

DATAFRAME = 'df'
GRAPHIC = 'plt'


# Z wejścia złożonego z symboli 0-9; ',' i '-' (z czego liczby na wejściu muszą być pomiędzy 1 a 12)
# zwraca, które podpunkty wyświetlić
def parse_input(input_str, min_val=1, max_val=12):
    _numbers = set()
    if not re.fullmatch(r"[0-9,\- ]+", input_str):
        raise ValueError("Invalid input format. Only numbers, commas, and hyphens are allowed.")
    
    for seg in input_str.split(","):
        try:
            if "-" in seg:
                start, end = map(int, seg.split("-"))
                if not (min_val <= start <= end <= max_val):
                    raise ValueError(f"Range {start}-{end} is out of bounds ({min_val}-{max_val}).")
                _numbers.update(range(start, end + 1))
            else:
                _num = int(seg)
                if not (min_val <= _num <= max_val):
                    raise ValueError(f"Number {_num} is out of bounds ({min_val}-{max_val}).")
                _numbers.add(_num)
        except ValueError as e:
            print(f"Error parsing input: {e}")
            exit(1)

    return sorted(_numbers)

# Ustawienia związane z opcjami
parser = argparse.ArgumentParser(description="Process input and options.")
parser.add_argument("input_str", type=str, help="Input string containing numbers and ranges.")
parser.add_argument("-sv", action="store_true", help="Save option for plots (true/false)")
parser.add_argument("-sh", action="store_true", help="Show option for plots (true/false)")
parser.add_argument("-ge", action="store_true", help="Run on generated data")

args = parser.parse_args()
parsed_numbers = parse_input(args.input_str)

show_option = args.sh
save_option = args.sv
gen_data = args.ge

if gen_data:
    print('Generating data...')
    data = generate_dict()
    print('Data generated')
else:
    data = None

function_map = {
    1: ("module_01", "solution_1", [DATAFRAME]),
    2: ("module_02", "solution_2", [DATAFRAME, GRAPHIC]),
    3: ("module_03", "solution_3", [DATAFRAME]),
    4: ("module_04", "solution_4", [DATAFRAME]),
    5: ("module_05", "solution_5", [DATAFRAME, GRAPHIC]),
    6: ("module_06", "solution_6", [GRAPHIC]),
    7: ("module_07", "solution_7", [DATAFRAME]),
    8: ("module_08", "solution_8", [GRAPHIC]),
    9: ("module_09", "solution_9", [DATAFRAME, GRAPHIC]),
    10: ("module_10", "solution_10", [DATAFRAME]),
    11: ("module_11", "solution_11", [GRAPHIC]),
    12: ("module_12", "solution_12", [GRAPHIC]),
}

special_inputs = {
    2: "Give drug id for graph: ",
    11: "Give gene for graph: ",
    12: "Give drug id for graph: "
}



if save_option:
    if not Path('graphics').exists():
        Path('graphics').mkdir()

# Wyliczanie funkcji
for num in parsed_numbers:
    mod_name, func_name, tags = function_map[num]
    mod = importlib.import_module(mod_name)
    func = getattr(mod, func_name)
    res=""

    if save_option:
        save_file = Path('graphics') / Path(f"{num}.png")
    else:
        save_file = None

    try:
        if num in special_inputs:
            user_input = input(f"[{num}] " + special_inputs[num])
            if num == 2 or num == 12:
                res = func(drug_id=user_input, data=data, save_path=save_file, show=show_option)
            elif num == 11:
                res = func(gene=user_input, data=data, save_path=save_file, show=show_option,
                        display_text=not gen_data, small_nodes=gen_data)
        else:
            res = func(data=data, save_path=save_file, show=show_option) if GRAPHIC in tags else func(data=data)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")
        exit(1)

    if DATAFRAME in tags:
        print(f"\n\n\n----- S O L U T I O N   {num} -----\n\n")
        print(res)
    if num == 4:
        print('Number of paths:', len(res))