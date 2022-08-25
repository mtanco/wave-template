venv:
	python3 -m venv venv
	./venv/bin/python3 -m pip install --upgrade pip

.PHONY: setup
setup: venv
	./venv/bin/pip3 install -r requirements.in

.PHONY: setup-dev
setup-dev: venv setup
	./venv/bin/pip3 install -r requirements-test.txt
	./venv/bin/playwright install

.PHONY: run-app
run-app:
	H2O_WAVE_NO_LOG=True ./venv/bin/wave run src.app

.PHONY: format
format: setup-dev
	./venv/bin/isort src/*
	./venv/bin/black src/*

libraries:
	mkdir libraries

.PHONY: fat-bundle
fat-bundle: setup-dev libraries
	./venv/bin/pip-compile \
		--quiet \
		--generate-hashes \
		--output-file=requirements.txt \
		requirements.in
	./venv/bin/pip download \
		-r requirements.txt \
		--platform manylinux1_x86_64 \
		--python-version 39 \
		--no-deps \
		-d libraries
	ls libraries | sed 's/^/.\/libraries\//' > requirements.txt

.PHONY: clean
clean:
	rm -rf venv libraries