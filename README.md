Pokr - Politics in Korea
==================================

**Pull requests are always welcome.**

## Installation

1. Install dependant packages
    - Ubuntu Linux:

            Install nodejs to use npm (http://nodejs.org/download/)
            Install Redis (http://redis.io/download)
            # apt-get update
            # apt-get install python python-dev python2.7 libpq-dev libevent-dev
            # npm install less uglify-js@1 -g
    - Mac OS X:

            Install Homebrew (http://mxcl.github.com/homebrew/)
            Install nodejs to use npm (http://nodejs.org/download/)
            Install Redis (http://redis.io/download)
            # brew install python postgresql libevent
            # initdb /usr/local/var/postgres -E utf8
            # npm install less uglify-js@1 -g

1. Install **pokr**

        $ sudo make install

## Setup

1. Modify configuration files:
    - conf/frontend.py
    - conf/storage.py
        - `POSTGRES_SETTINGS`
    - alembic.ini
        - `ID_HERE`: postgres id
        - `PASSWD_HERE`: postgres pw
        - `HOST_HERE`: postgres host

1. Load data

        $ make load_db

    <blockquote>
    <b>Troubleshooting</b>

    1. For load_db error:

            pg_restore -d popongdb data/db.sql
            pg_restore: [archiver] input file does not appear to be a valid archive
            make: *** [load_db] Error 1

        execute:<br>
        (If you don't have a password set, run `ALTER USER 'someUsername' PASSWORD 'somePassword';` in psql.)

            $ sudo -u postgres psql
            postgres=# create database popongdb;

            $ cat data/db.sql | psql popongdb

    2. For `Exception: alembic is not on the head`, execute:

            $ alembic upgrade head

    </blockquote>

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

    $ ./run.py

## Run API Server

	$ ./api.py

## License
[Apache v2.0](http://www.apache.org/licenses/LICENSE-2.0.html)

