PYTHON ?= python

.PHONY: inplace build test publish doc publish-doc lint clean

inplace:
	@echo "Installing package in-place"
	pip install --editable . --use-mirrors
	@echo ""

build:
	@echo "Building becas-python"
	$(PYTHON) setup.py build
	@echo ""

test: build
	@echo "Running Python tests"
	$(PYTHON) test_becas.py
	@echo ""

publish:
	@echo "Publishing becas-python to PyPI"
	$(PYTHON) setup.py sdist bdist_wininst upload
	@echo ""

doc:
	@echo "Building HTML documentation"
	make -C docs html
	@echo ""

publish-doc: clean doc
	@echo "Publishing HTML documentation"
	git checkout gh-pages
	cp -r docs/build/html/* .
	find . -name "*.pyc" | xargs rm -f
	rm -rf docs
	git add .
	git commit
	git push origin gh-pages
	git checkout master
	@echo ""

lint:
	@echo "Linting Python files"
	flake8 becas.py setup.py test_becas.py
	pylint -E -i y becas.py setup.py test_becas.py
	@echo ""

clean:
	@echo "Cleaning build artifacts and temp files"
	find . -name "*.pyc" | xargs rm -f
	rm -rf build
	rm -rf dist becas.egg-info MANIFEST
	rm -rf __pycache__
	make -C docs clean
	@echo ""
