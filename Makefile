devinst:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest --cov -vv
	rm -rf .coverage .pytest_cache

lint:
	check-requirements
	black --check zagrajmy tests
	isort --recursive --check-only zagrajmy tests
	pycodestyle zagrajmy tests
	pydocstyle zagrajmy tests
	bandit zagrajmy tests
	mypy zagrajmy
	pylint zagrajmy tests
	rm -rf .mypy_cache

format:
	black zagrajmy tests
	isort --recursive zagrajmy tests