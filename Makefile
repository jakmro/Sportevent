install:
	pip install -r requirements.txt
	npm install

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver

all: install migrate