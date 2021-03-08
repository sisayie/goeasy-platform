FROM python:3.6
MAINTAINER Sisay Chala

RUN mkdir /application

COPY . /application
COPY requirements.txt /application

WORKDIR /application

RUN pip3 install -r requirements.txt

#Should be modified at on containers up on deployment
ENV POSTGRES_USER="postgres"
ENV POSTGRES_PASSWORD="password"
ENV POSTGRES_DB="pubdb"
ENV POSTGRES_PORT="5443"
ENV POSTGRES_HOST="db"
ENV APP_SECRET_KEY="your_secrete_key"

EXPOSE 5003

#CMD ["uwsgi", "wsgi.ini"]
CMD ["python", "server.py"]