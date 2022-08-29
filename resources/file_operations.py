from copy import deepcopy
import csv
import pandas


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

    return sorted(result_data, key=lambda row: row["Дата"])


def normalize_db_table_name(db_name: list):
    rel = {
        "asgard": "Асгард",
        "midgard": "Мидгард",
        "yotunhame": "Йотунхейм",
    }
    names = [
        (k, v) for k, v in rel.items() for item in db_name if k in item[0]
    ]
    return names


def create_xlsx_report(raw_data: list, name: str):
    data = {
        "Дата": [],
        "Техника": [],
        "Номер техники": [],
        "Площадь, га": [],
        "Объем работ, м3": [],
    }
    for item in raw_data:
        data["Дата"].append(item[0])
        data["Техника"].append(item[1])
        data["Номер техники"].append(item[2])
        data["Площадь, га"].append(item[3])
        data["Объем работ, м3"].append(item[4])
    xlsx = pandas.DataFrame(data)
    xlsx.to_excel(f"/home/alekseyf/task_from_rmk/{name}.xlsx", index=False)
