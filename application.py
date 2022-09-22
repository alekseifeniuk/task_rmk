from pathlib import Path
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from werkzeug.utils import secure_filename
from resources.file_operations import (
    create_xlsx_report,
    normalize_csv_data,
)
from resources.sql_operations import (
    write_data_to_db,
    get_company_names,
    get_company_content,
    get_table_content,
    SECRET_KEY,
)

# Getting the path to save files
UPLOAD_FOLDER = Path.cwd()

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = SECRET_KEY


# Work with HTML
@app.route("/", methods=["GET"])
def index():
    names = get_company_names()
    comp_name = request.args.get("man", "all")
    first_date = request.args.get("first_date")
    last_date = request.args.get("last_date")

    if comp_name != "all":
        if first_date and last_date:
            rows = get_company_content(comp_name, first_date, last_date)
        else:
            rows = get_company_content(comp_name)
    else:
        if first_date and last_date:
            rows = get_table_content(first_date, last_date)
        else:
            rows = get_table_content()

    return render_template(
        "index.html",
        names=names,
        rows=rows,
        comp_name=comp_name,
        first_date=first_date,
        last_date=last_date,
    )


@app.route("/upload", methods=["POST"])
def upload_data():
    name = request.form.get('manufacture')
    machine = request.files["machine"]
    volume = request.files["volume"]

    machine_filename = secure_filename(machine.filename)
    machine_path = UPLOAD_FOLDER / f"{machine_filename}"
    machine.save(machine_path)
    volume_filename = secure_filename(volume.filename)
    volume_path = UPLOAD_FOLDER / f"{volume_filename}"
    volume.save(volume_path)
    data_for_db = normalize_csv_data(volume_path, machine_path)
    write_data_to_db(data_for_db, name)
    return redirect(url_for("index"))


@app.route("/report", methods=["GET"])
def generate_report():
    comp_name = request.args.get("man", "all")
    first_date = request.args.get("first_date")
    last_date = request.args.get("last_date")

    if comp_name == "all":
        flash("Выберите отдельное хозяйство!")
        return redirect(url_for("index"))
    else:
        if first_date and last_date:
            data = get_company_content(comp_name, first_date, last_date)
            create_xlsx_report(data, comp_name, UPLOAD_FOLDER)
            return redirect(url_for("index"))
        elif not first_date or not last_date:
            flash("Неверно задан диапазон отображения записей!")
            return redirect(url_for("index"))
        else:
            data = get_company_content(comp_name)
            create_xlsx_report(data, comp_name, UPLOAD_FOLDER)
            return redirect(url_for("index"))
