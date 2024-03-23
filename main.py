import csv
import json
import os
from datetime import datetime

import matplotlib.pyplot as plt

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
    _spot_aim_datatime = {}
    files = os.listdir(_directory)

    csv_files = [file for file in files if
                 file.endswith('.csv') and not file.endswith('_mod.csv') and not file.endswith('_stl.csv')]

    # Iterate over each CSV file and read its contents
    for csv_file in csv_files:
        with open(os.path.join(_directory, csv_file), 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                arr = row[0].split(';')
                aim = arr[1]
                ground = '10'
                spot = str(arr[3])
                time = str(arr[6])
                formatted_date = datetime.strptime(
                    csv_file.replace('x', '').replace('X', '').replace('w', '').replace('W', '').replace('.csv', ''),
                    "%Y%m%d").strftime("%Y-%m-%d")
                _date_time = formatted_date + ' ' + time
                if _spot_aim_datatime.get(ground + ';' + spot) is None:
                    _spot_aim_datatime[ground + ';' + spot] = []
                _spot_aim_datatime[ground + ';' + spot].append((_date_time, aim))

    return _spot_aim_datatime


def find_score(ground, spot, begin_end_time, spot_aim_datatime):
    def is_between(time, begin_end_time):
        time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        begin = datetime.strptime(begin_end_time[0], '%Y-%m-%d %H:%M:%S')
        end = begin_end_time[1]
        return begin < time < end

    scores = []
    if spot_aim_datatime.get(str(ground) + ';' + spot) is None:
        return scores
    for time_and_score in spot_aim_datatime[str(ground) + ';' + spot]:
        if is_between(time_and_score[0], begin_end_time):
            scores.append(time_and_score)
    return scores


# 遍历运动员的打靶时间段，再查表获取成绩
def get_result(node, ground, spot, spot_aim_datatime, result, level):
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
                    scores = find_score(ground, spot, begin_end_time, spot_aim_datatime)
                    # elapsed_time = time.time() - start_time
                    # print(f"Elapsed time: {elapsed_time} seconds")
                    result.append({"athlete_name": _athlete_name, "ground": ground, "spot": spot, "scores": scores})
            continue

        get_result(val, ground, spot, spot_aim_datatime, result, level + 1)


# 根据成绩画出折线图
def save_to_plot(x, y, path):
    # Plotting the data
    plt.plot(x, y, marker='o', linestyle='-')

    # Formatting the plot
    plt.title('Line Chart')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.grid(True)

    # Rotating x-axis labels for better readability
    plt.xticks(rotation=45)

    # Displaying the plot
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


if __name__ == '__main__':
    names = ["焦若璇", "高楠", "高莹", "张嘉轩", "李佳静"]
    # names = ["焦若璇"]
    # directory = r'C:\Users\64468\Downloads\10M靶场18日-23日'
    # spot_file_path = r'C:\Users\64468\Downloads\10M.csv'
    # spot_and_time_field = get_spot_and_time_field(spot_file_path)
    # # json_str = json.dumps(tmp, ensure_ascii=False, default=str)
    # # print(json_str)
    #
    # # 根据每个运动员打靶的时间段获取成绩
    # spot_aim_datatime = filter_aim(directory)
    # result = []
    # get_result(spot_and_time_field, None, None, spot_aim_datatime, result, 0)
    #
    # json_str = json.dumps(result, ensure_ascii=False, default=str)
    # file_path = "output.json"
    # # Open the file in write mode and write the JSON string to it
    # with open(file_path, "w", encoding="utf-8") as file:
    #     file.write(json_str)

    with open(r'C:\Users\64468\PycharmProjects\SIUS\output.json', 'r', encoding='utf-8') as file:
        result = json.load(file)
    cnt = 0
    for item in result:
        if item["athlete_name"] not in names:
            continue
        x = []
        y = []
        for key, val in item.items():
            if key == "scores":
                for score in val:
                    x.append(datetime.strptime(score[0], "%Y-%m-%d %H:%M:%S.%f"))
                    y.append(float(score[1]))
        path = r"C:\Users\64468\PycharmProjects\SIUS" + '\\' + item["athlete_name"] + '-' + str(cnt)
        if len(y) != 0:
            save_to_plot(x, y, path)
        cnt += 1

