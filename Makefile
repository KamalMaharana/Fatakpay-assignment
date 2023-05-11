# Makefile for Fatakpay Backend Challenge
.ONESHELL:
SHELL := /bin/bash


# Set the default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := pip

# Targets
.PHONY: run
run:  ## Run the application
	uvicorn main:app --reload

.PHONY: install
install:  ## Install dependencies
	$(PYTHON) -m venv venv
	source venv/bin/activate
	$(PIP) install -r requirements.txt

.PHONY: test
test:  ## Run unit tests
	$(PYTHON) -m unittest Test/test_payment.py

.PHONY: clean
clean:  ## Clean up generated files
	rm -f Database/payment.db
	rm -rf __pycache__
	rm -rf Test/__pycache__
	rm -rf .coverage

.PHONY: help
help:  ## Show this help message
	@echo "Fatakpay Backend Challenge Makefile"
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
