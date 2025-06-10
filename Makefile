install:
		uv sync

build:
		./build.sh

render-start:
		gunicorn task_manager.wsgi

make dev:
		python3 manage.py runserver 

lint:
		uv run ruff check task_manager 


fix-lint:
		uv run ruff check task_manager

migrate:
		uv run manage.py migrate

create-migration:
		python manage.py makemigrations
