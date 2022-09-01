from psycopg2 import connect
from dotenv import load_dotenv
from resources.file_operations import normalize_names
import os

# Importing data for connection
load_dotenv()

DB_ROLE = os.getenv('DB_ROLE')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')
SECRET_KEY = os.getenv('SECRET_KEY')


# Work with PostgreSQL
def connect_db():
    conn = connect(
        user=DB_ROLE,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        database=DATABASE,
    )
    cursor = conn.cursor()
    return conn, cursor


def disconnect_db(connection, cursor):
    cursor.close()
    connection.close()


def create_table():
    connection, cursor = connect_db()
    table = '''CREATE TABLE company_report (
        date   VARCHAR,
        company   VARCHAR,
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
    for row in data:
        ins_data = f"""INSERT INTO company_report 
        (date, company, vehicle, vehicle_number, square, scope_of_work) VALUES (
            '{row["Дата"]}',
            '{name}',
            '{row["Техника"]}',
            '{row["Номер техники"]}',
            '{row["Площадь, га"]}',
            '{row["Объем работ, м3"]}'
        );"""

        cursor.execute(ins_data)
    connection.commit()
    disconnect_db(connection, cursor)


def get_company_names() -> list:
    connection, cursor = connect_db()
    cursor.execute("SELECT DISTINCT company FROM company_report;")
    raw_names = cursor.fetchall()
    disconnect_db(connection, cursor)
    names = normalize_names(raw_names)
    return names


def get_company_content(name: str, first_date=None, last_date=None) -> list:
    connection, cursor = connect_db()
    query = f"""SELECT date, vehicle, vehicle_number, square, scope_of_work
                FROM company_report WHERE company='{name}'
                AND date BETWEEN '{first_date}' AND '{last_date}';"""

    if not first_date and not last_date:
        query = f"""SELECT date, vehicle, vehicle_number, square, scope_of_work
                    FROM company_report WHERE company='{name}';"""

    cursor.execute(query)
    raw_data = cursor.fetchall()
    disconnect_db(connection, cursor)
    return raw_data


def get_table_content(first_date=None, last_date=None) -> list:
    connection, cursor = connect_db()
    query = f"""SELECT date, vehicle, vehicle_number, square, scope_of_work
                FROM company_report WHERE 
                date BETWEEN '{first_date}' AND '{last_date}';"""

    if not first_date and not last_date:
        query = """SELECT date, vehicle, vehicle_number, square, scope_of_work 
                    FROM company_report;"""

    cursor.execute(query)
    raw_data = cursor.fetchall()
    disconnect_db(connection, cursor)
    return raw_data
