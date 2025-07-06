#!/bin/bash
gunicorn run:app --bind 0.0.0.0:5000 --reload --log-level debug

