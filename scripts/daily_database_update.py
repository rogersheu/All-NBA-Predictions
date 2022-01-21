import sqlite3
from transfer_data import *
from os import listdir

def database_pipeline(path):
    connection = sqlite3.connect("./baseData/allPlayerStats.db")

    cursor = connection.cursor()

    # See this for various ways to import CSV into sqlite using Python. Pandas used here because files are not prohibitively large.
    # https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python

    print("SQL scripts starting...")
    # Drop old tables, might not be necessary since we're dropping them
    sql_file = open("./scripts/SQL/drop_old_tables.sql")
    try:
        sql_as_string = sql_file.read()
        cursor.executescript(sql_as_string)
        sql_file.close()
    except:
        pass

    # Decide whether to have user pick path or just set it automatically...
    for fileName in listdir(path):
        if fileName.endswith('.csv'): #Avoid any accidents
            df = pd.read_csv(f'{path}/{fileName}')
            df.to_sql(f'{fileName.replace(".csv","").split("_")[0]}', connection, if_exists='replace', index=False)
            try:
                date = f'{fileName.replace(".csv","").split("_")[1]}'
            except:
                pass

    # Make changes to tables
    sql_file = open("./scripts/SQL/prep_tables_for_extraction.sql")
    try:
        sql_as_string = sql_file.read()
        cursor.executescript(sql_as_string)
    except:
        pass

    sql_file.close()

    # Extract this season's qualified players
    sql_file = open("./scripts/SQL/players2022_dbeaver.sql")
    df_output = pd.read_sql_query(sql_file.read(),connection)
    sql_file.close()
    #sql_as_string = sql_file.read()
    #cursor.executescript(sql_as_string)
    print(df_output)
    df_output.to_csv(f'{path}/stats_{date}.csv', index = False)

    print("SQL scripts complete.")




def main():
    data_path = pick_path()
    database_pipeline(data_path)

if __name__ == '__main__':
    main()