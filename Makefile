all: venv install env migrate run

venv:
	pip3 install virtualenv
	python3 -m venv .venv

install:
	. .venv/bin/activate && pip3 install -r requirements.txt
	. .venv/bin/activate && npm install

env:
	touch .env
	echo GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY >> .env
	echo EMAIL_ADDRESS=YOUR_GMAIL_ADDRESS >> .env
	echo EMAIL_PASSWORD=YOUR_GMAIL_GENERATED_PASSWORD >> .env

migrate:
	. .venv/bin/activate && python3 manage.py makemigrations
	. .venv/bin/activate && python3 manage.py migrate

run:
	. .venv/bin/activate && python3 manage.py runserver