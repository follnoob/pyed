.PHONY: clean tar zip clean_py release  
# Python path
PYTHON=python3
# Arguments for run
ARGS=
# Version of pyed
VERSION=0.1.0

release: sdist wheel

sdist:
	$(PYTHON) setup.py sdist

wheel:
	$(PYTHON) setup.py bdist_wheel

install:
	$(PYTHON) setup.py install

run:
	$(PYTHON) -m pyed $(ARGS)

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

clean_py:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +
	find . -name "__pycache__" -type d -exec rm -rf {} +

clean: clean_py
	rm -rf $(OUT_DIR)
	rm -rf pyed.egg-info
	rm -rf build
	rm -rf dist
