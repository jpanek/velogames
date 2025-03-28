from velogames import get_teams, save_team_text, save_team_html, generate_html
from organize import generate_directory_html, generate_directory
from datetime import datetime


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


races = [e3]

for race in races:
    teams = get_teams(race)
    save_team_text(teams, race)
    #save_team_html(teams,race)
    #generate_html(teams,race)

generate_directory_html('race_data','index.html')
