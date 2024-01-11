FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8
ENV SECRET_KEY=13521685416516

RUN apt-get update && apt-get install -y libpq-dev gcc

RUN pip install poetry
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    htop \
    tzdata \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml poetry.lock /app/
COPY entrypoint.sh /usr/bin/

RUN poetry config virtualenvs.create false && poetry install

ADD . /app/

EXPOSE 8000

RUN ["chmod", "a+x", "/usr/bin/entrypoint.sh"]

USER root

ENTRYPOINT ["/usr/bin/entrypoint.sh"]
