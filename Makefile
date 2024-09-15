PREFIX ?= ~/.local

PYTHON := $(shell which python)
PIP := $(shell which pip)

install_deps:
	$(PIP) install -r requirements.txt
	$(PIP) install pyinstaller

build: install_deps
	$(PYTHON) -m PyInstaller main.spec

install: build
	install -m 755 dist/debuggen $(PREFIX)/bin/debuggen

uninstall:
	rm -f $(PREFIX)/bin/debuggen

clean:
	rm -rf dist build __pycache__

.PHONY: install_deps build install uninstall clean
