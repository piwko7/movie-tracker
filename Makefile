run:
	sudo docker-compose up -d

stop:
	sudo docker-compose down

build: purge
	sudo docker-compose build


pre-deps:
	pip install pipenv

install: pre-deps
	pipenv sync --dev

lint:
	pipenv run ruff .
	pipenv run isort --check .
	pipenv run black --check .
	pipenv run mypy

format:
	pipenv run isort .
	pipenv run black .

test:
	pipenv run pytest

update-pre-commit:
	pre-commit autoupdate


check-bandit:
	pipenv run bandit -r -c pyproject.toml .
