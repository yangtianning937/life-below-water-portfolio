from utils.csv_utils import read_csv


def get_mapping():
    return read_csv("data/fish_names.csv")
