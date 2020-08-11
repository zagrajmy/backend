export DJANGO_SETTINGS_MODULE=zagrajmy.settings.development
export PYTHONPATH=app:stubs
export COMPOSE_PROJECT_NAME=zagrajmy

devinst:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest --cov
	rm -rf .coverage .pytest_cache

lint:
	check-requirements
	black --check app tests stubs
	isort --recursive --check-only --diff app tests stubs
	pycodestyle app tests
	bandit -r app
	mypy app||true
	pylint app tests
	rm -rf .mypy_cache

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
	django-admin behave tests/functional --no-capture

coverage:
	coverage run --source=app,tests/functional -m manage behave tests/functional --no-capture
	coverage report
	pytest --cov=app --cov=tests/unit

upgrade:
	upgrade-requirements
	pip install -r requirements.txt
	pip install -r requirements-dev.txt