.PHONY: clean build sdist wheel
# Python path
PYTHON=python3

build: sdist wheel

sdist:
	$(PYTHON) setup.py sdist

wheel:
	$(PYTHON) setup.py bdist_wheel

install:
	$(PYTHON) setup.py install

clean:
	rm -rf pyed.egg-info
	rm -rf build
	rm -rf dist
