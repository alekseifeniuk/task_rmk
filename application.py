from flask import (
    Flask,
    render_template,
    request,
)
from copy import deepcopy
from psycopg2 import Error, connect
import csv

app = Flask(__name__)


# Work with PostgreSQL
def connect_db():
    try:
        conn = connect(
            user="zuba",
            password="jw8s0F4",
            host="127.0.0.1",
            port="5432",
            database="my_db",
        )
        cursor = conn.cursor()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL!", error)
    finally:
        if conn:
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


# Work with CSV data
def get_csv_data(file_path: str) -> iter:
    with open(file_path, encoding="utf-8-sig") as content:
        return list(csv.DictReader(content))


def normalize_csv_data(volume_path: str, machine_path: str) -> list:
    volume_raw = get_csv_data(volume_path)
    machine_raw = get_csv_data(machine_path)
    result_data = deepcopy(machine_raw)
    for item in result_data:
        for i in range(len(machine_raw)):

            if item["Дата"] == volume_raw[i]["Дата"]:
                item.update(volume_raw[i])

    return result_data


# Work with HTML
@app.route('/')
def root():
    return render_template('index.html')


@app.route('/load', methods=('GET', 'POST'))
def load_data():

    if request.method == "POST":
        name = request.form['name']
        volume = request.form['volume']
        machine = request.form['machine']
        data_for_db = normalize_csv_data(volume, machine)
        try:
            create_table(name)
        except (Exception, Error):
            pass
        finally:
            write_data_to_db(data_for_db, name)

    return render_template('load.html')


@app.route("/generate")
def generate_report():
    return render_template('generate.html')
