.PHONY: clean tar zip release  
# Python path
PYTHON=python3
# Arguments for run
ARGS=

release: sdist wheel

sdist:
	$(PYTHON) setup.py sdist

wheel:
	$(PYTHON) setup.py bdist_wheel

install:
	$(PYTHON) setup.py install

run:
	$(PYTHON) -m pyed $(ARGS)

clean:
	rm -rf pyed.egg-info
	rm -rf build
	rm -rf dist
