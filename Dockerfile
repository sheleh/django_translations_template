FROM python:3.9
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt install gettext -y

RUN mkdir /code
WORKDIR /code

COPY . /code

RUN pip install --upgrade pip
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/
