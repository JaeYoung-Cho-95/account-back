FROM python:3.9

RUN mkdir /usr/src/account-back/

WORKDIR /usr/src/account-back/

COPY ./ .

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

RUN apt-get update &&\
    apt-get install sudo &&\
    sudo apt-get install sqlite3

WORKDIR ./django_app
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
