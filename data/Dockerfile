# set base image
FROM python:3.12.11-slim-bookworm AS build

# set working directory
WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir poetry==1.8.3

# copy source code to build
COPY pyproject.toml poetry.lock scripts/init ./
COPY dayfeel_auth ./dayfeel_auth

COPY alembic ./alembic
COPY alembic.ini ./

# create virutal environment and install project dependencies in it
RUN poetry config virtualenvs.in-project true \
 && poetry install --without dev


# set production image
FROM python:3.12.11-slim-bookworm

# install all deps
RUN apt-get update && apt-get install -y curl && apt-get clean

# set environment variables
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.utf-8
ENV PATH="/app/.venv/bin:$PATH"

# set working directory
COPY --from=build /app /app

# run app
CMD ["/app/init"]
