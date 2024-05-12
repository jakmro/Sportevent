install:
	pip3 install -r requirements.txt
	npm install

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

run:
	python3 manage.py runserver

all: install migrate