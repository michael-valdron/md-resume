# Makefile
# Author: Michael Valdron
# Date: Feb. 28, 2021

ifndef PYTHON
PYTHON := python3
endif

ifndef PIP
PIP := pip
endif

ifndef STYLE
STYLE := styles/style.css
endif

OUT_DIR := out
MD2PDF := md2pdf --css $(OUT_DIR)/style.out.css $(OUT_DIR)/content.out.md $(OUT_DIR)/resume.pdf
BUILD_CMD := $(PYTHON) build.py $(OUT_DIR)

default:
	# $(BUILD_CMD) content/content.md ... --css $(STYLE)
	$(BUILD_CMD) content/content.md \
--header content/header.md \
--css $(STYLE)
	$(MD2PDF)

view:
	(cd "$(PWD)/$(OUT_DIR)" && python3 -m http.server)

clean:
	rm -rf $(OUT_DIR)/

deps:
	$(PIP) install -r requirements.txt

.PHONY: default view clean deps
