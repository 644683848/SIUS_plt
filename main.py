import configparser
import csv
import os
import time
from datetime import datetime

from databases import insert_data

threshold_seconds = 5


def get_time_period(time_str):
    # Convert string to datetime object
    dt_object = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    # Extract hour component
    hour = dt_object.hour
    # Determine time period
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 18:
        return 'afternoon'
    else:
        return 'evening'


def get_end_period(time_str):
    # Convert string to datetime object
    dt_object = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    # Extract hour component
    hour = dt_object.hour
    # Determine time period
    if 5 <= hour < 12:
        return dt_object.replace(hour=12, minute=0, second=0)
    elif 12 <= hour < 18:
        return dt_object.replace(hour=18, minute=0, second=0)
    else:
        return dt_object.replace(hour=21, minute=0, second=0)


def are_datetimes_close(datetime1, datetime2):
    time_diff = abs((datetime.strptime(datetime1, "%Y-%m-%d %H:%M:%S") - datetime.strptime(datetime2,
                                                                                           "%Y-%m-%d %H:%M:%S")).total_seconds())
    return time_diff <= 5


# 获取每个人在某个靶位的时间段
def get_next_begin_time(current_athlete_name, current_athlete_begin_time, athlete_time_tale):
    result = get_end_period(current_athlete_begin_time)

    def bigger_and_closer(current_begin_time, current_result, next_begin_time):
        current_begin_time = datetime.strptime(current_begin_time, '%Y-%m-%d %H:%M:%S')
        next_begin_time = datetime.strptime(next_begin_time, '%Y-%m-%d %H:%M:%S')
        return current_begin_time < next_begin_time < current_result

    for athlete_name, times in athlete_time_tale.items():
        if current_athlete_name is athlete_name: continue
        for time in times:
            if bigger_and_closer(current_athlete_begin_time, result, time[0]):
                result = datetime.strptime(time[0], '%Y-%m-%d %H:%M:%S')
    return result


def get_spot_and_time_field(file_path):
    result = {}
    with open(file_path, 'r', newline='', encoding='utf-8', errors='ignore') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[0].strip() == '': continue
            athlete = row[0]
            ground = row[3]
            spot = ground + '-' + row[4]
            _date = row[5].split(' ')[0]
            _date_time = row[5]
            if result.get(spot) is None:
                result[spot] = {}
            if result.get(spot).get(_date) is None:
                result[spot][_date] = {_period: {} for _period in ['morning', 'afternoon', 'evening']}
            period = get_time_period(row[5])
            if result.get(spot).get(_date).get(period).get(athlete) is None:
                result[spot][_date][period][athlete] = []
            # 去除异常点
            flag = 1
            for item in result[spot][_date][period][athlete]:
                if are_datetimes_close(item[0], _date_time):
                    flag = 0
            if flag:
                result[spot][_date][period][athlete].append([_date_time, None])

    # 为每个靶场每个靶号每天每个时间段的每个运动员添加结束时间
    def add_end_time(node):
        for key, val in node.items():
            if key in ["morning", "afternoon", "evening"]:
                # 如果这个时间段有不止一个人在用，则后一个人的开始时间就是前一个人的结束时间
                for _athlete_name, times in val.items():
                    for time in times:
                        # 找到大于当前运动员开始时间，并且最近的那个开始时间; 没有找到则置为中午12点/下午6点/晚上9点
                        next_begin_time = get_next_begin_time(_athlete_name, time[0], val)
                        time[1] = next_begin_time
            if key == "evening":
                return
            if isinstance(val, dict):
                add_end_time(val)

    add_end_time(result)
    return result


# 根据姓名找到靶位和时间
def get_spot_and_time(_names):
    file_path = r'C:\Users\64468\Downloads\10M.csv'
    result = {_name.strip(): [] for _name in names}
    with open(file_path, 'r', newline='', encoding='utf-8', errors='ignore') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0].strip() in _names:
                result[row[0].strip()].append(row[4] + ';' + row[5])
    return result


# 根据时刻和靶位找到成绩：姓名-时间-靶位：成绩
def filter_aim(_directory):
    _spot_aim_datetime = {}
    files = os.listdir(_directory)

    csv_files = [file for file in files if
                 file.endswith('.csv') and not file.endswith('_mod.csv') and not file.endswith('_stl.csv')]

    # Iterate over each CSV file and read its contents
    for csv_file in csv_files:
        with open(os.path.join(_directory, csv_file), 'r', newline='') as file:
            reader = csv.reader(file)
            try:
                file_name = csv_file.replace('x', '').replace('X', '').replace('w', '').replace('W', '').replace('.csv',
                                                                                                                 '')
                if len(file_name) != 8:
                    print(file_name)
                    file_name = file_name[:-1]
                formatted_date = datetime.strptime(file_name, "%Y%m%d").strftime("%Y-%m-%d")
            except ValueError as e:
                print(e)
                break
            for row in reader:
                arr = row[0].split(';')
                A_column = arr[0]
                aim = arr[1]
                tournament = arr[2]
                spot = str(arr[3])
                aim4 = arr[4]
                if aim4 != '0':
                    aim = aim4
                if int(float(aim)) == 0 and int(float(aim4)) == 0:
                    continue
                F_column = arr[5]
                time = str(arr[6])
                H_column = arr[7]
                x = arr[8]
                y = arr[9]
                K_column = arr[10]
                L_column = arr[11]
                M_column = arr[12]
                N_column = arr[13]
                O_column = arr[14]
                P_column = arr[15]
                Q_column = arr[16]
                R_column = arr[17]
                S_column = arr[18]
                T_column = arr[19]
                U_column = arr[20]
                V_column = arr[21]
                W_column = arr[22]
                X_column = arr[23]
                Y_column = arr[24]
                Z_column = arr[25]
                AA_column = arr[26]
                AB_column = arr[27]
                _date_time = formatted_date + ' ' + time
                key = spot
                if _spot_aim_datetime.get(key) is None:
                    _spot_aim_datetime[key] = []
                _spot_aim_datetime[key].append(
                    {"tournament": tournament, "x": x, "y": y, "O_column": O_column, "P_column": P_column,
                     "date_time": _date_time, "score": aim,
                     "A_column": A_column, "F_column": F_column, "H_column": H_column,
                     "K_column": K_column, "L_column": L_column, "M_column": M_column,
                     "N_column": N_column, "Q_column": Q_column, "R_column": R_column, "S_column": S_column,
                     "T_column": T_column, "U_column": U_column, "V_column": V_column,
                     "W_column": W_column, "X_column": X_column, "Y_column": Y_column,
                     "Z_column": Z_column, "AA_column": AA_column, "AB_column": AB_column})

    return _spot_aim_datetime


def find_score(spot, begin_end_time, spot_aim_datetime):
    def is_between(time, begin_end_time):
        time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        begin = datetime.strptime(begin_end_time[0], '%Y-%m-%d %H:%M:%S')
        end = begin_end_time[1]
        return begin < time < end

    scores = []
    if spot_aim_datetime.get(spot) is None:
        return scores
    for time_and_score in spot_aim_datetime[spot]:
        if is_between(time_and_score["date_time"], begin_end_time):
            scores.append(time_and_score)
    return scores


# 遍历运动员的打靶时间段，再查表获取成绩
def get_result(node, ground, spot, spot_aim_datetime, result, level):
    for key, val in node.items():
        if level == 0:
            ground = key.split('-')[0]
            spot = key.split('-')[1]
        if key in ["morning", "afternoon", "evening"]:
            # 如果这个时间段有不止一个人在用，则后一个人的开始时间就是前一个人的结束时间
            for _athlete_name, times in val.items():
                # print(_athlete_name)
                # if _athlete_name != "冀子烁": continue
                for begin_end_time in times:
                    # 找到当前时间段内的成绩
                    # start_time = time.time()
                    scores = find_score(spot, begin_end_time, spot_aim_datetime)
                    for score in scores:
                        result.append(
                            {"athlete_name": _athlete_name, "ground": ground, "spot": spot,
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
                    # elapsed_time = time.time() - start_time
                    # print(f"Elapsed time: {elapsed_time} seconds")
            continue

        get_result(val, ground, spot, spot_aim_datetime, result, level + 1)


if __name__ == '__main__':
    names = ["焦若璇", "高楠", "高莹", "张嘉轩", "李佳静"]
    # names = ["焦若璇"]
    directory = r'C:\Users\64468\Downloads\3_25-3_30\10米3.25-30'
    spot_file_path = r'C:\Users\64468\Downloads\3_25-3_30\spot.csv'
    spot_and_time_field = get_spot_and_time_field(spot_file_path)
    # json_str = json.dumps(tmp, ensure_ascii=False, default=str)
    # print(json_str)

    # 根据每个运动员打靶的时间段获取成绩
    spot_aim_datetime = filter_aim(directory)
    result = []
    print("get_result")
    get_result(spot_and_time_field, None, None, spot_aim_datetime, result, 0)
    rows = []
    print("get_rows")
    for data in result:
        rows.append((data["athlete_name"], data["ground"], data["spot"], data["score"], data["date_time"],
                     data["tournament"], data["x"], data["y"], data["O_column"], data["P_column"],
                     data["A_column"], data["F_column"], data["H_column"], data["K_column"],
                     data["L_column"], data["M_column"], data["N_column"], data["Q_column"], data["R_column"],
                     data["S_column"], data["T_column"], data["U_column"], data["V_column"],
                     data["W_column"], data["X_column"], data["Y_column"], data["Z_column"],
                     data["AA_column"], data["AB_column"]))

    table_name = 'athlete_scores'
    columns = ['athlete_name', 'ground', 'spot', 'scores', 'datetime', 'tournament', 'x', 'y', 'O_column', 'P_column',
               'A_column', 'F_column', 'H_column', 'K_column', 'L_column', 'M_column',
               'N_column', 'Q_column', 'R_column', 'S_column', 'T_column', 'U_column', 'V_column',
               'W_column', 'X_column', 'Y_column', 'Z_column', 'AA_column', 'AB_column']
    for i in range(0, len(rows), 10000):
        print(f"insert_data: {i}-{i + 10000} rows")
        insert_data(table_name, columns, rows[i:i + 10000])

    # # Create a ConfigParser object
    # config = configparser.ConfigParser()
    #
    # # Load the INI file
    # config.read('exclude.ini')
    #
    # # Read values from the sections
    # value1 = config['Section1']['key1']
    # value2 = config['Section2']['key2']

    # json_str = json.dumps(result, ensure_ascii=False, default=str)
    # file_path = "output.json"
    # # Open the file in write mode and write the JSON string to it
    # with open(file_path, "w", encoding="utf-8") as file:
    #     file.write(json_str)
    # with open(r'C:\Users\64468\PycharmProjects\SIUS\output.json', 'r', encoding='utf-8') as file:
    #     result = json.load(file)
    # cnt = 0
    # for item in result:
    #     if item["athlete_name"] not in names:
    #         continue
    #     x = []
    #     y = []
    #     for key, val in item.items():
    #         if key == "scores":
    #             for score in val:
    #                 x.append(datetime.strptime(score[0], "%Y-%m-%d %H:%M:%S.%f"))
    #                 y.append(float(score[1]))
    #     path = r"C:\Users\64468\PycharmProjects\SIUS" + '\\' + item["athlete_name"] + '-' + str(cnt)
    #     if len(y) != 0:
    #         save_to_plot(x, y, path)
    #     cnt += 1
