import csv
import json
import os


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as csvfile:
        data = list(csv.DictReader(csvfile))
        return data

def init_csv(filename, header):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)

def write_csv(filename, data: list[dict]):
    # Collect all keys
    fieldnames = set()
    for row in data:
        fieldnames.update(row.keys())
    fieldnames = list(fieldnames)

    file_exists = os.path.isfile(filename)

    with open(filename, "a", encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(data)

def csv_to_json(filename):
    data = read_csv(filename)
    return json.loads(json.dumps(data))

def json_to_csv(filename, data):
    write_csv(filename, data)


# def test():
#     data = [
#         {"name": "Alice", "age": 25},
#         {"name": "Bob", "city": "Sydney"},
#         {"age": 30, "city": "Melbourne"}
#     ]
#
#     write_csv("data/form.csv", data)
#
# test()
