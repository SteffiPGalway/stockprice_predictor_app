#!/bin/bash
# gunicorn run:app --bind 0.0.0.0:8080 --reload --log-level debug
web: gunicorn run:app --bind 0.0.0.0:$PORT --reload --log-level debug

