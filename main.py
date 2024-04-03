import csv

from databases import insert_data
from utils import get_time_period, are_datetimes_close, get_next_begin_time, filter_aim, get_result


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


if __name__ == '__main__':
    directory = r'C:\Users\64468\Downloads\3_25-3_30\10米3.25-30'
    spot_file_path = r'C:\Users\64468\Downloads\3_25-3_30\spot.csv'
    spot_and_time_field = get_spot_and_time_field(spot_file_path)

    # 根据每个运动员打靶的时间段获取成绩
    spot_aim_datetime = filter_aim(directory)
    result = []
    print("get_result")
    get_result(spot_and_time_field, None, None, spot_aim_datetime, result, 0)

    # rows = []
    # print("get_rows")
    # for data in result:
    #     rows.append((data["athlete_name"], data["ground"], data["spot"], data["score"], data["date_time"],
    #                  data["tournament"], data["x"], data["y"], data["O_column"], data["P_column"],
    #                  data["A_column"], data["F_column"], data["H_column"], data["K_column"],
    #                  data["L_column"], data["M_column"], data["N_column"], data["Q_column"], data["R_column"],
    #                  data["S_column"], data["T_column"], data["U_column"], data["V_column"],
    #                  data["W_column"], data["X_column"], data["Y_column"], data["Z_column"],
    #                  data["AA_column"], data["AB_column"]))
    #
    # table_name = 'athlete_scores'
    # columns = ['athlete_name', 'ground', 'spot', 'scores', 'datetime', 'tournament', 'x', 'y', 'O_column', 'P_column',
    #            'A_column', 'F_column', 'H_column', 'K_column', 'L_column', 'M_column',
    #            'N_column', 'Q_column', 'R_column', 'S_column', 'T_column', 'U_column', 'V_column',
    #            'W_column', 'X_column', 'Y_column', 'Z_column', 'AA_column', 'AB_column']
    # for i in range(0, len(rows), 10000):
    #     print(f"insert_data: {i}-{i + 10000} rows")
    #     insert_data(table_name, columns, rows[i:i + 10000])

