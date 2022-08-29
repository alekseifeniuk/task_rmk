from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from resources.file_operations import (
    create_xlsx_report,
    normalize_csv_data,
    normalize_db_table_name,
)
from resources.sql_operations import (
    create_table,
    write_data_to_db,
    get_table_names,
    get_table_content,
)
from os import path
from psycopg2 import Error
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "/home/alekseyf/task_from_rmk/reports"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "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"


# Work with HTML
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/load', methods=('GET', 'POST'))
def load_data():

    if request.method == "POST":
        name = request.form.get('manufacture')
        machine = request.files["machine"]
        volume = request.files["volume"]

        if volume.filename == '' or machine.filename == '':
            flash("Не выбран один из файлов!")
            return redirect(request.url)

        if machine and volume:
            machine_filename = secure_filename(machine.filename)
            machine_path = path.join(UPLOAD_FOLDER, machine_filename)
            machine.save(machine_path)
            volume_filename = secure_filename(volume.filename)
            volume_path = path.join(UPLOAD_FOLDER, volume_filename)
            volume.save(volume_path)
            data_for_db = normalize_csv_data(volume_path, machine_path)
            try:
                create_table(name)
            except (Exception, Error):
                pass
            finally:
                write_data_to_db(data_for_db, name)
                return redirect(url_for('index'))

    return render_template('load.html')


@app.route("/generate", methods=('GET', 'POST'))
def generate_report():
    db_names = get_table_names()
    names = normalize_db_table_name(db_names)

    if request.method == "POST":
        name = request.form.get('manufacture')

        if not name:
            flash("В базе данных нет записей!")
            return redirect(request.url)
        else:
            report_data = get_table_content(name)
            create_xlsx_report(report_data, name)
            return redirect(url_for('index'))

    return render_template('generate.html', names=names)
