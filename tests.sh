#!/bin/sh

# Run tests
cat .env.dev > .env
pytest -sq --cache-clear
