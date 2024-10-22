#    <one line to give the program's name and a brief idea of what it does.>  
#    Copyright © 2024 Charudatta
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#    email contact: 152109007c@gmailcom

set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]

env_path := "C:/Users/$env:username/Documents/GitHub"

default:
    @just --choose

# create files and directories
project-init:
    #!pwsh
    New-Project.ps1

# add documentation to repo
docs-init:
    #!pwsh
    conda activate blog
    python -m mkdocs new .

# generate and readme to repo    
project-readme:
    #!pwsh
    conda activate w
    python {{env_path}}/readmeGen/main.py

# version control repo with git
project-commit message="init":
    #!pwsh
    git add .
    git commit -m {{message}}

# create windows executable
project-exe file_name:
    #!pwsh
    pyinstaller src/{{file_name}} --onefile

# run python unit test 
code-tests:
    #!pwsh
    conda activate webdev
    python -m unittest discover -s tests

# run project
project-run:
    #!pwsh
    python run.py

# exit just file
quit:
    #!pwsh
    write-Host "Copyright © 2024 Charudatta"
    
# install dependencies
project-install:
    #!pwsh
    pip install -r requirements.txt

# lint code
code-lint:
    #!pwsh
    pylint src/
    flake8 src/

# format code
code-format:
    #!pwsh
    black src/

# run security checks
code-security:
    #!pwsh
    bandit -r src/

# build documentation
docs-build:
    #!pwsh
    mkdocs build

# deploy application
project-deploy:
    #!pwsh
    git pull origin main --force
    @test 
    @security
    @lint
    @format
    @commit
    git push -u origin main

# setup logging
log-init:
    #!pwsh
    Add-Logger.ps1

# view logs
log-view:
    #!pwsh
    Get-Content -Path ".log" -Tail 10

# clean up
build-clean:
    #!pwsh
    Remove-Item -Recurse -Force dist, build, *.egg-info

# check for updates
project-update:
    #!pwsh
    pip list --outdated

# project mangement add task and todos 
cicd-todos:
    #!pwsh
    wic

cicd-timeit cmd="start":
    #!pwsh
    timetrace {{cmd}} # start, stop, list

# Add custom tasks, enviroment variables

code-compile:
    #!pwsh
    conda activate w
    python src/main.py
    Copy-Item  -Path src/static -Destination src/site/ -Recurse -force

#run:
#    #!pwsh
#    conda activate w
#    python src/main.py



        

