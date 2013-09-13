POPONG Korean Politician Dictionary
===================================

## Installation

<span style="color: red">Caution: outdated. Need to be updated.</span>

1. Install dependant packages
    - Ubuntu Linux:

            Install nodejs to use npm (http://nodejs.org/download/)
            # apt-get update
            # apt-get install python python-dev python2.7 libpq-dev libevent-dev
            # npm install less uglify-js@1 -g
    - Mac OS X:

            Install Homebrew (http://mxcl.github.com/homebrew/)
            $ brew install python postgresql libevent
            $ initdb /usr/local/var/postgres -E utf8

1. Install **pokr**

        $ sudo make install

## Setup

1. Modify settings file
    - settings.py
    - conf/storage.py
    - alembic.ini

1. Load data

        $ make load_db
        $ python server.py insert_bills "some/where/*.json"
        $ python server.py insert_bill_keywords "some/where/*.txt"

## Run

    $ python server.py
