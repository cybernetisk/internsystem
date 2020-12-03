FROM python:3.9-alpine@sha256:df77433749466a68bb599009753c9e5a8efaa3dd9c16450d442bb32f4c1fad4e

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
