export DJANGO_SETTINGS_MODULE=zagrajmy.settings.development
export PYTHONPATH=app:stubs
export COMPOSE_PROJECT_NAME=zagrajmy

devinst:
	pip install -r requirements.txt -r requirements-dev.txt --use-feature=2020-resolver

upgrade-req:
	upgrade-requirements

make upgrade: upgrade-req devinst

test:
	pytest --cov

pytest-dev:
	pytest --cov -vv -x

check:
	check-requirements

black:
	black --check app tests stubs

isort:
	isort --recursive --check-only --diff app tests stubs

pycodestyle:
	pycodestyle app tests

bandit:
	bandit -r app

mypy:
	mypy app||true

pylint:
	pylint app/contrib app/notice_board app/common app/crowd app/chronology app/zagrajmy
	pylint --rcfile=tests/.pylintrc tests

clean:
	rm -rf .mypy_cache .coverage .pytest_cache


lint: check black isort pycodestyle bandit mypy pylint clean

format:
	black app tests stubs
	isort --recursive app tests stubs

graph:
	docker exec -ti backend_web_1 django-admin graph_models chronology crowd notice_board -g -o docs/models.png

dc-dev-down:
	docker-compose -f docker-compose.yml down

dc-dev-up:
	docker-compose -f docker-compose.yml up -d --build

dc-prod-down:
	docker-compose -f docker-compose.prod.yml down

dc-prod-up:
	docker-compose -f docker-compose.prod.yml up -d --build

behave:
	django-admin behave tests/functional

coverage:
	coverage run --source=app,tests/functional -m manage behave tests/functional
	coverage report
	pytest --cov=app --cov=tests/unit

upgrade:
	upgrade-requirements
	pip install -r requirements.txt
	pip install -r requirements-dev.txt