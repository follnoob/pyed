.PHONY: clean tar zip clean_py release  
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

clean: clean_py
	rm -rf $(OUT_DIR)
	rm -rf pyed.egg-info
	rm -rf build
	rm -rf dist
