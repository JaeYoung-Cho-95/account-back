FROM python:3.9

RUN mkdir /usr/src/account-back/

WORKDIR /usr/src/account-back/

COPY . .

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

RUN apt-get update &&\
    apt-get install sudo

WORKDIR ./account-back