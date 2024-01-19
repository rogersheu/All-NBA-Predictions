import sqlite3
import os
import os.path as osp

import pandas as pd

from utils.transfer_data import pick_path
from utils.vars import curr_season_str


def database_pipeline(path):
    connection = sqlite3.connect("./data/allPlayerStats.db")

    cursor = connection.cursor()

    # See this for various ways to import CSV into sqlite using Python. Pandas used here because files are not prohibitively large.
    # https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python

    print("SQL scripts starting...")
    # Drop old tables, might not be necessary since we're dropping them
    with open("./SQL/drop_old_tables.sql", encoding="utf-8") as f:
        try:
            sql_as_string = f.read()
            cursor.executescript(sql_as_string)
        except Exception:
            pass

    # Decide whether to have user pick path or just set it automatically...
    for file_name in os.listdir(path):
        if file_name.endswith(".csv"):  # Avoid any accidents
            df = pd.read_csv(osp.join(path, file_name))
            df.to_sql(
                f'{file_name.replace(".csv","").split("_")[0]}',
                connection,
                if_exists="replace",
                index=False,
            )
            try:
                date = f'{file_name.replace(".csv","").split("_")[1]}'
            except Exception:
                pass

    # Make changes to tables
    with open("./SQL/prep_tables_for_extraction.sql", encoding="utf-8") as f:
        try:
            sql_as_string = f.read()
            cursor.executescript(sql_as_string)
        except Exception as e:
            raise e

    # Extract this season's qualified players
    with open(f"./SQL/players{curr_season_str}_dbeaver.sql", encoding="utf-8") as f:
        df_output = pd.read_sql_query(f.read(), connection)
    print(df_output)
    df_output.to_csv(f"{path}/stats_{date}.csv", index=False)

    print("SQL scripts complete.")


if __name__ == "__main__":
    data_path = pick_path()
    database_pipeline(data_path)
