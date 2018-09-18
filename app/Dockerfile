FROM python:3.7.0-alpine3.8

ENV PROJECT_ROOT /opt

# Set timezone
RUN set -x && \
    apk add --update --no-cache \
        tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del --purge tzdata && \
    rm -rf /var/cache/apk/*

# Install dependencies
RUN set -x && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir \
        django>=2.0.7 \
        python-dotenv>=0.9 \
        gunicorn

COPY ./webapp ${PROJECT_ROOT}/webapp

WORKDIR ${PROJECT_ROOT}/webapp

CMD ["gunicorn", "webapp.wsgi", "--config", "gunicorn.config.py"]