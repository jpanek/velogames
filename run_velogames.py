from velogames import get_teams, save_team_text, save_team_html
from organize import generate_directory_html, generate_directory
import os 

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
    "url":"https://www.velogames.com/sixes-superclasico/2025/leaguescores.php?league={league_id}&ga=13&st={stage_id}",
    "team_url":"https://www.velogames.com/sixes-superclasico/2025/teamroster.php?tid={team_id}&ga=13&st={stage_id}"
}

gent = {
    "name":"Supersixies",
    "league_id":61627774,
    "stage":"Gent-Wevelgem",
    "stage_id":9,
    "url":"https://www.velogames.com/sixes-superclasico/2025/leaguescores.php?league={league_id}&ga=13&st={stage_id}",
    "team_url":"https://www.velogames.com/sixes-superclasico/2025/teamroster.php?tid={team_id}&ga=13&st={stage_id}"
}

races = [torino, msr, bruge, e3, catalunya]
races = [e3]

for race in races:
    teams = get_teams(race)
    save_team_text(teams, race)
    save_team_html(teams,race)

generate_directory_html('race_data','index.html')