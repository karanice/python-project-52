[![Actions Status](https://github.com/karanice/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/karanice/python-project-52/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=karanice_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=karanice_python-project-52)

[Deployed app](https://task-manager-0qwl.onrender.com/, "task_manager")

### About

Task manager with autentification and authorization. \
Following entities are developed:
* Users
* Tasks
* Statuses
* Labels \
Users can create tasks, assign performers, statuses and labels.

### Stack

* **django 5.2.2** for backend
* **Bootstrap 5**, **Django Templates** for frontend
* **PostgreSQL** (production), **SQLite** (development) as databases
* Deployed on **Render.com**
* **Rollbar** for error tracking
* **SonarQube** for code quality control
* Build with **uv**
* **Ruff** for linting

### Development Setup

1. Clone repository
```
https://github.com/karanice/python-project-52.git
cd python-project-52
```
2. Use make-commands
```
make install
make build
make migrate
make dev
```
3. You're great 🎉
