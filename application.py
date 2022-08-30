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
    SECRET_KEY,
)
from werkzeug.utils import secure_filename
from pathlib import Path
from psycopg2 import Error

UPLOAD_FOLDER = Path.cwd()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    try:
        create_table()
    except (Exception, Error):
        pass
    finally:
        pass
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
            machine_path = UPLOAD_FOLDER / f"{machine_filename}"
            machine.save(machine_path)
            volume_filename = secure_filename(volume.filename)
            volume_path = UPLOAD_FOLDER / f"{volume_filename}"
            volume.save(volume_path)
            data_for_db = normalize_csv_data(volume_path, machine_path)
            write_data_to_db(data_for_db, name)
            return redirect(url_for('index'))

    return render_template('load.html')


@app.route("/generate", methods=('GET', 'POST'))
def generate_report():
    names = get_company_names()

    if request.method == "POST":
        comp_name = request.form.get('manufacture')
        first_date = request.form.get('first_date')
        last_date = request.form.get('last_date')

        if not comp_name:
            flash("В базе данных нет записей!")
            return redirect(request.url)

        if not first_date and not last_date:
            data = get_company_content(comp_name)
            create_xlsx_report(data, comp_name, UPLOAD_FOLDER)
            return redirect(url_for('index'))

        if first_date and last_date:
            data = get_company_content(comp_name, first_date, last_date)
            create_xlsx_report(data, comp_name, UPLOAD_FOLDER)
            return redirect(url_for('index'))

        if not first_date or not last_date:
            flash("""Неверно задан диапазон отображения записей!""")
            return redirect(request.url)

    return render_template('generate.html', names=names)
