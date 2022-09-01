from copy import deepcopy
import csv
import pandas


# Work with CSV and XLS files
def get_csv_data(file_path) -> iter:
    with open(file_path, encoding="utf-8-sig") as content:
        return list(csv.DictReader(content))


def normalize_csv_data(volume_path, machine_path) -> list:
    volume_raw = get_csv_data(volume_path)
    machine_raw = get_csv_data(machine_path)
    result_data = deepcopy(machine_raw)
    for item in result_data:
        for i in range(len(machine_raw)):

            if item["Дата"] == volume_raw[i]["Дата"]:
                item.update(volume_raw[i])

    return sorted(result_data, key=lambda row: row["Дата"])


def normalize_names(raw_names: list) -> list:
    names = [item[0] for item in raw_names]
    return names


def create_xlsx_report(raw_data: list, name: str, folder):
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
    xlsx.to_excel(f"{folder}/{name}.xlsx", index=False)
