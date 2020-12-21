
FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  && apt-get install -y gcc \
  && apt-get install -y ldap-utils \
  && apt-get install -y libffi-dev \
  && apt-get install -y build-essential \
  && apt-get install -y libldap2-dev \
  && apt-get install -y libsasl2-dev \

  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY ./backend/requirements.txt /requirements.txt
#RUN pip install --upgrade pip && pip install --no-cache-dir -r /requirements.txt && rm -rf /requirements.txt
RUN pip install --upgrade pip && pip install -r /requirements.txt --use-deprecated=legacy-resolver && rm -rf /requirements.txt

COPY ./compose/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat


COPY  ./backend /app

USER root

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
