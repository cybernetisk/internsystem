REQUIREMENTS_TXT=requirements.txt requirements_saml.txt
DEVSERVER_PORT=8000

include Makefile.venv
Makefile.venv:
	curl \
		-o Makefile.fetched \
		-L "https://github.com/sio/Makefile.venv/raw/v2019.11.22/Makefile.venv"
	echo "048c4a1b9265231db97b4903bb2e835b01e0d84a5b7435d4bb8d5926c99aa7f7 *Makefile.fetched" \
		| sha256sum --check - \
		&& mv Makefile.fetched Makefile.venv

.PHONY: init-settings
init-settings:
	./scripts/setup_settings.sh

.PHONY: install
install: venv
	$(VENV)/pip install -r requirements.txt -r requirements_saml.txt

.PHONY: migrate
migrate: venv
	$(VENV)/python ./manage.py migrate
	sh -c ". .venv/bin/activate && scripts/load_fixtures.sh"

.PHONY: init
init: Makefile.venv venv install init-settings migrate

.PHONY: run
run: venv
	$(VENV)/python ./manage.py runserver $(DEVSERVER_PORT)

.PHONY: docker-init
docker-init: init-settings
	# Fetch last built image to reduce build time locally.
	docker-compose pull
	docker-compose build api
	docker-compose run --rm api ./manage.py migrate
	docker-compose run --rm api ./scripts/load_fixtures.sh

.PHONY: docker-run
docker-run:
	docker-compose up api

.PHONY: docker-shell
docker-shell:
	docker-compose run --rm api sh
