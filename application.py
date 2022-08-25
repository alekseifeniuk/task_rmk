from flask import (
    Flask,
    render_template,
    request,
)
import csv
from copy import deepcopy
from psycopg2 import Error, connect

app = Flask(__name__)


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


def get_csv_content(file_path: str) -> iter:
    with open(file_path, encoding="utf-8-sig") as content:
        return list(csv.DictReader(content))


def normalize_csv_data(volume_path: str, machine_path: str) -> list:
    volume_raw = get_csv_content(volume_path)
    machine_raw = get_csv_content(machine_path)
    result_data = deepcopy(machine_raw)
    for item in result_data:
        for i in range(len(machine_raw)):

            if item["Data"] == volume_raw[i]["Data"]:
                item.update(volume_raw[i])

    return result_data


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

    return render_template('load.html')


@app.route("/generate")
def generate_report():
    return render_template('generate.html')
