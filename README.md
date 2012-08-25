POPONG
======

Prerequisites
-------------
TBD


Development
-----------
TBD


Testing
-------
TBD


Install & Run Service
---------------------

### Preperations

1. 저장소 서브모듈들을 로드한다.

	$ make update_submodule

### Installation

1. 다음 패키지들을 설치한다. (명령어는 Ubuntu Linux 기준)

	$ sudo add-apt-repository ppa:chris-lea/node.js
	$ sudo apt-get update
	$ sudo apt-get install python python-dev python2.7 libpq-dev nodejs npm
		mongodb mongodb-server mongodb-dev memcached

1. 파이썬, node.js 패키지들을 설치한다.

	$ sudo make install

### Setup

1. 데이터를 DB에 올린다.

	$ make load_db

1. 설정 파일을 변경한다.

	$ vi settings.py

### Run

1. 서버를 실행한다.

	$ python server.py
