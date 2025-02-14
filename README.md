# Globant's Coding Challenge - Data Engineer

## Coding challenge instructions

### Section 1: API

In the context of a DB migration with 3 different tables (departments, jobs, employees) , create a local REST API that must:

1. Receive historical data from CSV files
2. Upload these files to the new DB
3. Be able to insert batch transactions (1 up to 1000 rows) with one request

You need to publish your code in GitHub. It will be taken into account if frequent updates are made to the repository that allow analyzing the development process. Ideally, create a markdown file for the Readme.md

#### Clarifications

* You decide the origin where the CSV files are located.
* You decide the destination database type, but it must be a SQL database.
* The CSV file is comma separated.

### Section 2: SQL

You need to explore the data that was inserted in the previous section. The stakeholders ask for some specific metrics they need. You should create an end-point for each requirement.

#### Requirements

* Number of employees hired for each job and department in 2021 divided by quarter. The table must be ordered alphabetically by department and job.

Output example:

| department | job | Q1 | Q2 | Q3 | Q4 |
| ---------- | --- | -- | -- | -- | -- |
| Staff | Recruiter | 3 | 0 | 7 | 11 |
| Staff | Manager | 2 | 1 | 0 | 2 |
| Supply Chain | Manager | 0 | 1 | 3 | 0 |

* List of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments, ordered by the number of employees hired (descending).

Output example:

| id | department | hired |
| -- | ---------- | ----- |
| 7 | Staff | 45 |
| 9 | Supply Chain | 12 |

## Considerations, assumptions and rationale

* Python management is done with `uv`, which accounts for the high number of project files (`pyproject.toml`, `requirements.in` and `requirements.txt`)
* Certain basic automations are deployed using a `Makefile`. The recipes can be found on section [**Automations**](#automations)
* In regards of the API, all the relevant discussion can be found on the [backend README](app/backend/README.md) file.
* That being said, certain design and architecture decisions can be laid out here, in general terms:
    * The API is deployed using Python's FastAPI
    * Given that the location of the files is not declared on the requirement, the API allows for file uploads and filesystem load triggering
    * No DAG-based orchestrator is deployed for this solution, but a possible and follow-up enhancement would be to orchestrate the load process
* In regards of the SQL section, all relevant discussion can be found on the [functions README](app/backend/functions/README.md) file.
* As an addition to the developed REST API, a frontend webapp is deployed to enable better interactions with the API

## Repo structure

```text
app/                    :
|- backend/             :
    |- assets/          :
    |- db/              :
    |- functions/       :
    |- lib/             :
    |- output/          :
    |- utils/           :
    |- __init__.py      :
    |- .dockerignore    :
    |- Dockerfile       :
    |- main.py          :
    |- README.md        :
|- frontend/            :
    |- .dockerignore    :
    |- Dockerfile       :
    |- main.py          :
|- __init__.py          :
|- .gitkeep             :
data/                   :
docs/                   :
tests/                  :
|- backend/             :
|- frontend/            :
|- functional/          :
.gitignore              :
.python-version         :
Makefile                :
pyproject.toml          :
README.md               :
requirements.in         :
requirements.txt        :
uv.lock                 :
```

## Tech stack

* **Language**: Python 3.13
* **API development**: FastAPI
* **Web development**: FastHTML
* **Containerization**: Docker

## Automations
In this section the Makefile recipes are described.

* `install-deps`: this recipe allows the `uv` dependency management workflow, by reading in `requirements.in`, compiling it to `requirements.txt` and then installing them on the current virtual environment.
* `run-dev`: this recipe will run the development FastAPI server.
* `run-tests`: this recipe will run **all** the tests found in the `tests/` folder, in separate streams for each folder.

## Comments, issues and requests

All questions, requests and comments can be placed on the [Issues GitHub page](https://github.com/DarkestAbed/challenge-de-ingestion/issues).

Also, if you want to contribute, you can fork the repo and [send a Pull Request](https://github.com/DarkestAbed/challenge-de-ingestion/pulls).
