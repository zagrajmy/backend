export PYTHONPATH=app

devinst:
	pip install -r app/requirements.txt
	pip install -r app/requirements_dev.txt

test:
	pytest --cov
	rm -rf .coverage .pytest_cache

lint:
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