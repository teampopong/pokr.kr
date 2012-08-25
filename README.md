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
1. 다음 패키지들을 설치한다. (Ubuntu Linux 기준)

	$ sudo add-apt-repository ppa:chris-lea/node.js
	$ sudo apt-get update
	$ sudo apt-get install python python-dev python2.7 libpq-dev nodejs npm
		mongodb mongodb-server mongodb-dev memcached

1. 파이썬, node.js 패키지들을 설치한다.

	$ sudo make install

1. 데이터를 DB에 올린다.

	$ sudo make load_db

1. 설정 파일을 변경한다.

	$ vi settings.py

1. 서버를 실행한다.

	$ python server.py
