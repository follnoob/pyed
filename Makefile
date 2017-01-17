.PHONY: clean
ARGS=""

run:
	python3 pyed.py $(ARGS) &

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +
	find . -name "__pycache__" -type d -exec rm -rf {} +

