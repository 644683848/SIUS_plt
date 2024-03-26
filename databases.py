import mysql.connector


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
    try:
        # Establish a connection to the MySQL server
        # Replace 'username', 'password', 'hostname', 'database_name' with your MySQL credentials
        connection = mysql.connector.connect(
            user='root',
            password='uwWHwh5Y5xDSAmq',
            host='101.200.44.29',
            port='27776',
            database='sius'
        )

        # Create a cursor object to execute queries
        cursor = connection.cursor()

        # Construct the SQL query dynamically based on table_name, columns, and number of values
        placeholders = ', '.join(['%s'] * len(columns))
        sql_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

        # Execute the SQL query for each row
        cursor.executemany(sql_query, rows)

        # Commit the transaction
        connection.commit()

        print("Data inserted successfully!")

    except mysql.connector.Error as error:
        print(f"Failed to insert data into MySQL table: {error}")

    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


# # Example usage:
# table_name = 'athlete_scores'
# columns = ['athlete_name', 'ground', 'spot', 'scores', 'datetime']
# rows = [
#     ('Athlete1', 'Ground1', 'Spot1', 10, '2024-03-26 12:00:00'),
#     ('Athlete2', 'Ground2', 'Spot2', 15, '2024-03-26 13:00:00'),
#     # Add more rows as needed
# ]
#
# insert_data(table_name, columns, rows)
