# Makefile for development and demo.
# See INSTALL and docs/dev.txt for details.

SHELL = /bin/bash
PROJECT = 'django-doctor'
ROOT_DIR = $(shell pwd)
BIN_DIR = $(ROOT_DIR)/bin
DATA_DIR = $(ROOT_DIR)/var
WGET = wget
PYTHON = $(shell which python)
BUILDOUT_CFG = $(ROOT_DIR)/etc/buildout.cfg
BUILDOUT_DIR = $(ROOT_DIR)/lib/buildout
BUILDOUT_VERSION = 1.7.0
BUILDOUT_BOOTSTRAP_URL = https://raw.github.com/buildout/buildout/$(BUILDOUT_VERSION)/bootstrap/bootstrap.py
BUILDOUT_BOOTSTRAP = $(BUILDOUT_DIR)/bootstrap.py
BUILDOUT_BOOTSTRAP_ARGS = -c $(BUILDOUT_CFG) --version=$(BUILDOUT_VERSION) --distribute buildout:directory=$(ROOT_DIR)
BUILDOUT = $(BIN_DIR)/buildout
BUILDOUT_ARGS = -N -c $(BUILDOUT_CFG) buildout:directory=$(ROOT_DIR)
NOSE = $(BIN_DIR)/nosetests

configure:
	# Configuration is stored in etc/ folder. Not generated yet.


develop: buildout


buildout:
	if [ ! -d $(BUILDOUT_DIR) ]; then mkdir -p $(BUILDOUT_DIR); fi
	if [ ! -f $(BUILDOUT_BOOTSTRAP) ]; then wget -O $(BUILDOUT_BOOTSTRAP) $(BUILDOUT_BOOTSTRAP_URL); fi
	if [ ! -x $(BUILDOUT) ]; then $(PYTHON) $(BUILDOUT_BOOTSTRAP) $(BUILDOUT_BOOTSTRAP_ARGS); fi
	$(BUILDOUT) $(BUILDOUT_ARGS)


clean:
	find $(ROOT_DIR)/ -name "*.pyc" -delete
	find $(ROOT_DIR)/ -name ".noseids" -delete


distclean: clean
	rm -rf $(ROOT_DIR)/*.egg-info
	rm -rf $(ROOT_DIR)/demo/*.egg-info


maintainer-clean: distclean
	rm -rf $(ROOT_DIR)/bin/
	rm -rf $(ROOT_DIR)/lib/


release:
	bin/fullrelease


test: test-demo


test-demo:
	bin/demo test demo
	mv $(ROOT_DIR)/.coverage $(DATA_DIR)/test/demo.coverage


demo: develop
	bin/demo syncdb --noinput


serve:
	bin/demo runserver


healthcheck:
	$(NOSE) --config=$(ROOT_DIR)/etc/nose.cfg --attr="is_healthcheck" django_doctor_demo
