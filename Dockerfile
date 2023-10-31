FROM python:3.9

RUN mkdir /usr/src/account-book/

WORKDIR /usr/src/account-book/

COPY . .

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

RUN apt-get update &&\
    apt-get install sudo

WORKDIR /usr/src/account-book/account-back