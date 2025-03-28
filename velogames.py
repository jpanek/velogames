import requests
from bs4 import BeautifulSoup
import csv
import os
import json

def construct_url(url_raw, league):
    return url_raw.format(**league)

def construct_filename(league, suffix=""):
    name = league["name"]
    stage = league.get("stage", "")  # Get stage if it exists, otherwise empty string
    stage_id = league.get("stage_id","")

    # Format stage_id as two digits, if it's a number
    if stage_id:
        stage_id = f"{int(stage_id):02d}"  # Ensure it is always two digits

    filename = f"{name}_{stage}{suffix}.csv" if stage else f"{name}{suffix}.csv"
    #filename = f"{stage_id}_{stage}{suffix}.csv" if stage and stage_id else f"{name}{suffix}.csv"
    directory = os.path.join("race_data", name, str(stage_id)+"_"+stage) if stage and stage_id else os.path.join("race_data", name)
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, filename)

def get_teams(race):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # Ensure URL construction is consistent
    if "stage_id" in race:
        url = race["url"].format(league_id=race["league_id"], stage_id=race["stage_id"])
    else:
        url = race["url"].format(league_id=race["league_id"])

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
            
        #print(f"Data saved to {filename}")


    full_team = get_cyclists(race,data)    
    
    return full_team

def get_cyclists(race, teams):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    all_cyclists = []
    pts = 0
    
    for tid, team_name, manager in teams:
        # Adjust URL construction based on whether stage_id exists
        if "stage_id" in race:
            url = race["team_url"].format(team_id=tid, stage_id=race["stage_id"])
        else:
            url = race["team_url"].format(team_id=tid)

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        for td in soup.select("table.team-info-panel td"):
            text = td.get_text(separator="\n").strip().split("\n")
            if len(text) == 2:
                rider, points = text
                points = points.replace(" pts", "").strip()
                pts += int(points)
                all_cyclists.append([tid, team_name, manager, rider, points])
    
    filename = construct_filename(race, "_teams")
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["TID", "Team Name", "Manager", "Rider", "Points"])
        writer.writerows(all_cyclists)
    
    #print(f"Data saved to {filename}")
    if pts > 0:
        results = True
    else: results = False
    return all_cyclists, results



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
    
    #print(f"Team list saved to {filename}")

def save_team_html(full_team, race):
    team_dict = {}
    team_names = {}

    # Organize data
    for tid, team_name, manager, rider, points in full_team:
        if manager not in team_dict:
            team_dict[manager] = []
            team_names[manager] = team_name
        team_dict[manager].append(rider)

    max_riders = max(len(riders) for riders in team_dict.values()) if team_dict else 0

    # Sort the managers alphabetically
    sorted_managers = sorted(team_dict.keys())

    # Generate Bootstrap table HTML

    if max_riders == 0:
        table_html = '<div class="alert alert-warning text-center" role="alert">Not available yet</div>'
    else:
        table_html = "<thead><tr>"
        table_html += "".join(f"<th>{manager}</th>" for manager in sorted_managers) + "</tr></thead>\n"
        table_html += "<tbody><tr>" + "".join(f"<th>{team_names[manager]}</th>" for manager in sorted_managers) + "</tr>\n"

        for i in range(max_riders):
            table_html += "<tr>"
            for manager in sorted_managers:
                rider = team_dict[manager][i] if i < len(team_dict[manager]) else ""
                table_html += f"<td>{rider}</td>"
            table_html += "</tr>\n"
        
        table_html += "</tbody>"

    # Read template and insert table
    with open("/Users/jurajpanek/Documents/code/velogames/templates/template.html", "r", encoding="utf-8") as f:
        template_html = f.read()

    header = race['name']  # Start with the name

    # Check if stage_id and stage exist and append them if they do
    if race.get('stage_id') and race.get('stage'):
        header += f" - {race['stage_id']} - {race['stage']}"
    elif race.get('stage_id'):  # Include only stage_id if it exists
        header += f" - {race['stage_id']}"
    elif race.get('stage'):  # Include only stage if it exists
        header += f" - {race['stage']}"
    template_html = template_html.replace("<!-- HEADER GOES HERE -->", header)
    final_html = template_html.replace("<!-- TABLE GOES HERE -->", table_html)

    # Construct filename
    filename = construct_filename(race, "_teams").replace(".csv", ".html")

    # Save to file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_html)
    
    print(f"Team composition saved to {filename}")


def generate_html(full_team, race):
    team_dict = {}
    team_names = {}

    # Organize data
    for tid, team_name, manager, rider, points in full_team:
        if manager not in team_dict:
            team_dict[manager] = []
            team_names[manager] = team_name
        team_dict[manager].append((rider, points))

    max_riders = max(len(riders) for riders in team_dict.values()) if team_dict else 0

    # Sort managers alphabetically
    sorted_managers = sorted(team_dict.keys())

    # Generate Table HTML
    if max_riders == 0:
        table_html = '<div class="alert alert-warning text-center" role="alert">Not available yet</div>'
    else:
        table_html = "<thead><tr>"
        table_html += "".join(f"<th>{manager}</th>" for manager in sorted_managers) + "</tr></thead>\n"
        table_html += "<tbody><tr>" + "".join(f"<th>{team_names[manager]}</th>" for manager in sorted_managers) + "</tr>\n"

        for i in range(max_riders):
            table_html += "<tr>"
            for manager in sorted_managers:
                rider_info = team_dict[manager][i] if i < len(team_dict[manager]) else ("", "")
                rider, points = rider_info
                table_html += f"<td>{rider} ({points})</td>" if rider else "<td></td>"
            table_html += "</tr>\n"

        table_html += "</tbody>"

    # Prepare Chart.js Data
    labels = sorted_managers
    datasets = []
    
    # Create dataset for each rider
    rider_point_dict = {}
    for manager, riders in team_dict.items():
        for i, (rider, points) in enumerate(riders):
            if rider not in rider_point_dict:
                rider_point_dict[rider] = [0] * len(sorted_managers)
            rider_point_dict[rider][sorted_managers.index(manager)] = points

    for rider, points in rider_point_dict.items():
        datasets.append({
            "label": rider,
            "data": points,
            "backgroundColor": f"rgba({(hash(rider) % 256)}, {(hash(rider) // 256 % 256)}, {(hash(rider) // 65536 % 256)}, 0.7)"
        })

    chart_data = {
        "labels": labels,
        "datasets": datasets
    }

    chart_data_json = json.dumps(chart_data)

    # Read template and insert content
    with open("/Users/jurajpanek/Documents/code/velogames/templates/results.html", "r", encoding="utf-8") as f:
        template_html = f.read()

    header = race['name']
    if race.get('stage_id') and race.get('stage'):
        header += f" - {race['stage_id']} - {race['stage']}"
    elif race.get('stage_id'):
        header += f" - {race['stage_id']}"
    elif race.get('stage'):
        header += f" - {race['stage']}"

    template_html = template_html.replace("<!-- HEADER GOES HERE -->", header)
    template_html = template_html.replace("<!-- CHART DATA GOES HERE -->", chart_data_json)
    final_html = template_html.replace("<!-- TABLE GOES HERE -->", table_html)

    # Save to file
    filename = construct_filename(race, "_results").replace(".csv", ".html")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Race results published to {filename}")
