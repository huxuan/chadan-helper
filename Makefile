.PHONY: clean deps install lint pycodestyle pyflakes pylint test

clean:
	find . -name '*.pyc' -print0 | xargs -0 rm -f
	find . -name '*.swp' -print0 | xargs -0 rm -f
	find . -name '__pycache__' -print0 | xargs -0 rm -rf
	-rm -rf build dist *.egg-info .eggs

deps:
	pip install -r requirements.txt

install:
	python setup.py install

lint: pycodestyle pyflakes pylint

pycodestyle:
	-pycodestyle --statistics --count *.py

pyflakes:
	-pyflakes *.py

pylint:
	-pylint *.py
