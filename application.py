from flask import (
    Flask,
    render_template,
    request,
)
from resources.sqlactions import (
    create_table,
    write_data_to_db,
    get_table_names,
)
from copy import deepcopy
from psycopg2 import Error
import csv

app = Flask(__name__)


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
        name = request.form.get('manufacture')
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
    names = get_table_names()
    return render_template('generate.html', names=names)
