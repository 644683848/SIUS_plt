import csv
import os

from utils import filter_aim, save_to_mysql

filename = 'StartNumbersOfEntries.csv'


def get_name_id(directory):
    result = {}
    competition_name = None
    with open(os.path.join(directory, filename), 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        current_name = None
        for row in reader:
            if reader.line_num == 1:
                competition_name = row[1]
                continue
            if row[0].isdigit():
                result[row[0]] = current_name
            else:
                if '\n' not in row[0]: current_name = row[0]
                else: current_name = row[0][row[0].index('\n') + 1:]
    print(result)
    return competition_name, result


if __name__ == '__main__':
    root = r'C:\Users\64468\Documents\workspace\HB\competition'
    directories = os.listdir(root)
    for directory in directories:
        competition_name, id_name_map = get_name_id(os.path.join(root, directory))
        # 遍历成绩csv
        spot_aim_datetime = filter_aim(os.path.join(root, directory))
        result = []
        for spot, item in spot_aim_datetime.items():
            for score in item:
                _athlete_name = id_name_map.get(score['A_column'])
                if _athlete_name is not None:
                    result.append(
                        {"athlete_name": _athlete_name, "ground": competition_name, "spot": spot,
                         "tournament": score["tournament"],
                         "x": score["x"], "y": score["y"],
                         "O_column": score["O_column"],
                         "P_column": score["P_column"], "date_time": score["date_time"], "score": score["score"],
                         "A_column": score["A_column"],
                         "F_column": score["F_column"],
                         "H_column": score["H_column"],
                         "K_column": score["K_column"],
                         "L_column": score["L_column"],
                         "M_column": score["M_column"],
                         "N_column": score["N_column"],
                         "Q_column": score["Q_column"],
                         "R_column": score["R_column"],
                         "S_column": score["S_column"],
                         "T_column": score["T_column"],
                         "U_column": score["U_column"],
                         "V_column": score["V_column"],
                         "W_column": score["W_column"],
                         "X_column": score["X_column"],
                         "Y_column": score["Y_column"],
                         "Z_column": score["Z_column"],
                         "AA_column": score["AA_column"],
                         "AB_column": score["AB_column"]
                         })
        table_name = 'competition_scores2'
        save_to_mysql(result, table_name)
