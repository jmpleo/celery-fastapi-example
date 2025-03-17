FROM python:3.11-slim

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy --ignore-pipfile --system

COPY . .

EXPOSE 8000