FROM python:3.8.10

ENV PYTHONUNBUFFERED 1

RUN mkdir /globant_weather_api

WORKDIR /globant_weather_api

COPY . .

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

ENV API_KEY_OPW=21056e88589f13ccd2c21c8f9acbba8e

RUN useradd -ms /bin/bash the_user
USER the_user