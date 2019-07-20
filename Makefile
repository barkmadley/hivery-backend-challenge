.PHONY: setup
setup:
	# Requires python 3
	# virtualenv .venv
	@echo "Please run 'source .venv/bin/activate' to enter virtualenv for subsequent commands"

.PHONY: dep
dep:
	pip install pip-tools
	pip-compile > requirements.txt
	pip install -r requirements.txt

.PHONY: test
test:
	PYTHONPATH=${PYTHONPATH}:. python -m unittest discover -s src -p "*_test.py"

.PHONY: typecheck
typecheck:
	PYTHONPATH=${PYTHONPATH}:. mypy src
