import csv
import json


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as csvfile:
        data = list(csv.DictReader(csvfile))
        return data


def csv_to_json(filename):
    data = read_csv(filename)
    return json.loads(json.dumps(data))


# def test():
#     print(csv_to_json("data/Site Metadata.csv"))
#
# test()
