import typer
import os
import json
from rich import print
from rich.panel import Panel
import copy
import datetime
import random

PROJECT_DESCRIPTION = \
"""Your current project started at [red]{start}[/red] and ends at [red]{end}[/red].
Project specifics:{specs}"""

app = typer.Typer()

def get_specific(specific: str, db: dict):
    return random.choice(list(db['database'][specific].keys()))

@app.command()
def status():
    assert os.path.exists("./projgen.json")
    with open("./projgen.json", "r") as f:
        data = json.loads(f.read())
    specs = ""
    for key, value in data['currentProject']['specifics'].items():
        specs += f"\n·\t{key}: {value}"
    print(Panel(PROJECT_DESCRIPTION.format(start=data['currentProject']['start'], end=data['currentProject']['end'], specs=specs), title="Current Project", style="white"))

@app.command()
def new_project():
    assert os.path.exists("./projgen.json")
    with open("./projgen.json", "r") as f:
        data = json.loads(f.read())
    new = copy.deepcopy(data)
    new['pastProjects'].append(data['currentProject'])
    new['currentProject'] = {}
    new['currentProject']['start'] = str(datetime.datetime.now())
    new['currentProject']['end'] = str(datetime.datetime.now() + datetime.timedelta(days=30))
    new['currentProject']['specifics'] = {}
    todo = ['type']
    for t in todo:
        new['currentProject']['specifics'][t] = get_specific(t, data)
        todo += data['database'][t][new['currentProject']['specifics'][t]]
    with open("./projgen.json", "w") as f:
        f.write(json.dumps(new, indent=4))
    status()

@app.command()
def update():
    assert os.path.exists("./projgen.json")
    with open("./projgen.json", "r") as f:
        data = json.loads(f.read())
    if datetime.datetime.fromisoformat(data['currentProject']['end']) < datetime.datetime.now():
        print("Project finished.")
        new_project()
    else:
        print("Project not yet finished.")
        status()

@app.command()
def add_db_item(specific: str, item: str):
    assert os.path.exists("./projgen.json")
    with open("./projgen.json", "r") as f:
        data = json.loads(f.read())
    if specific not in data['database']:
        data['database'][specific] = {}
    data['database'][specific][item] = []
    with open("./projgen.json", "w") as f:
        f.write(json.dumps(data, indent=4))

@app.command()
def add_db_requirement(specific: str, item: str, requirement: str):
    assert os.path.exists("./projgen.json")
    with open("./projgen.json", "r") as f:
        data = json.loads(f.read())
    if specific not in data['database']:
        data['database'][specific] = {}
    if item not in data['database'][specific]:
        data['database'][specific][item] = []
    data['database'][specific][item].append(requirement)
    with open("./projgen.json", "w") as f:
        f.write(json.dumps(data, indent=4))

@app.command()
def show_database():
    assert os.path.exists("./projgen.json")
    with open("./projgen.json", "r") as f:
        data = json.loads(f.read())
    for key, value in data['database'].items():
        print(f"[bold]{key}[/bold]:")
        for k, v in value.items():
            print(f"·\t{k}: {v}")

def main():
    app()

if __name__ == '__main__':
    main()