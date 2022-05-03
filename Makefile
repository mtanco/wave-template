WAVE_URL:=https://github.com/h2oai/wave/releases/download/v0.16.0/wave-0.16.0-darwin-amd64.tar.gz
WAVE_DIR:=$(shell pwd)/wave

venv:
	python3.7 -m venv venv
	./venv/bin/python3 -m pip install --upgrade pip

.PHONY: setup
setup: venv
	./venv/bin/pip3 install -r requirements.txt

.PHONY: setup-test
setup-test: venv setup
	./venv/bin/pip3 install -r requirements-test.txt
	./venv/bin/playwright install

.PHONY: run-app
run-app:
	H2O_WAVE_NO_LOG=True ./venv/bin/wave run src.app

.PHONY: format
format:
	./venv/bin/isort --skip venv --skip wave .
	./venv/bin/black --exclude='(venv|wave)' .


.PHONY: test
test:
	@PYTHONPATH=. ./venv/bin/pytest --no-header tests/unit/

.PHONY: test-style
test-style:
	@./venv/bin/flake8

.PHONY: test-e2e
test-e2e:
	PYTHONPATH=. ./venv/bin/pytest --headed tests/e2e/

.PHONY: clean
clean:
	rm -rf venv wave