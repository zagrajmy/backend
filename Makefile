export PYTHONPATH=app

devinst:
	pip install -r app/check-requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest --cov
	rm -rf .coverage .pytest_cache

lint:
	check-requirements
	black --check app
	isort --recursive --check-only app
	pycodestyle app
	pydocstyle app
	bandit app
	mypy app
	pylint app
	rm -rf .mypy_cache

format:
	black app
	isort --recursive app