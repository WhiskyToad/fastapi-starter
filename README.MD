# GoalForge FastAPI App with PostgreSQL and Docker

## Introduction

This is an API for the goalforge app.

## Features

- FastAPI for building API endpoints
- PostgreSQL for database storage
- Docker for containerization
- SQLAlchemy as the ORM (Object-Relational Mapping)
- Pyright for type checking

## Prerequisites

- [Docker](https://www.docker.com/) installed
- [Docker Compose](https://docs.docker.com/compose/) installed
- [Poetry] (<https://python-poetry.org/docs/>) installed

## Getting Started

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/WhiskyToad/fastapi-starter
   cd fastapi-starter
   ```

2. **Configure Environment Variables:**

Copy the .env.example file in the root of the project and configure your environment variables.

3. **Install the dependancies locally:**

We use poetry to manage this project, you will want to ensure you create virtual environments locally

   ```bash
   poetry config virtualenvs.in-project true
   ```

And then run this command to install the dependancies and create a local .venv file

   ```bash
   poetry install
   ```

Make sure your ide is configured to use this .venv as your interpretor for python

4. **Build and Run the Docker Container:**

   ```bash
   docker compose up --build

   ```

5. **Access the FastAPI App:**

Open your browser and navigate to <http://localhost:8000/docs> to access the FastAPI Swagger documentation.

6. **Stop the Docker Container:**

   ```bash
   docker-compose down
   ```

## Making migrations

We use alembic for migrations, here are the commands that will need to be ran inside your docker terminal. When you make new models add them to the init file in the models folder to be picked up.

**Make migration:**

```bash
poetry run alembic revision --autogenerate -m "Initial migration"
poetry run alembic upgrade head
```

## Tests

Tests are all under the test folder and split into different folders within. It spins up a SQLite database for each test run and you can run the tests with the command

   ```bash
   poetry run pytest
   ```

## Types

This project is managed by pyright, you should have the pylance extension installed from vscode and can run the checker with this command

   ```bash
   poetry run pyright
   ```

## Project Module Creator

This script creates a basic module structure with Model, Repository, Routes, Schema, and Service files.

### Usage

1. Make sure you have Python installed on your system.

2. Clone this repository or download the script `create_module.py`.

3. Open a terminal window and navigate to the directory containing the `create_module.py` script.

4. Run the script by executing the following command:

    ```bash
    python create_module.py
    ```

5. Follow the prompts and enter the name of the module when prompted.

6. After execution, a new folder with the module name will be created in the `app` directory. Inside this folder, you will find the following files:
    - `ModuleNameModel.py`: Contains the data model definitions.
    - `ModuleNameRepository.py`: Provides access to data storage and retrieval methods.
    - `ModuleNameRoutes.py`: Defines the API routes and endpoint handlers.
    - `ModuleNameSchema.py`: Contains Pydantic schema definitions for data validation.
    - `ModuleNameService.py`: Implements the business logic and interacts with the repository.

7. You can modify these files to suit your specific project requirements.

### Folder Structure

project_root/
│
├── apps/
│ ├── ModuleName/
│ │ ├── ModuleNameModel.py
│ │ ├── ModuleNameRepository.py
│ │ ├── ModuleNameRoutes.py
│ │ ├── ModuleNameSchema.py
│ │ └── ModuleNameService.py
