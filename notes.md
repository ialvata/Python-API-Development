After some trial and errors... Poetry is really not suitable/easy to manage the virtual env,
so..
First create a venv:
    python3 -m venv /path/to/new/virtual/environment

In your venv bin/activate script, add the following line:
    PYTHONPATH="/path/to/root/level"
    export PYTHONPATH

Now activate it, and install poetry inside the venv.
Do:
    poetry install
or
    poetry add <package>

After installing pytest, we may need to deactivate the venv and reactivate it again.
    deactivate && source .env/bin/activate
or just close VSCode and open it again.

To install psycopg2, we first install:
    sudo apt install libpq-dev python3-dev

# Running the App
1- While in the directory, run:
        Docker Compose up
2- Activate our server app:
        uvicorn app.main:app --reload
    If you want to access the server app:
        http://localhost:8000/

# Accessing Integrations
Grafana:
We need an API key to validate almost any request.
We'll be able to find them at /org/apikeys
The usual url to access Grafana is:
    http://localhost:3000/


# Environment Variables
This project has two ways of accessing environmental variables:
    - Through `load_dotenv`
        `load_dotenv(dotenv_path=env_path)`
    and then we load using
        `os.environ["GF_SECURITY_ADMIN_USER"]`
    - Through `configparser` which allows for sections with passwords. This is useful
    if we have several different databases, but the variables names are the same accross dbs.
    See `PostgresDB` class, for an example.

Docker useful commands:
    docker exec -ti mycontainer /bin/bash
    docker logs mycontainer

This project has Linear(linear.app) integration, using my personal profile.
