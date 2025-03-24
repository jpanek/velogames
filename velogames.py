import requests
from bs4 import BeautifulSoup
import csv
import os

def construct_url(url_raw, league):
    return url_raw.format(**league)

def construct_filename(league, suffix=""):
    name = league["name"]
    stage = league.get("stage", "")  # Get stage if it exists, otherwise empty string
    filename = f"{name}_{stage}{suffix}.csv" if stage else f"{name}{suffix}.csv"
    directory = os.path.join("race_data", name, stage) if stage else os.path.join("race_data", name)
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, filename)

def get_teams(race):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    url = construct_url(race["url"], race)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    data = []
    
    for link in soup.find_all("a", href=True):
        if "teamroster.php?tid=" in link["href"]:
            tid = link["href"].split("tid=")[1]
            team_name = link.text.strip()
            
            p_tag = link.find_next("p", class_="born")
            name = p_tag.text.strip() if p_tag else "Unknown"
            
            data.append([tid, team_name, name])

    if 0:
        filename = construct_filename(race)
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["TID", "Team Name", "Name"])
            writer.writerows(data)
            
        print(f"Data saved to {filename}")


    full_team = get_cyclists(race,data)    
    
    return full_team

def get_cyclists(race, teams):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    all_cyclists = []
    
    for tid, team_name, manager in teams:
        url = race["team_url"].format(team_id=tid)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        for td in soup.select("table.team-info-panel td"):
            text = td.get_text(separator="\n").strip().split("\n")
            if len(text) == 2:
                rider, points = text
                points = points.replace(" pts", "").strip()
                all_cyclists.append([tid, team_name, manager, rider, points])
    
    filename = construct_filename(race, "_teams")
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["TID", "Team Name", "Manager", "Rider", "Points"])
        writer.writerows(all_cyclists)
    
    print(f"Data saved to {filename}")
    return all_cyclists

def save_team_text(full_team, race):
    team_dict = {}
    for tid, team_name, manager, rider, points in full_team:
        if manager not in team_dict:
            team_dict[manager] = []
        team_dict[manager].append(rider)
    
    filename = construct_filename(race, "_teams")
    filename = filename.replace(".csv", ".txt")
    
    with open(filename, "w", encoding="utf-8") as f:
        for manager, riders in team_dict.items():
            f.write(f"{manager}: {', '.join(riders)}\n")
    
    print(f"Team list saved to {filename}")
