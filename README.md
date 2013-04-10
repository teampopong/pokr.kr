POPONG Korean Politician Dictionary
===================================

Install & Run Service
---------------------

### Installation

1. install dependant packages

    - Ubuntu Linux:

	$ sudo apt-get update
	$ sudo apt-get install python python-dev python2.7 libpq-dev libevent-dev

    - Mac OS X:
	
	Install Homebrew (http://mxcl.github.com/homebrew/)
	$ brew install python postgresql libevent

1. install **polidic**

	$ sudo make install

### Setup

1. modify settings file

	- settings.py
	- alembic.ini

1. load data

	$ make load_db

### Run

1. run the server

	$ python server.py

### TODO

1. setuptools
1. tests
