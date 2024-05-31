all: install env migrate run

install:
	pip3 install -r requirements.txt
	npm install

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

env:
	touch .env
	echo GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY >> .env
	echo EMAIL_ADDRESS=YOUR_GMAIL_ADDRESS >> .env
	echo EMAIL_PASSWORD=YOUR_GMAIL_GENERATED_PASSWORD >> .env

run:
	python3 manage.py runserver