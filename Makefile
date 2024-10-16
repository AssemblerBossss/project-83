#Makefile
PORT ?= 8000

install-whl:
	pip dist/install hexlet_code-0.1.0-py3-none-any.whl

build:
	poetry build

db-create:
	createdb project83

schema-load:
	psql project83 < database.sql

install:
	poetry install,

dev:
	poetry run flask --debug --app page_analyzer:app run


start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app


