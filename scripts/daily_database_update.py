import sqlite3
from transfer_data import *

def database_pipeline():
    connection = sqlite3.connect("./baseData/allPlayerStats.db")

    cursor = connection.cursor()

    # See this for various ways to import CSV into sqlite using Python. Pandas used here because files are not prohibitively large.
    # https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python

    # Decide whether to have user pick path or just set it automatically...
    for fileName in pick_path():
        if fileName.endswith('.csv'): #Avoid any accidents
            df = pd.read_csv(fileName)
            df.to_sql(fileName.replace(".csv", ""), connection, if_exists='replace', index=False)


    # Drop old tables
    sql_file = open("./scripts/SQL/drop_old_tables.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)

    # Make changes to tables
    sql_file = open("./scripts/SQL/prep_tables_for_extraction.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)

    # Extract this season's qualified players
    sql_file = open("./scripts/SQL/players2022_dbeaver.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)




def main():
    database_pipeline()

if __name__ == '__main__':
    main()