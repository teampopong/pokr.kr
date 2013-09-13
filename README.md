POPONG Korean Politician Dictionary
===================================

[![Stories in Ready](https://badge.waffle.io/teampopong/pokr.png)](http://waffle.io/teampopong/pokr)

## Installation

1. Install dependant packages
    - Ubuntu Linux:

            $ sudo apt-get update
            $ sudo apt-get install python python-dev python2.7 libpq-dev libevent-dev
    - Mac OS X:

            Install Homebrew (http://mxcl.github.com/homebrew/)
            $ brew install python postgresql libevent
            $ initdb /usr/local/var/postgres -E utf8

1. Install **pokr**

        $ sudo make install

## Setup

1. Modify settings file
    - settings.py
    - alembic.ini
1. Load data

        $ make load_db
        $ python server.py insert_bills "some/where/*.json"
        $ python server.py insert_bill_keywords "some/where/*.txt"

## Run

    $ python server.py
