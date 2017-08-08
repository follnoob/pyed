.PHONY: clean build sdist wheel
# Python path
PYTHON=python3

build: clean sdist wheel

sdist:
	$(PYTHON) setup.py sdist

wheel:
	$(PYTHON) setup.py bdist_wheel

install:
	$(PYTHON) setup.py install

clean:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist
