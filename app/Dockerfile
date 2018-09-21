FROM python:3.6-alpine3.8

ENV PROJECT_ROOT /opt/Hacku

# Set timezone
RUN set -x && \
    apk add --update --no-cache \
        tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del --purge tzdata && \
    rm -rf /var/cache/apk/*

# Install dependenciesi
COPY Pipfile ${PROJECT_ROOT}/
COPY Pipfile.lock ${PROJECT_ROOT}/

RUN set -x && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pipenv

WORKDIR ${PROJECT_ROOT}

RUN pipenv install

COPY ./webapp ${PROJECT_ROOT}/webapp

WORKDIR ${PROJECT_ROOT}/webapp

CMD ["pipenv","run","gunicorn", "webapp.wsgi", "--config", "gunicorn.config.py"]