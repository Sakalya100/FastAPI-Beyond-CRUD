# FastAPI-Beyond-CRUD
The entire project developed while learning the advanced concepts of FastAPI

For more details, visit the project's [website](https://jod35.github.io/fastapi-beyond-crud-docs/site/).


## Application

It is hosted on Render under a free-tier plan just for learning purposes. You can check it out [here](https://bookly-api-5aos.onrender.com/docs#/)
## Table of Contents

1. [Getting Started](#getting-started)
2. [Prerequisites](#prerequisites)
3. [Project Setup](#project-setup)
4. [Running the Application](#running-the-application)
5. [Running Tests](#running-tests)
6. [Notes](#Notes)

## Getting Started
Follow the instructions below to set up and run your FastAPI project.

### Prerequisites
Ensure you have the following installed:

- Python >= 3.10
- PostgreSQL
- Redis

### Project Setup
1. Clone the project repository:
    ```bash
    git clone git@github.com:Sakalya100/FastAPI-Beyond-CRUD.git
    ```
   
2. Navigate to the project directory:
    ```bash
    cd FastApi-Beyond-CRUD/
    ```

3. Create and activate a virtual environment:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Set up environment variables by copying the example configuration:
    ```bash
    cp .env.example .env
    ```

6. Run database migrations to initialize the database schema:
    ```bash
    alembic upgrade head
    ```

7. Open a new terminal and ensure your virtual environment is active. Start the Celery worker (Linux/Unix shell):
    ```bash
    sh runworker.sh
    ```

## Running the Application
Start the application:

```bash
fastapi dev src/
```

## Running Tests
Run the tests using this command
```bash
pytest
```

## Notes
I have created a comprehensive set of notes while learning capturing almost all the important topics from the video. You can check it out here in the published [Blog](https://neuralnomad.notion.site/Advanced-FastAPI-14760f647adc8140b946f30a5b4e41ec).
