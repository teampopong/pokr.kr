[![Stories in Ready](http://badge.waffle.io/teampopong/pokr.png)](http://waffle.io/teampopong/pokr)  
POPONG Korean Politician Dictionary
===================================

## Installation

1. Install dependant packages
    - Ubuntu Linux:

            $ sudo apt-get update
            $ sudo apt-get install python python-dev python2.7 libpq-dev libevent-dev
    - Mac OS X:
	
            Install Homebrew (http://mxcl.github.com/homebrew/)
            $ brew install python postgresql libevent

1. Install **pokr**

        $ sudo make install

## Setup

1. Modify settings file
    - settings.py
    - alembic.ini
1. Load data

        $ make load_db
        $ python server.py insert_bill_keywords some_bill_file.pdf

## Run

	$ python server.py
