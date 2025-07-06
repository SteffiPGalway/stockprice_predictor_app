#!/bin/bash
gunicorn run:app --bind 0.0.0.0:$PORT --reload --log-level debug
