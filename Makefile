install:
		uv sync

build:
		./build.sh

render-start:
		gunicorn task_manager.wsgi

dev:
		python3 manage.py runserver 

shell:
		python3 manage.py shell

lint:
		uv run ruff check task_manager 


fix-lint:
		uv run ruff check task_manager

migrate:
		uv run manage.py migrate

create-migration:
		python3 manage.py makemigrations
