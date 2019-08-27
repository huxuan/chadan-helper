.PHONY: clean deps lint pycodestyle pyflakes pylint dist

clean:
	find . -name '*.pyc' -print0 | xargs -0 rm -f
	find . -name '*.swp' -print0 | xargs -0 rm -f
	find . -name '__pycache__' -print0 | xargs -0 rm -rf
	-rm -rf build dist *.egg-info .eggs *.spec

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

dist:
	pyinstaller --clean -F main.py
	cp config.example.json README.md dist
