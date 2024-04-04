import mysql.connector


def connect_to_mysql():
    """
    Connect to MySQL database.

    Returns:
    - connection: MySQL connection object
    """
    try:
        connection = mysql.connector.connect(
            user='root',
            password='uwWHwh5Y5xDSAmq',
            host='101.200.44.29',
            port='27776',
            database='sius'
        )
        return connection
    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL: {error}")
        return None


def insert_data(table_name, columns, rows):
    """
    Insert data into a MySQL table.

    Args:
    - table_name (str): The name of the table to insert data into.
    - columns (list of str): The column names in the table.
    - rows (list of tuples): The values to insert into the table. Each tuple represents one row of data.

    Returns:
    - None
    """
    connection = connect_to_mysql()
    if connection:
        try:
            cursor = connection.cursor()
            placeholders = ', '.join(['%s'] * len(columns))
            sql_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            cursor.executemany(sql_query, rows)
            connection.commit()
            print("Data inserted successfully!")
        except mysql.connector.Error as error:
            print(f"Failed to insert data into MySQL table: {error}")
        finally:
            cursor.close()
            connection.close()


def fetch_all(table_name):
    """
    Fetch all data from a MySQL table.

    Args:
    - table_name (str): The name of the table to fetch data from.

    Returns:
    - None
    """
    connection = connect_to_mysql()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            return rows
        except mysql.connector.Error as error:
            print(f"Error fetching data from MySQL table: {error}")
        finally:
            cursor.close()
            connection.close()
            print('MySQL connection is closed')
