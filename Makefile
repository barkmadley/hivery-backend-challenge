.PHONY: setup
setup:
	# Requires python 3
	virtualenv .venv -p `which python3`
	@echo "Please run 'source .venv/bin/activate' to enter virtualenv for subsequent commands"

.PHONY: find-dep
find-deps:
	pip install pip-tools
	pip-compile

.PHONY: dep
dep:
	pip install -r requirements.txt

.PHONY: test
test:
	PYTHONPATH=${PYTHONPATH}:. python -m unittest discover -p "*_test.py"

.PHONY: typecheck
typecheck:
	PYTHONPATH=${PYTHONPATH}:. mypy . --ignore-missing-imports

.PHONY: lint
lint:
	PYTHONPATH=${PYTHONPATH}:. pyflakes paranuara

.PHONY: run
run:
	PYTHONPATH=${PYTHONPATH}:. FLASK_ENV=development flask run
