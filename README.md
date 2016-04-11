Pokr - Politics in Korea
==================================

**Pull requests are always welcome.**

## Installation

1. Install dependencies

    - Ubuntu

            $ sudo apt-get install nodejs postgresql-9.3 npm python-psycopg2 node-less
            $ sudo npm install -g uglify-js
            $ sudo pip install -r requirements.txt
            $ sudo pip install git+https://github.com/teampopong/popong-nlp.git
            $ sudo make install

    - Mac OS X

            $ brew install node postgresql
            $ npm install less uglify-js -g
            $ pip install -r requirements.txt
            $ pip install psycopg2
            $ make install

1. Create & modify configuration files

        $ make init
        $ createuser postgres
    - Set password for user "postgres" in PostgreSQL

            ALTER USER "postgres" WITH PASSWORD 'new_password';

    - Modify `alembic.ini`
        - `ID_HERE`: postgres id (ex: postgres)
        - `PASSWD_HERE`: postgres pw
        - `HOST_HERE`: postgres host (ex: localhost)

1. Create & init DB (You should first obtain a `pokrdb.dump` from [here](https://drive.google.com/file/d/0BwxUh0GzMJ4VMXJncHM4Qm1LZDQ/view?usp=sharing))

        $ sudo -u postgres psql -h localhost -U postgres -c 'CREATE DATABASE pokrdb;'
        $ sudo -u postgres psql -d pokrdb -f pokrdb.dump
        $ ./shell.py db init
        $ alembic stamp head

## Run Server

    $ ./run.py [-d] [-l LOCALE] [--port PORT]

## Update Data

1. Bills

        $ ./shell.py bill update "some/where/*.json" # from files
        $ ./shell.py bill update --source redis  # from Redis queue
        $ ./shell.py bill update --source db  # existing bills of the current session

1. Bill Keywords

        $ ./shell.py bill_keyword update "some/where/*.txt"

1. Candidacies

        $ ./shell.py candidacy update "some/where/*.json"

1. People

        $ ./shell.py person update "some/where/*.json"

    when the json is in [this form](https://github.com/teampopong/data-assembly/blob/master/assembly.json).

## License
[Apache v2.0](http://www.apache.org/licenses/LICENSE-2.0.html)
