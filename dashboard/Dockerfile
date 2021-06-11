FROM python:3.6
MAINTAINER Sisay Chala

RUN mkdir /application

COPY ./dist /application

COPY requirements.txt /application

WORKDIR /application

RUN pip3 install -r requirements.txt


EXPOSE 7009

CMD ["python3", "main.py"]