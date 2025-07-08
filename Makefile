# Makefile
# Author: Michael Valdron
# Date: Feb. 28, 2021

ifndef GO_CMD
GO_CMD := go
endif

ifndef PYTHON
PYTHON := python3
endif

ifndef PIP
PIP := pip
endif

ifndef STYLE
STYLE := styles/style.css
endif

ifndef MD_BASE_TEMPLATE
MD_BASE_TEMPLATE := templates/base.md.tmpl
endif

MDTMPL_BIN := $(PWD)/bin/mdtmpl

OUT_DIR := out
MD2PDF := md2pdf --css $(STYLE) $(OUT_DIR)/resume.md $(OUT_DIR)/resume.pdf

ifndef MDTMPL_CMD
MDTMPL_CMD := $(MDTMPL_BIN)
endif

default: build
	mkdir -p $(OUT_DIR)
	$(MDTMPL_CMD) -f -t $(MD_BASE_TEMPLATE) -o $(OUT_DIR)/resume.md
	$(MD2PDF)

build: deps
	(cd $(PWD)/mdtmpl && go build -o $(MDTMPL_BIN))

view:
	(cd "$(PWD)/$(OUT_DIR)" && $(PYTHON) -m http.server)

clean:
	rm -rf $(OUT_DIR)/ bin/

deps:
	$(PIP) install -r requirements.txt

.PHONY: default build view clean deps
