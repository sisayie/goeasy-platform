FROM python:3.6
MAINTAINER Sisay Chala

RUN mkdir /application

COPY . /application
COPY requirements.txt /application

WORKDIR /application

RUN pip install -r requirements.txt

ENV POSTGRES_USER="postgres"
ENV POSTGRES_PASSWORD="password"
ENV POSTGRES_DB="pubdb"
ENV POSTGRES_PORT="5442"
ENV POSTGRES_HOST="gedb"
ENV APP_SECRET_KEY="your_secrete_key"

EXPOSE 5003

#CMD ["uwsgi", "wsgi.ini"]
CMD ["python", "server.py"]

unable to delete aa819d948626 (must be forced) - image is being used by stopped container 5a1fb92e39a6