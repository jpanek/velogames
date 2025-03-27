from velogames import get_teams, save_team_text, save_team_html
from organize import generate_directory_html, generate_directory
from datetime import datetime

#supersixies:
torino = {
    "name":"Supersixies",
    "league_id":61627774,
    "stage":"Milano-Torino",
    "stage_id":5,
    "url":"https://www.velogames.com/sixes-superclasico/2025/leaguescores.php?league={league_id}&ga=13&st={stage_id}",
    "team_url":"https://www.velogames.com/sixes-superclasico/2025/teamroster.php?tid={team_id}&ga=13&st={stage_id}"
}

msr = {
    "name":"Supersixies",
    "league_id":61627774,
    "stage":"MSR",
    "stage_id":6,
    "url":"https://www.velogames.com/sixes-superclasico/2025/leaguescores.php?league={league_id}&ga=13&st={stage_id}",
    "team_url":"https://www.velogames.com/sixes-superclasico/2025/teamroster.php?tid={team_id}&ga=13&st={stage_id}"
}   

bruge = {
    "name":"Supersixies",
    "league_id":61627774,
    "stage":"Brugge-De-Panne",
    "stage_id":7,
    "race_date":"2025-03-27",
    "url":"https://www.velogames.com/sixes-superclasico/2025/leaguescores.php?league={league_id}&ga=13&st={stage_id}",
    "team_url":"https://www.velogames.com/sixes-superclasico/2025/teamroster.php?tid={team_id}&ga=13&st={stage_id}"
}

#catalunya
catalunya = {
    "name":"Stage-races",
    "league_id":61627774,
    "stage": "Catalunya",
    "stage_id": 7,
    "url": "https://www.velogames.com/catalunya/2025/leaguescores.php?league={league_id}",
    "team_url":"https://www.velogames.com/catalunya/2025/teamroster.php?tid={team_id}"
}

e3 = {
    "name":"Supersixies",
    "league_id":61627774,
    "stage":"E3",
    "stage_id":8,
    "race_date":"2025-03-28",
    "url":"https://www.velogames.com/sixes-superclasico/2025/leaguescores.php?league={league_id}&ga=13&st={stage_id}",
    "team_url":"https://www.velogames.com/sixes-superclasico/2025/teamroster.php?tid={team_id}&ga=13&st={stage_id}"
}

gent = {
    "name":"Supersixies",
    "league_id":61627774,
    "stage":"Gent-Wevelgem",
    "stage_id":9,
    "race_date":"2025-03-30",
    "url":"https://www.velogames.com/sixes-superclasico/2025/leaguescores.php?league={league_id}&ga=13&st={stage_id}",
    "team_url":"https://www.velogames.com/sixes-superclasico/2025/teamroster.php?tid={team_id}&ga=13&st={stage_id}"
}

dwars = {
    "name":"Supersixies",
    "league_id":61627774,
    "stage":"Dwars-door-Vlaanderen",
    "stage_id":10,
    "race_date":"2025-04-04",
    "url":"https://www.velogames.com/sixes-superclasico/2025/leaguescores.php?league={league_id}&ga=13&st={stage_id}",
    "team_url":"https://www.velogames.com/sixes-superclasico/2025/teamroster.php?tid={team_id}&ga=13&st={stage_id}"
}

rvv = {
    "name":"Supersixies",
    "league_id":61627774,
    "stage":"RVV",
    "stage_id":11,
    "race_date":"2025-04-06",
    "url":"https://www.velogames.com/sixes-superclasico/2025/leaguescores.php?league={league_id}&ga=13&st={stage_id}",
    "team_url":"https://www.velogames.com/sixes-superclasico/2025/teamroster.php?tid={team_id}&ga=13&st={stage_id}"
}

scheldeprijs = {
    "name":"Supersixies",
    "league_id":61627774,
    "stage":"Scheldeprijs",
    "stage_id":12,
    "race_date":"2025-04-09",
    "url":"https://www.velogames.com/sixes-superclasico/2025/leaguescores.php?league={league_id}&ga=13&st={stage_id}",
    "team_url":"https://www.velogames.com/sixes-superclasico/2025/teamroster.php?tid={team_id}&ga=13&st={stage_id}"
}

roubaix = {
    "name":"Supersixies",
    "league_id":61627774,
    "stage":"Roubaix",
    "stage_id":13,
    "race_date":"2025-04-13",
    "url":"https://www.velogames.com/sixes-superclasico/2025/leaguescores.php?league={league_id}&ga=13&st={stage_id}",
    "team_url":"https://www.velogames.com/sixes-superclasico/2025/teamroster.php?tid={team_id}&ga=13&st={stage_id}"
}



races = [torino, msr, bruge, e3, catalunya]
races = [bruge,e3, gent, dwars, scheldeprijs, roubaix]

today = datetime.today().date()

for race in races:
    if datetime.strptime(race["race_date"], "%Y-%m-%d").date() == today:
        teams = get_teams(race)
        save_team_text(teams, race)
        save_team_html(teams,race)

generate_directory_html('race_data','index.html')
