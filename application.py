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
)
from resources.sql_operations import (
    create_table,
    write_data_to_db,
    get_company_names,
    get_company_content,
    get_table_content,
    SECRET_KEY,
)
from werkzeug.utils import secure_filename
from pathlib import Path
from psycopg2 import Error

UPLOAD_FOLDER = Path.cwd()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=('GET', 'POST'))
def index():

    try:
        create_table()
    except (Exception, Error):
        pass
    finally:
        pass

    names = get_company_names()
    rows = get_table_content()
    return render_template('index.html', names=names, rows=rows)


@app.route('/upload', methods=('GET', 'POST'))
def upload_data():

    if request.method == "POST":
        name = request.form.get('manufacture')
        machine = request.files["machine"]
        volume = request.files["volume"]

        if volume.filename == '' or machine.filename == '':
            flash("Не выбран один из файлов!")
            return redirect(url_for('index'))

        if machine and volume:
            machine_filename = secure_filename(machine.filename)
            machine_path = UPLOAD_FOLDER / f"{machine_filename}"
            machine.save(machine_path)
            volume_filename = secure_filename(volume.filename)
            volume_path = UPLOAD_FOLDER / f"{volume_filename}"
            volume.save(volume_path)
            data_for_db = normalize_csv_data(volume_path, machine_path)
            write_data_to_db(data_for_db, name)

    return redirect(url_for('index'))


@app.route('/report', methods=('GET', 'POST'))
def generate_report():

    if request.method == 'GET':
        comp_name = request.args.get('man')
        first_date = request.args.get('first_date')
        last_date = request.args.get('last_date')

        if not comp_name:
            flash("В базе данных нет записей!")
            return redirect(url_for('index'))

        if not first_date and not last_date:
            data = get_company_content(comp_name)
            create_xlsx_report(data, comp_name, UPLOAD_FOLDER)
            return redirect(url_for('index'))

        if first_date and last_date:
            data = get_company_content(comp_name, first_date, last_date)
            create_xlsx_report(data, comp_name, UPLOAD_FOLDER)
            return redirect(url_for('index'))

        if not first_date or not last_date:
            flash("Неверно задан диапазон отображения записей!")
            return redirect(url_for('index'))
