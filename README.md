Pokr - Politics in Korea
==================================

**Pull requests are always welcome.**

## Installation

1. Install dependencies

        $ apt-get install postgresql-9.3 npm python-psycopg2 node-less node-uglify # and set password for user 'postgres' in postgresql
        $ pip install -r requirements.txt

    > Installing `less` and `uglify` via npm may not work

1. Create & modify configuration files:
    - `make init`
    - settings.py
    - alembic.ini
        - `ID_HERE`: postgres id
        - `PASSWD_HERE`: postgres pw
        - `HOST_HERE`: postgres host

1. Create & init DB

        $ make create_db # psql dumpfile should be in the highest directory as 'pokr.dump'
        $ make init_db

## Insert/Update Data

1. Bills

        $ ./shell.py bill update "some/where/*.json" # from files
        $ ./shell.py bill update --source redis  # from Redis queue
        $ ./shell.py bill update --source db  # existing bills of the current session

1. Bill Keywords

        $ ./shell.py bill_keyword update "some/where/*.txt"

1. Candidacies

        $ ./shell.py candidacy update "some/where/*.json"


## Run Server

    $ ./run.py [-d] [-l LOCALE] [--port PORT]


## License
[Apache v2.0](http://www.apache.org/licenses/LICENSE-2.0.html)

