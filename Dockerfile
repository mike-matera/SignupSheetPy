FROM docker.io/ubuntu:20.04

RUN apt update -y && DEBIAN_FRONTEND=noninteractive apt install -y python3-pip tzdata libmariadb-dev
RUN pip install django mariadb

COPY . /app
RUN mkdir /db

WORKDIR /app
RUN pip install -r requirements.txt

CMD /bin/sh /app/entrypoint.sh
EXPOSE 8000
