build:
		./build.sh

render-start:
		gunicorn task_manager.wsgi

lint:
		uv run ruff check task_manager 


fix-lint:
		uv run ruff check task_manager
