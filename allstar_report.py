import pandas as pd
from datetime import datetime
from utils.team_mapping import conference_to_teams

curr_dt = datetime.now().strftime("%Y-%m-%d")
curr_dt_no_delim = curr_dt.replace("-", "")

MIN_POS = {
    "frontcourt": 6,
    "backcourt": 4,
}

MAX_POS = {
    "frontcourt": 8,
    "backcourt": 6,
}

TOTAL_PER_TEAM = 12

EXTRA_FOR_INJURY = 3


def generate_report():
    df_modeled = pd.read_csv(
        rf".\data\dailystats\{curr_dt}\stats_{curr_dt_no_delim}_modeled.csv",
    )
    df_genstat = pd.read_csv(
        rf".\data\dailystats\{curr_dt}\totals_{curr_dt_no_delim}.csv",
    )
    player_to_team = dict(zip(df_genstat["Player"], df_genstat["Tm"]))
    player_to_position = dict(zip(df_genstat["Player"], df_genstat["Pos"]))

    teams = [player_to_team[player] for player in df_modeled["Player"]]
    positions = [player_to_position[player] for player in df_modeled["Player"]]

    team_to_conference = {
        team: conference
        for conference, team_list in conference_to_teams.items()
        for team in team_list
    }
    conferences = [team_to_conference[team] for team in teams]

    frontcourt_backcourt = {
        "frontcourt": ["SF", "PF", "C"],
        "backcourt": ["PG", "SG"],
    }

    pos_to_frontback = {
        pos: frontback
        for frontback, position_list in frontcourt_backcourt.items()
        for pos in position_list
    }

    front_back = [pos_to_frontback[pos] for pos in positions]

    df_modeled.insert(2, "Conf", conferences)
    df_modeled.insert(3, "FrontBack", front_back)

    make_teams(df_modeled)


def make_teams(df: pd.DataFrame):
    teams = {
        "east": {"backcourt": [], "frontcourt": []},
        "west": {"backcourt": [], "frontcourt": []},
    }

    injury_replacements = {
        "east": {"backcourt": [], "frontcourt": []},
        "west": {"backcourt": [], "frontcourt": []},
    }

    allstar_dict = df.to_dict(orient="records")

    team_size = {"east": 0, "west": 0}
    replacement_count = {"east": 0, "west": 0}
    for player in allstar_dict:
        for conference in ["east", "west"]:
            team_size[conference] = len(
                teams[conference]["frontcourt"],
            ) + len(teams[conference]["backcourt"])
            replacement_count[conference] = len(
                injury_replacements[conference]["frontcourt"],
            ) + len(injury_replacements[conference]["backcourt"])

        if (team_size["west"] + replacement_count["west"]) == (
            TOTAL_PER_TEAM + EXTRA_FOR_INJURY
        ) and (team_size["east"] + replacement_count["east"]) == (
            TOTAL_PER_TEAM + EXTRA_FOR_INJURY
        ):
            break
        name = player["Player"]
        conference = player["Conf"]
        frontback = player["FrontBack"]
        avg = player["Avg"]
        if (
            len(teams[conference]["frontcourt"]) + len(teams[conference]["backcourt"])
            < TOTAL_PER_TEAM
            and len(teams[conference][frontback]) < MAX_POS[frontback]
        ):
            teams[conference][frontback].append((name, avg))
        elif len(injury_replacements[conference]["frontcourt"]) + len(
            injury_replacements[conference]["backcourt"]
        ) < (EXTRA_FOR_INJURY):
            injury_replacements[conference][frontback].append((name, avg))

    print("All-Star Teams:", teams)
    print("Injury Replacements:", injury_replacements)


if __name__ == "__main__":
    generate_report()
