#!/bin/bash
gunicorn run:app --bind 0.0.0.0:8000 --reload --log-level debug
