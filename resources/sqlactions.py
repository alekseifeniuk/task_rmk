from psycopg2 import connect


# Work with PostgreSQL
def connect_db():
    conn = connect(
        user="zuba",
        password="jw8s0F4",
        host="127.0.0.1",
        port="5432",
        database="my_db",
    )
    cursor = conn.cursor()
    return conn, cursor


def disconnect_db(connection, cursor):
    cursor.close()
    connection.close()


def create_table(name: str):
    connection, cursor = connect_db()
    table = f'''CREATE TABLE {name} (
        ID SERIAL PRIMARY KEY,
        date   VARCHAR,
        vehicle   VARCHAR,
        vehicle_number   VARCHAR,
        square   VARCHAR,
        scope_of_work   VARCHAR
    );'''
    cursor.execute(table)
    connection.commit()
    disconnect_db(connection, cursor)


def write_data_to_db(data: list, name: str):
    connection, cursor = connect_db()
    for line in data:
        ins_data = f"""INSERT INTO {name} 
        (date, vehicle, vehicle_number, square, scope_of_work) VALUES (
            '{line["Дата"]}',
            '{line["Техника"]}',
            '{line["Номер техники"]}',
            '{line["Площадь, га"]}',
            '{line["Объем работ, м3"]}'
        );"""

        cursor.execute(ins_data)
    connection.commit()
    disconnect_db(connection, cursor)


def get_table_names():
    connection, cursor = connect_db()
    query = """SELECT table_name FROM information_schema.tables 
                WHERE table_schema='public';"""
    cursor.execute(query)
    tables = cursor.fetchall()
    disconnect_db(connection, cursor)
    return tables
