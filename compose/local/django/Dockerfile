FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# TOFIX: Verify if the following lines are necessary
RUN apt-get update
    # dependencies for building Python packages
    # && apt-get install -y build-essential \
    # psycopg2 dependencies
    # && apt-get install -y libpq-dev \
    # Translations dependencies
    # && apt-get install -y gettext \
    # LibreOffice for pdf generation from docx
    # && apt-get install default-jre libreoffice libreoffice-java-common -y \
    # cleaning up unused files
    # && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    # && rm -rf /var/lib/apt/lists/*
RUN apt-get install -y build-essential
RUN apt-get install -y libpq-dev
RUN apt-get install -y gettext
RUN apt-get install -y default-jre libreoffice libreoffice-java-common
RUN apt-get purge  -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false
RUN rm -rf /var/lib/apt/lists/*

# Install Requirements of the project
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

COPY ./compose/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker


COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
