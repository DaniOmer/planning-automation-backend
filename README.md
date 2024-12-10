# PLANIFY BACKEND

## Prerequisites

## Project structure

```bash
planify-backend/
├── src/                     # Main source code
│   ├── apps/                # Application-specific modules
│   │   ├── users/           # Users module
│   │   │   ├── api/         # Routes and controllers
│   │   │   │   ├── routes.py
│   │   │   │   └── user_controller.py
│   │   │   ├── domain/      # Business logic for users
│   │   │   │   └── user_service.ts
│   │   │   ├── data-access/ # Data access (models, repositories)
│   │   │       ├── user_model.py
│   │   │       └── user_repository.py
│   ├── config/              # Configuration files
│   │   ├── db.ts            # MongoDB connection configuration
│   │   └── config.ts        # Other global settings
│   ├── shared/           # Reusable cross-component libraries
│   │   ├── logger/          # Log management
│   │   │   └── logger.py
│   │   ├── authenticator/   # Authentication and JWT management
│   │       └── auth_middleware.py
├── main.py                  # Project entrypoint
├── .gitignore               # Git ignore file for untracked files
├── requirements.txt         # Main project dependencies
└── .env                     # TypeScript configuration

```

## Running API locally

### Create and activate environment

```bash
python3 -m venv .venv
```

```bash
.venv/bin/activate
```

### Install requirements

```
pip3 install -r requirements.txt
```

### Start the Postgres databases:

```bash
docker-compose up -d
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
