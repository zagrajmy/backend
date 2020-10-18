export DJANGO_SETTINGS_MODULE=zagrajmy.settings.development
export PYTHONPATH=app:stubs

# INSTALL

inst-prod:
	pip install -r requirements.txt --use-feature=2020-resolver

inst-dev:
	pip install -r requirements-dev.txt --use-feature=2020-resolver

inst-pip:
	pip install -U pip --use-feature=2020-resolver

inst-upg:
	upgrade-requirements

install-prod: inst-pip inst-prod

install-dev: inst-pip inst-prod inst-dev

upgrade: inst-upg install-dev

# TESTING

test-unit:
	pytest

test-unit-cov:
	pytest --cov=app --cov=tests/unit

test-behave:
	django-admin behave tests/functional

test-behave-cov:
	coverage run --source=app,tests/functional -m manage behave tests/functional
	coverage report

test: test-behave test-unit

test-cov: test-behave-cov test-unit-cov

behave-dev:
	django-admin behave --stop -vv tests/functional

pytest-dev:
	pytest --cov -svvx


# FORMATTING

fmt-black:
	black app tests stubs

fmt-isort:
	isort app tests stubs

format: fmt-black fmt-isort

# LINTING

lint-check:
	check-requirements

lint-black:
	black --check app tests stubs

lint-isort:
	isort --check-only --diff app tests stubs

lint-pylint:
	pylint app/contrib app/notice_board app/common app/crowd app/chronology app/zagrajmy
	pylint --rcfile=tests/.pylintrc tests

lint-pycodestyle:
	pycodestyle app tests

lint-bandit:
	bandit -r app

lint-mypy:
	mypy app||true

lint: lint-check lint-black lint-isort lint-pycodestyle lint-bandit lint-mypy lint-pylint

# General

prcheck: install-dev format lint test-cov graph messages

# Docker

graph:
	docker-compose exec -T web django-admin graph_models chronology crowd notice_board -g -o docs/models.png

messages:
	docker-compose exec -T web django-admin makemessages -l pl

django:
	docker-compose exec web django-admin $(cmd)
