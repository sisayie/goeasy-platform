FROM python:3.6
MAINTAINER Sisay Chala

RUN mkdir /application

COPY . /application

WORKDIR /application

RUN pip install -r requirements.txt

EXPOSE 5003

CMD ["uwsgi", "wsgi.ini"]
