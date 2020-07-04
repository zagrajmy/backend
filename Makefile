export DJANGO_SETTINGS_MODULE=zagrajmy.settings.development
export PYTHONPATH=app
export COMPOSE_PROJECT_NAME=zagrajmy

devinst:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest --cov
	rm -rf .coverage .pytest_cache

lint:
	check-requirements
	black --check app
	isort --check-only app
	pycodestyle app
	bandit app
	mypy app
	pylint app
	rm -rf .mypy_cache

format:
	black app
	isort app

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
