#!/bin/bash

pip install -r requirements.txt
gunicorn -w 4 --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker main:app
