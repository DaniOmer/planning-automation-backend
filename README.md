# PLANIFY BACKEND

## Prerequisites

Ensure you have Docker and Docker Compose installed on your system.
Verify that you have Python 3.9 to 3.11 installed if running locally outside of Docker.
Optional: Install a PostgreSQL database if not using the default Docker setup.

## Global stacks

### - Backend stack

- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- Alembic
- Docker

### - Frontend stack

- Next.js
- TailwindCSS
- ShadCN
- ReactPicker

## Main Functionalities and contributors

[Omer DOTCHAMOU](https://github.com/DaniOmer)

- Project backend configuration and setup (Init with database, docker, logging and migrations tools)
- Authentication configuration on backend side (Login and register users (admin + teacher), Invitation workflow)
- Implementation of security configuration (fastapi dependencies for managing users roles and permissions)
- `Dynamic Scheduling`: Generate optimized schedules using advanced constraints and OR-Tools.
- Usage of security dependancies

[Johnny CHEN](https://github.com/johnnyhelloworld)

- CRUD implementation for `EducationalCourses`, `YearsGroups` and `Classes`
- Implementation of route to load availability from csv file
- Logic to convert data from LLM to csv file
- Usage of security dependancies

[Mohand AIT AMARA](https://github.com/aitamara)

- CRUD implementation on `Availabilities` et `Subjects` models
- Implementation of script to generate data fixtures
- Implementation of LLM (GPT-4) for processing user prompt to generate csv file
- Implementation of frontend logic for `teachers`, `years_groups` and `subjects`
- Usage of security dependancies

[Faez BACAR ZOUBERI](https://github.com/FAEZ10)

- CRUD implementation for `Classrooms`, `SessionSubject` and `AssignmentSubject`
- Implementation of teachers workflow with good error handling
- Implementation of data fixtures with faker
- Implementation of admin forms and users availabilities logic on frontend side
- Implementation of the view to display `subjects` assignated to teachers
- Usage of security dependancies

[Ady Masivi](https://github.com/ady243)

- Authentication workflow on frontend side (CurrentUser, Auth token handling, Invitation logic)
- Implementation of admin forms (YearsGroups, Classes, Assignments, Subjects)
- Implementation of the view to display sessions on calendar
- Implementation of the view to vizualize user planning
- Implementation of the view for prompting LLM to generate availabilities

## API Documentation

- `SWAGGER DOC` http://localhost:8000/docs

## Project structure

```bash
planify-backend/
├── src/                                # Main source code
│   ├── apps/                           # Application-specific modules
│   │   ├── users/                      # Users module
│   │   │   ├── routes/                 # Routes
│   │   │   │   └── user_route.py
│   │   │   ├── services/               # Business logic for users
│   │   │   │   └── user_service.py     # Operations related to users
│   │   │   ├── model/                  # Data access (models, pydantic schema)
│   │   │       ├── user_model.py       # SQLAlchemy model
│   │   │       └── user_schema.py      # Pydantic schema
│   ├── config/                         # Configuration files
│   │   ├── database_service.py         # Postgres database connection configuration
│   │   └── config.py                   # Other global settings
│   ├── helpers/                        # Reusable cross-component
│   │   ├── messenger_helper.py         # Missive for sending email
│   │   ├── security_helper.py          # Security helper for authentication
│   ├── libraries/                      # Reusable cross-component libraries
│   │   ├── ortools/                    # Or-Tools
│   │       └── combinator.py           # Class for handling timetambling issues
├── main.py                             # Project entrypoint
├── .gitignore                          # Git ignore file for untracked files
├── requirements.txt                    # Main project dependencies
└── .env                                # Environment variables

```

## Running API locally without docker

### Create .env file based on .env.example file

```bash
touch .env
```

### Create and activate environment

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

### Install requirements

```
pip3 install -r requirements.txt
```

### Start the Postgres databases:

```bash
docker compose up -d
```

To setup DB run :

```bash
python3 -m alembic upgrade head
```

To clean your databse run :

```bash
python3 -m alembic downgrade -1
```

## You modify something in databse ?

Change your sqlAlchemy model or if you add new tables add it in import in file `src/migrations/env.py`.</br>
Then you can run this command :

```bash
 python3 -m alembic revision --autogenerate -m "the name of your changes"
```

### Run the following command to start Planify API

```
python3 -m uvicorn main:app --reload
```

## Running API locally with docker

### Build the project

```bash
docker compose build
```

### Run the project

```bash
docker compose up
```
