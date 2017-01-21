.PHONY: clean tar zip clean_py
PYTHON=python3  # Python path
ARGS=			# Arguments for run
VERSION=  		# Version for the zip and tar (start with '-')
OUT_DIR=dist	# dist folder as output

run:
	$(PYTHON) pyed.py $(ARGS)

tar: clean_py $(OUT_DIR)
	tar -cvzf pyed$(VERSION).tar.gz pyed *.py README.md VERSION.txt LICENSE.txt
	mv *.tar.gz $(OUT_DIR)

zip: clean_py $(OUT_DIR)
	zip -r $(OUT_DIR)/pyed$(VERSION).zip pyed *.py VERSION.txt README.md LICENSE.txt
	mv *.zip $(OUT_DIR)

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

clean_py:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +
	find . -name "__pycache__" -type d -exec rm -rf {} +

clean: clean_py
	rm -rf $(OUT_DIR)
