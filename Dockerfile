ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim

ENV POETRY_VERSION=2.1.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

WORKDIR /app

RUN pip3 install poetry==${POETRY_VERSION}

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create true &&\
    poetry install --no-interaction --no-ansi --no-root

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.pokemon_python_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
