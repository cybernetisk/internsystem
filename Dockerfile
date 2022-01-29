FROM python:3.9-alpine@sha256:a90109e6a257b503924fbc69c782850d4ad98e9b778697d046352ef149368234

# postgresql-dev required to build psycopg2 with pip
RUN set -eux; \
    apk add --no-cache \
      ca-certificates \
      build-base \
      libxml2-dev \
      libxslt-dev \
      postgresql-dev \
      su-exec \
      xmlsec-dev \
      libffi-dev \
      libressl-dev \
      musl-dev \
      cargo \
      rust \
    ; \
    mkdir -p /app; \
    mkdir -p /usr/src/static; \
    addgroup -g 1000 app; \
    adduser -D -G app -u 1000 app; \
    chown app:app /app /usr/src/static

WORKDIR /app
USER app

ENV PATH="/home/app/.local/bin:$PATH"

# handle saml-stuff first because it takes very long to install (compile)
COPY requirements_saml.txt /app
RUN pip install --user --no-cache-dir -r requirements_saml.txt

COPY requirements.txt /app/
RUN pip install --user --no-cache-dir -r requirements.txt

COPY . /app
COPY container/start.sh /start.sh
COPY container/gunicorn.conf /gunicorn.conf

EXPOSE 8000

CMD ["/start.sh"]
