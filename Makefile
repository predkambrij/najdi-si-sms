.PHONY: all test install

all:
	@echo "Commands:"
	@echo "    make install - Install to system"
	@echo "    make test - Run test"


install:
	@type pip || { echo "ERROR: Please install python-pip!"; exit 1; }
	pip install .

test:
	python setup.py test
