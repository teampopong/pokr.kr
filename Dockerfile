FROM python:2

ENV PYTHONIOENCODING='UTF-8'
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

RUN apt-get update && apt-get install -y git wget && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /pokr.kr && \
    mkdir ~/.pip && echo '[global]\n\
index-url=http://mirror.kakao.com/pypi/simple/\n\
trusted-host=mirror.kakao.com' > ~/.pip/pip.conf

WORKDIR /pokr.kr
ADD . .
RUN pip install --upgrade pip && pip install -r requirements.txt && \
    pip install git+https://github.com/teampopong/popong-models.git && \
    pip install git+https://github.com/teampopong/popong-data-utils.git && \
    pip install git+https://github.com/teampopong/popong-nlp.git && \
    git submodule init && git submodule update

ADD .conf.samples/alembic.ini.sample /pokr.kr/alembic.ini
ADD .conf.samples/settings.py.sample /pokr.kr/settings.py
#RUN cat /pokr.kr/.conf.samples/alembic.ini.sample | sed 's/ID_HERE/docker/g' | sed 's/PASSWD_HERE/docker/g' | sed 's/HOST_HERE/localhost/g' > ./pokr.kr/alembic.ini

EXPOSE 8000
ENTRYPOINT ./entrypoint.sh
