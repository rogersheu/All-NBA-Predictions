import csv
import os


def write_to_csv(file_name, list_input):
    try:
        # Open the csv.
        with open(file_name, "a", newline="", encoding="utf-8") as fopen:
            csv_writer = csv.writer(fopen)
            csv_writer.writerow(list_input)

    except FileNotFoundError:
        pass


def reset_csv(file_name):
    try:
        with open(file_name, "r+", encoding="utf-8") as f:
            f.truncate(0)  # need '0' when using r+

    except FileNotFoundError:
        pass


def make_dir_if_nonexistent(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
