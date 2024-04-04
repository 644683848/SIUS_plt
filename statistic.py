from databases import fetch_all, insert_data


def save_to_mysql(rows, table_name, columns):
    print("get_rows")
    for i in range(0, len(rows), 10000):
        print(f"insert_data: {i}-{i + 10000} rows")
        insert_data(table_name, columns, rows[i:i + 10000])


if __name__ == '__main__':
    # table_name = "competition_scores2"
    table_name = "athlete_scores"
    rows = fetch_all(table_name)
    scores_map = {}
    for row in rows:
        date = row[4].strftime('%Y%m%d')
        tournament = row[7]
        ground = row[1]
        if tournament != '0':
            key = date + ': ' + ground
        else:
            key = date
        if scores_map.get(row[0]) is None:
            scores_map[row[0]] = {}
        if scores_map[row[0]].get(key) is None:
            scores_map[row[0]][key] = []
        scores_map[row[0]][key].append(row[3])

    rows = []
    for athlete_name, date_scores in scores_map.items():
        for key, scores in date_scores.items():
            max_scores = -1
            min_scores = 999
            avg = 0
            for score in scores:
                avg += score
                if score > max_scores:
                    max_scores = score
                if score < min_scores:
                    min_scores = score
            avg = avg / len(scores)
            # result.append({"athlete_name": athlete_name, "date": key, "high": max_scores, "low": min_scores, "avg": avg})
            rows.append((athlete_name, key, max_scores, min_scores, avg))

    columns = ['athlete_name', 'date', 'high', 'low', 'avg']
    save_to_mysql(rows, "statistic_scores", columns)
