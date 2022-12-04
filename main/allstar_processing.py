import re

import pandas as pd

from utils.csv_functions import write_to_csv


# Looks for 2019-2020, for example.
yearPattern = re.compile(r'^([0-9]{4})-?([0-9]{4})?$')
fileName = 'allstar_full.csv'


def process_allstars():
    df = pd.read_csv(
        r'.\baseData\allstar_raw.csv',
        delimiter=',', engine='python', encoding='utf-8',
    )

    for row in range(len(df)):
        yearsRaw = str(df.iloc[row][1])
        yearsSplit = yearsRaw.split(';')
        fullListofYears = []

        for element in yearsSplit:
            match = re.match(yearPattern, element)
            startYear = match.group(1) if match else None
            endYear = match.group(2) if match else None

            if endYear is None:
                fullListofYears.append(startYear)
                write_to_csv(fileName, [df.iloc[row][0], startYear])
            else:
                for year in range(int(startYear), int(endYear) + 1):
                    fullListofYears.append(str(year))
                    write_to_csv(fileName, [df.iloc[row][0], year])

        df.iat[row, 1] = fullListofYears

    print(df)


def main():
    process_allstars()


if __name__ == '__main__':
    main()
