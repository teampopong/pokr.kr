Pokr - Politics in Korea
==================================

**Pull requests are always welcome.**

## Installation

1. Install dependant packages (postgresql >= 9.2)


    - Ubuntu Linux:

            Install postgresql (http://www.postgresql.org/download/)
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

1. Create Database

1. Create & modify configuration files:
    - `make init`
    - settings.py
    - alembic.ini
        - `ID_HERE`: postgres id
        - `PASSWD_HERE`: postgres pw
        - `HOST_HERE`: postgres host

1. Initialize Database

        $ make init\_db

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

