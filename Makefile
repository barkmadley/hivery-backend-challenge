.PHONY: setup
setup:
	# Requires python 3
	# virtualenv .venv
	@echo "Please run 'source .venv/bin/activate' to enter virtualenv for subsequent commands"

.PHONY: dep
dep:
	pip install pip-tools
	pip-compile
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
