.PHONY: clean
PYTHON=python3  # Python path
ARGS=			# Arguments for run
VERSION=  		# Version for the zip and tar (start with '-')

run:
	$(PYTHON) pyed.py $(ARGS)

tar: clean
	tar -cvzf pyed$(VERSION).tar.gz pyed *.py README.md VERSION LICENSE

zip: clean
	zip -r pyed$(VERSION).zip pyed *.py VERSION README.md LICENSE

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +
	find . -name "__pycache__" -type d -exec rm -rf {} +

