# ProjGen: The Project Manager Forcing You To Make Cool Stuff
As I want to make cool projects, but never finish them, I've made
this program. Every 30 days a new project will be generated, and you
get 30 days to build that.

## Getting Started
```bash
pip install projgen
python3 -m projgen new-db
python3 -m projgen show-database
python3 -m projgen status
```

## Adding things to the database
```bash
python3 -m projgen add-db-item "type" "Cli Tool"
python3 -m projgen add-db-requirement "type" "Cli Tool" "cliToolAction"
python3 -m projgen add-db-item "cliToolAction" "Git Info Viewer"
python3 -m projgen add-db-item "cliToolAction" "Project Manager Forcing You To Make Cool Stuff"
```