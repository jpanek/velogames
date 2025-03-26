from velogames import get_teams, get_cyclists, save_team_text

#supersixies:
sixies = {
    "name":"Supersixies",
    "league_id":61627774,
    "stage":"MSR",
    "stage_id":6,
    "url":"https://www.velogames.com/sixes-superclasico/2025/leaguescores.php?league={league_id}&ga=13&st={stage_id}",
    "team_url":"https://www.velogames.com/sixes-superclasico/2025/teamroster.php?tid={team_id}"
}   

bruge = {
    "name":"Supersixies",
    "league_id":61627774,
    "stage":"BruggeDePann",
    "stage_id":7,
    "url":"https://www.velogames.com/sixes-superclasico/2025/leaguescores.php?league={league_id}&ga=13&st={stage_id}",
    "team_url":"https://www.velogames.com/sixes-superclasico/2025/teamroster.php?tid={team_id}"
}

#catalunya
catalunya = {
    "name":"Catalunya",
    "league_id":61627774,
    "url": "https://www.velogames.com/catalunya/2025/leaguescores.php?league={league_id}",
    "team_url":"https://www.velogames.com/catalunya/2025/teamroster.php?tid={team_id}"
}

race = bruge

teams = get_teams(race)
save_team_text(teams, race)