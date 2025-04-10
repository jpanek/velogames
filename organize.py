import os
from datetime import datetime
import pytz


def generate_directory_html(directory, output_file):
    # Create a header for the HTML page with Bootstrap
    html = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MFCC</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            ul { list-style-type: none; padding-left: 20px; }
            li { margin: 5px 0; }
        </style>
    </head>
    <body>"""

    # Define Jakarta timezone
    jakarta_tz = pytz.timezone('Asia/Jakarta')

    # Get the current time in UTC and convert to Jakarta time
    jakarta_time = datetime.now(jakarta_tz)

    # Format the datetime as needed
    jkt_time = jakarta_time.strftime("%d %B %H:%M")


    # Get the current datetime
    now = datetime.now()
    # Format the datetime
    formatted_datetime = now.strftime("%d %B %H:%M")
    html += f"""
    <div class="alert alert-info text-center" role="alert">
        Updated {formatted_datetime} CET ({jkt_time} Jakarta time for kampung MFers)
    </div>
    """

    html += """
        <div class="container">
            <h1 class="my-4">Velogames MFCC teams</h1>
            <ul class="list-group">
    """

    # Walk through the directory and create a dictionary to group files by race name
    race_dirs = {}

    for root, dirs, files in os.walk(directory):
        files.sort()
        # Filter out non-HTML files
        html_files = [file for file in files if file.endswith(".html")]

        if html_files:
            # Extract the race name from the directory structure
            path_parts = os.path.relpath(root, directory).split(os.sep)
            race_name = path_parts[0]

            if race_name not in race_dirs:
                race_dirs[race_name] = {}

            if len(path_parts) > 1:
                subdir_name = path_parts[1]
                if subdir_name not in race_dirs[race_name]:
                    race_dirs[race_name][subdir_name] = []
                race_dirs[race_name][subdir_name].extend(html_files)
            else:
                race_dirs[race_name] = html_files

    # For each race, generate the nested HTML structure
    for race_name, subdirs in race_dirs.items():
        html += f'        <li class="list-group-item list-group-item-primary">{race_name}\n'
        html += "            <ul class=\"list-group ms-3\">\n"
        
        if isinstance(subdirs, dict):  # If there are subdirectories
            # Sort the subdirectories alphabetically
            for subdir_name in sorted(subdirs.keys()):
                files = subdirs[subdir_name]
                html += f'                <li class="list-group-item list-group-item-secondary">{subdir_name}: '
                for file in sorted(files, reverse=True):
                    html += f'                        <a href="{os.path.join(directory, race_name, subdir_name, file)}">{get_file_name(file)}</a>\n'
                #html += f'                <li class="list-group-item list-group-item-secondary">{subdir_name}\n'
                #html += "                    <ul class=\"list-group ms-3\">\n"
                #for file in files:
                #    html += f'                        <li class="list-group-item"><a href="{os.path.join(directory, race_name, subdir_name, file)}">{file}</a></li>\n'
                #html += "                    </ul>\n"
                html += "                </li>\n"
        else:  # If there are no subdirectories
            for file in subdirs:
                html += f'            <li class="list-group-item"><a href="{os.path.join(directory, race_name, file)}">{get_file_name(file)}</a></li>\n'
        
        html += "            </ul>\n"
        html += "        </li>\n"

    # Close the HTML tags
    html += """    
        </ul>
    </div>
</body>
</html>"""

    # Write the generated HTML to a file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"HTML file has been generated and saved to {output_file}")


def generate_directory(directory, output_file):
    # Create a header for the HTML page with Bootstrap
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Race Data Directory</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        ul { list-style-type: none; padding-left: 20px; }
        li { margin: 5px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="my-4">Race Data Files</h1>
        <ul class="list-group">
"""

    # Walk through the directory and create a dictionary to group files by race name
    race_dirs = {}

    for root, dirs, files in os.walk(directory):
        # Filter out non-HTML files
        html_files = [file for file in files if file.endswith(".html")]

        if html_files:
            # Extract the race name from the directory structure
            path_parts = os.path.relpath(root, directory).split(os.sep)
            race_name = path_parts[0]

            if race_name not in race_dirs:
                race_dirs[race_name] = {}

            if len(path_parts) > 1:
                subdir_name = path_parts[1]
                if subdir_name not in race_dirs[race_name]:
                    race_dirs[race_name][subdir_name] = []
                race_dirs[race_name][subdir_name].extend(html_files)
            else:
                race_dirs[race_name] = html_files

    # For each race, generate the nested HTML structure
    for race_name, subdirs in sorted(race_dirs.items()):
        html += f'        <li class="list-group-item list-group-item-primary">{race_name}\n'
        html += "            <ul class=\"list-group ms-3\">\n"
        
        if isinstance(subdirs, dict):  # If there are subdirectories
            # Sort the subdirectories alphabetically
            for subdir_name in sorted(subdirs.keys()):
                files = subdirs[subdir_name]
                html += f'                <li class="list-group-item list-group-item-secondary">{subdir_name}\n'
                html += "                    <ul class=\"list-group ms-3\">\n"
                for file in sorted(files):
                    html += f'                        <li class="list-group-item"><a href="{os.path.join(directory, race_name, subdir_name, file)}">{get_file_name(file)}</a></li>\n'
                html += "                    </ul>\n"
                html += "                </li>\n"
        else:  # If there are no subdirectories
            for file in sorted(subdirs):
                html += f'            <li class="list-group-item"><a href="{os.path.join(directory, race_name, file)}">{get_file_name(file)}" </a></li>\n'
        
        html += "            </ul>\n"
        html += "        </li>\n"

    # Close the HTML tags
    html += """    
        </ul>
    </div>
</body>
</html>"""

    # Write the generated HTML to a file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"HTML file has been generated and saved to {output_file}")


def get_file_name(file):
    if "teams" in file:
        file_name = "Teams"
    elif "results" in file:
        file_name = "Results"
    else:
        file_name = file
    return file_name