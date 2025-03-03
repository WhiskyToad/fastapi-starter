FROM python:3
ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Install Poetry
RUN pip install poetry==1.4.2


WORKDIR /app
# Copy poetry files
COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR
# we use an exclude everything and add what you need via the .dockerignore
COPY . /app

RUN poetry install --without dev
EXPOSE 8000