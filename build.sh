#!/usr/bin/env bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# УБРАТЬ ПОТОМ КОММЕНТАРИИ
# здесь добавьте все необходимые команды для установки вашего проекта 
# команду установки зависимостей, сборки статики, применения миграций и другие
make install && make collectstatic && make migrate