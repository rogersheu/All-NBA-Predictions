import csv
import os

def write_to_csv(fileName, list_input):
    try:
        # Open the csv.
        with open(fileName, "a", newline="") as fopen:
            csv_writer = csv.writer(fopen)
            csv_writer.writerow(list_input)

    except FileNotFoundError:
        return False


def reset_csv(fileName):
    try:
        tobeDeleted = open(fileName, "r+")
        tobeDeleted.truncate(0)  # need '0' when using r+

    except FileNotFoundError:
        return False
