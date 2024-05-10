# ProjGen: The Project Manager Forcing You To Make Cool Stuff
As I want to make cool projects, but never finish them, I've made
this program. Every 30 days a new project will be generated, and you
get 30 days to build that.

## Getting Started
```bash
pip install projgen
projgen new-db
projgen show-database
projgen status
```

## Adding things to the database
```bash
projgen add-db-item "type" "Cli Tool"
projgen add-db-requirement "type" "Cli Tool" "cliToolAction"
projgen add-db-item "cliToolAction" "Git Info Viewer"
projgen add-db-item "cliToolAction" "Project Manager Forcing You To Make Cool Stuff"
```

## Getting a project
During the thirty days, you can't get a new project. Once these 30 days are over, 
you can get a new project by running
```bash
projgen update
```